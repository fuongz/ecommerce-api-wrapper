from time import perf_counter, sleep
from typing import Dict, List
import requests
import urllib

import tqdm

from ...utils.faker import Faker
from .constants import LazadaConstants
from .schemas.response_schema import ResponseSchema


class Lazada:
    def __init__(
        self,
        debug=False,
        timeout=LazadaConstants.TIMEOUT,
        sleep_time=LazadaConstants.SLEEP_TIME,
        max_page=LazadaConstants.MAX_PAGE,
        max_retry=LazadaConstants.MAX_RETRY,
        proxies=None,
        proxies_headers=None,
        proxies_debug=False,
        country_code="ID",
        search_type="catalog",
    ) -> None:
        self.debug = debug
        self.proxies_debug = proxies_debug

        # HTTP Client config
        self.proxies = proxies
        self.proxies_headers = proxies_headers or {}
        self.connection_timeout: int = timeout
        self.read_timeout = LazadaConstants.READ_TIMEOUT
        self.sleep_time: int = sleep_time
        self.max_page: int = max_page
        self.max_retry: int = max_retry
        self.country_code: str = country_code.lower()
        self.search_type: str = search_type

        # Proxy
        self.proxy_index: int = 0

        if self.proxies or self.proxies_headers:
            self.session = requests.Session()
            if self.proxies and len(self.proxies) > 0:
                self.session.proxies = (
                    self.proxies[self.proxy_index]
                    if isinstance(self.proxies, list)
                    else self.proxies
                )
            if self.proxies_headers:
                self.session.headers = self.proxies_headers
        else:
            self.session = requests.Session()

    def _log(self, message, *args, **kws):
        if self.debug is True:
            tqdm.tqdm.write(message, *args, **kws)

    def _search_products(self, keyword: str) -> List[Dict]:
        if not keyword:
            raise ValueError("Keyword cannot be empty")

        encoded_keyword = urllib.parse.quote(keyword)
        products = []
        retry_count = 0
        page_number = 1
        while True:
            try:
                headers = {
                    **LazadaConstants.HEADERS,
                    "User-Agent": Faker.user_agent(),
                    "Referer": f"{LazadaConstants.API_URL}{self.country_code}",
                }
                start = (page_number - 1) * 40 if page_number > 1 else 0
                if retry_count > 0:
                    self._log(
                        f"[kw={keyword}] Retrying {retry_count} times with page {page_number}..."
                    )
                else:
                    self._log(
                        f"[kw={keyword}] Fetching page {page_number} (start from {start})..."
                    )
                response = None
                endpoint = f"{LazadaConstants.API_URL}{self.country_code}/{self.search_type}/?ajax=true&isFirstRequest=true&page={page_number}&q={encoded_keyword}"

                start_time = perf_counter()
                with self.session as session:
                    if self.proxies:
                        headers = {**headers, **self.proxies_headers}
                        if self.proxies_debug is True:
                            self._proxy_check()
                        response = session.get(
                            endpoint,
                            headers=headers,
                            verify=False,
                            timeout=(self.connection_timeout, self.read_timeout),
                        )
                    else:
                        response = session.get(
                            endpoint,
                            headers=headers,
                            timeout=(self.connection_timeout, self.read_timeout),
                        )
                end_time = perf_counter()
                self._log(
                    f"--> [kw={keyword}] Fetched time: {end_time - start_time} seconds!"
                )
                if response and response.status_code == 200:
                    retry_count = 0
                    json = response.json()
                    transformed = ResponseSchema().load({**json, "keyword": keyword})
                    cur_products = transformed.get("products", [])
                    products += cur_products
                    if not self.proxies:
                        sleep(1)
                    page_number += 1
                    if len(products) == 0 or page_number > self.max_page:
                        self._log(
                            f"✅ [kw={keyword}] Collected {len(products)} products!"
                        )
                        break

            except requests.Timeout as e:
                self._log(f"[kw={keyword}] {str(e)}")
                retry_count += 1
                if retry_count >= self.max_retry:
                    print(f"⛔️ [kw={keyword}] Collected {len(products)} products!")
                    break
                if isinstance(self.proxies, list):
                    next_index = (
                        self.proxy_index + 1
                        if self.proxy_index < len(self.proxies) - 1
                        else 0
                    )
                    self.proxy_index += next_index
                    self.session.proxies = self.proxies[next_index]
                if not self.proxies:
                    sleep(self.sleep_time)
                continue

            except requests.ConnectionError as e:
                self._log(f"[kw={keyword}] {str(e)}")
                retry_count += 1
                if retry_count >= self.max_retry:
                    print(f"⛔️ [kw={keyword}] Collected {len(products)} products!")
                    break
                continue

            except Exception as e:
                self._log(f"[kw={keyword}] {str(e)}")
                retry_count += 1
                if retry_count >= self.max_retry:
                    print(f"⛔️ [kw={keyword}] Collected {len(products)} products!")
                    break
                continue

        if len(products) == 0:
            return []

        return products

    def _proxy_check(self):
        try:
            response = self.session.get("https://ip.oxylabs.io/location", verify=False)
        except Exception:
            return
        if response.status_code == 200:
            json_response = response.json()
            ip_addr = json_response.get("ip", "Unknown")
            country: str = (
                json_response.get("providers", {})
                .get("ip2location", {})
                .get("country", "")
            )
            self._log(f"🚩 IP={ip_addr}, Country={country}")

from time import perf_counter, sleep
from typing import Dict, List
import requests
import urllib.parse
import tqdm
import urllib3

from ...utils.faker import Faker

from .utils.faker import TokopediaFaker
from .schemas.response_schema import ResponseSchema
from .constants import TokopediaConstants

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Tokopedia:
    def __init__(
        self,
        debug=False,
        timeout=TokopediaConstants.TIMEOUT,
        sleep_time=TokopediaConstants.SLEEP_TIME,
        max_page=TokopediaConstants.MAX_PAGE,
        max_retry=TokopediaConstants.MAX_RETRY,
        proxies=None,
        proxies_headers=None,
        proxies_debug=False,
    ) -> None:
        """
        Initialize a TokopediaCrawler instance.

        Parameters:
            debug (bool, optional): If True, enable debug mode. Defaults to False.
            timeout (int, optional): The HTTP connection timeout in seconds. Defaults to 3.
            max_workers (int, optional): The maximum number of concurrent workers. Defaults to 5.
            concurrent_type (str, optional): The type of concurrency to use, either "thread" or "process". Defaults to "thread".
            sleep_time (int, optional): The amount of time to sleep between requests in seconds. Defaults to 10.
            max_page (int, optional): The maximum number of pages to fetch. Defaults to 2.
            max_retry (int, optional): The maximum number of retries for each request. Defaults to 10.
        """
        self.debug = debug or False
        self.proxies_debug = proxies_debug or False

        # HTTP Client config
        self.proxies = proxies
        self.proxies_headers = proxies_headers or {}
        self.connection_timeout: int = timeout
        self.read_timeout = TokopediaConstants.READ_TIMEOUT
        self.sleep_time: int = sleep_time
        self.max_page: int = max_page
        self.max_retry: int = max_retry

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
        """
        Searches and retrieves products from Tokopedia based on the given keyword.

        The function performs a paginated search using the Tokopedia GraphQL API,
        and collects products until the maximum number of pages is reached or an
        error occurs. It handles retries for timeouts and connection errors and
        logs each request attempt. The search results are transformed into a
        ResponseSchema object and aggregated into a list.

        Args:
            keyword (str): The search keyword to query the Tokopedia API.

        Returns:
            List[Dict]: A list of products retrieved from the API for the given keyword.
        """
        if not keyword:
            raise ValueError("Keyword cannot be empty")

        encoded_keyword = urllib.parse.quote(keyword)
        component_id = "02.01.00.00"
        products = []
        retry_count = 0
        page_number = 1
        additional_params = ""
        while True:
            try:
                unique_id = TokopediaFaker.unique_id()
                device_id = TokopediaFaker.device_id()

                headers = {
                    **TokopediaConstants.HEADERS,
                    "User-Agent": Faker.user_agent(),
                    "bd-device-id": device_id,
                    "bd-web-id": device_id,
                    "iris_session_id": TokopediaFaker.iris_session_id(),
                    "Referer": f"{TokopediaConstants.REFERER}/search?navsource=&page={page_number}&q={encoded_keyword}&srp_component_id={component_id}&srp_page_id=&srp_page_title=&st={additional_params}",
                }
                start = (page_number - 1) * 60 if page_number > 1 else 0
                if retry_count > 0:
                    self._log(
                        f"[kw={keyword}] Retrying {retry_count} times with page {page_number}..."
                    )
                else:
                    self._log(
                        f"[kw={keyword}] Fetching page {page_number} (start from {start})..."
                    )
                response = None

                dict_data = {
                    "operationName": "SearchProductV5Query",
                    "variables": {
                        "params": f"device=desktop&srp_component_id={component_id}&srp_page_id=&srp_page_title=&enter_method=normal_search&l_name=sre&navsource=&ob=23&page={page_number}&q={encoded_keyword}&related=true&rows=60&safe_search=false&sc=&scheme=https&shipping=&show_adult=false&source=search&st=product&start={start}&topads_bucket=true&unique_id={unique_id}&user_addressId=&user_cityId=176&user_districtId=2274&user_id=&user_lat=&user_long=&user_postCode=&user_warehouseId=&variants=&warehouses="
                    },
                    "query": "query SearchProductV5Query($params: String!) {\n  searchProductV5(params: $params) {\n    header {\n      totalData\n      responseCode\n      keywordProcess\n      keywordIntention\n      componentID\n      isQuerySafe\n      additionalParams\n      backendFilters\n      meta {\n        dynamicFields\n        __typename\n      }\n      __typename\n    }\n    data {\n      totalDataText\n      banner {\n        position\n        text\n        applink\n        url\n        imageURL\n        componentID\n        trackingOption\n        __typename\n      }\n      redirection {\n        url\n        __typename\n      }\n      related {\n        relatedKeyword\n        position\n        trackingOption\n        otherRelated {\n          keyword\n          url\n          applink\n          componentID\n          products {\n            oldID: id\n            id: id_str_auto_\n            name\n            url\n            applink\n            mediaURL {\n              image\n              __typename\n            }\n            shop {\n              oldID: id\n              id: id_str_auto_\n              name\n              city\n              tier\n              __typename\n            }\n            badge {\n              oldID: id\n              id: id_str_auto_\n              title\n              url\n              __typename\n            }\n            price {\n              text\n              number\n              __typename\n            }\n            freeShipping {\n              url\n              __typename\n            }\n            labelGroups {\n              position\n              title\n              type\n              url\n              styles {\n                key\n                value\n                __typename\n              }\n              __typename\n            }\n            rating\n            wishlist\n            ads {\n              id\n              productClickURL\n              productViewURL\n              productWishlistURL\n              tag\n              __typename\n            }\n            meta {\n              oldWarehouseID: warehouseID\n              warehouseID: warehouseID_str_auto_\n              componentID\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        query\n        text\n        componentID\n        trackingOption\n        __typename\n      }\n      ticker {\n        oldID: id\n        id: id_str_auto_\n        text\n        query\n        applink\n        componentID\n        trackingOption\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      products {\n        oldID: id\n        id: id_str_auto_\n        ttsProductID\n        name\n        url\n        applink\n        mediaURL {\n          image\n          image300\n          videoCustom\n          __typename\n        }\n        shop {\n          oldID: id\n          id: id_str_auto_\n          ttsSellerID\n          name\n          url\n          city\n          tier\n          __typename\n        }\n        stock {\n          ttsSKUID\n          __typename\n        }\n        badge {\n          oldID: id\n          id: id_str_auto_\n          title\n          url\n          __typename\n        }\n        price {\n          text\n          number\n          range\n          original\n          discountPercentage\n          __typename\n        }\n        freeShipping {\n          url\n          __typename\n        }\n        labelGroups {\n          position\n          title\n          type\n          url\n          styles {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        labelGroupsVariant {\n          title\n          type\n          typeVariant\n          hexColor\n          __typename\n        }\n        category {\n          oldID: id\n          id: id_str_auto_\n          name\n          breadcrumb\n          gaKey\n          __typename\n        }\n        rating\n        wishlist\n        ads {\n          id\n          productClickURL\n          productViewURL\n          productWishlistURL\n          tag\n          __typename\n        }\n        meta {\n          oldParentID: parentID\n          parentID: parentID_str_auto_\n          oldWarehouseID: warehouseID\n          warehouseID: warehouseID_str_auto_\n          isImageBlurred\n          isPortrait\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                }
                endpoint = f"{TokopediaConstants.GRAPHQL_URL}/{TokopediaConstants.PATH_SEARCH_PRODUCTS}"

                start_time = perf_counter()
                with self.session as session:
                    if self.proxies:
                        headers = {**headers, **self.proxies_headers}
                        if self.proxies_debug is True:
                            self._proxy_check()
                        response = session.post(
                            endpoint,
                            headers=headers,
                            json=dict_data,
                            verify=False,
                            timeout=(self.connection_timeout, self.read_timeout),
                        )
                    else:
                        response = session.post(
                            endpoint,
                            headers=headers,
                            json=dict_data,
                            timeout=(self.connection_timeout, self.read_timeout),
                        )
                end_time = perf_counter()
                self._log(
                    f"--> [kw={keyword}] Fetched time: {end_time - start_time} seconds!"
                )
                if response and response.status_code == 200:
                    retry_count = 0
                    json = response.json()
                    cur_additional_params = (
                        json.get("data", {})
                        .get("searchProductV5", {})
                        .get("header", {})
                        .get("additionalParams", None)
                    )
                    if cur_additional_params:
                        additional_params = f"&{cur_additional_params}"
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

from typing import List, Tuple
from tqdm.contrib.concurrent import thread_map, process_map


class EcommerceApiWrapper:
    def __init__(
        self,
        ecom_type="tokopedia",
        debug=False,
        timeout=None,
        max_workers=None,
        concurrent_type=None,
        sleep_time=None,
        max_page=None,
        max_retry=None,
        proxies=None,
        proxies_headers=None,
        proxies_debug=False,
        country_code="ID",
        search_type="catalog",
    ):
        self.ecom_type = ecom_type
        self.max_workers = max_workers or 5
        self.concurrent_type = concurrent_type or "thread"

        self.client = None

        if self.ecom_type == "tokopedia":
            from .providers.tokopedia_api_wrapper.tokopedia import Tokopedia

            self.client = Tokopedia(
                debug=debug,
                timeout=timeout,
                sleep_time=sleep_time,
                max_page=max_page,
                max_retry=max_retry,
                proxies=proxies,
                proxies_headers=proxies_headers,
                proxies_debug=proxies_debug,
            )
        elif self.ecom_type == "lazada":
            from .providers.lazada_api_wrapper.lazada import Lazada

            self.client = Lazada(
                debug=debug,
                timeout=timeout,
                sleep_time=sleep_time,
                max_page=max_page,
                max_retry=max_retry,
                proxies=proxies,
                proxies_headers=proxies_headers,
                proxies_debug=proxies_debug,
                country_code=country_code,
                search_type=search_type,
            )

        else:
            raise NotImplementedError

    def search_products(self, keywords: List[str]) -> Tuple[List, ...]:
        """
        Search for products in parallel using the given keywords.

        Args:
            keywords (List[str]): List of keywords to search for.

        Returns:
            Tuple[List[ResponseSchema], ...]: A tuple of lists of ResponseSchema,
            where each list contains the products for the corresponding keyword.
        """
        max_workers = min(len(keywords), self.max_workers)
        if self.concurrent_type == "thread":
            return thread_map(
                self.client._search_products,
                keywords,
                max_workers=max_workers,
                desc="Searching products",
            )
        elif self.concurrent_type == "process":
            return process_map(
                self.client._search_products,
                keywords,
                max_workers=max_workers,
            )

        else:
            raise ValueError("Invalid concurrent type")

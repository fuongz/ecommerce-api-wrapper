import unittest

from src.ecommerce_api_wrapper.ecommerce_api_wrapper import (
    EcommerceApiWrapper,
)


class CommonTest(unittest.TestCase):
    def setUp(self):
        self.proxies = []
        self.keywords = ["xiaomi"]

    def test_lazada_search_products(self):
        self.client = EcommerceApiWrapper(
            ecom_type="lazada",
            debug=True,
            max_page=1,
            max_retry=1,
            proxies=self.proxies,
        )
        response = self.client.search_products(self.keywords)
        self.assertIsNotNone(response)

    def test_tokopedia_search_products(self):
        self.client = EcommerceApiWrapper(
            ecom_type="tokopedia",
            debug=True,
            max_page=1,
            max_retry=1,
            proxies=self.proxies,
        )
        response = self.client.search_products(self.keywords)
        self.assertIsNotNone(response)

import unittest

from src.ecommerce_api_wrapper.ecommerce_api_wrapper import (
    EcommerceApiWrapper,
)


class ConcurrentTest(unittest.TestCase):
    def setUp(self):
        self.proxies = []
        self.keywords = ["xiaomi"]

    def test_with_thread(self):
        self.client = EcommerceApiWrapper(
            ecom_type="tokopedia",
            debug=True,
            max_page=1,
            max_retry=1,
            proxies=self.proxies,
            concurrent_type="thread",
        )
        response = self.client.search_products(self.keywords)
        self.assertIsNotNone(response)

    def test_with_process(self):
        self.client = EcommerceApiWrapper(
            ecom_type="tokopedia",
            debug=True,
            max_page=1,
            max_retry=1,
            proxies=self.proxies,
            concurrent_type="process",
        )
        response = self.client.search_products(self.keywords)
        self.assertIsNotNone(response)

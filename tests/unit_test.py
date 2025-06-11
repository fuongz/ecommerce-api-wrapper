import unittest

from src.ecommerce_api_wrapper.ecommerce_api_wrapper import (
    EcommerceApiWrapper,
)


class CommonTest(unittest.TestCase):
    def setUp(self):
        proxies = []
        self.client = EcommerceApiWrapper(
            ecom_type="lazada", debug=True, max_page=10, max_retry=1, proxies=proxies
        )

    def test_search_products(self):
        keywords = ["xiaomi"]
        response = self.client.search_products(keywords)
        self.assertIsNotNone(response)

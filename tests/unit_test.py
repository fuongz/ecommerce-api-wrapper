import unittest

from src.tokopedia_api_wrapper.tokopedia import Tokopedia


class CommonTest(unittest.TestCase):
    def setUp(self):
        self.client = Tokopedia(debug=True, max_page=1, max_workers=1)

    def test_search_products(self):
        keywords = ["samsung"]
        response = self.client.parallel_search_products(keywords)
        self.assertIsNotNone(response)

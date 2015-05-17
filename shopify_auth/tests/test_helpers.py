from django.test import TestCase
from ..helpers import add_query_parameters_to_url


class HelpersTestCase(TestCase):

    def test_add_query_parameters_to_url(self):
        """
        Test add_query_parameters_to_url helper.
        """
        # Define a list of test cases as triples in the format (url, query_parameters, expected_url)
        test_cases = [
            ('http://example.com', {'page': 2}, 'http://example.com?page=2'),
            ('http://example.com?size=xl', {'page': 5}, 'http://example.com?page=5&size=xl'),
            ('http://example.com?size=xl&page=1', {'page': 5}, 'http://example.com?page=5&size=xl'),
        ]

        # Run each test case through the helper and check the expected output.
        for url, query_parameters, expected_url in test_cases:
            self.assertEqual(add_query_parameters_to_url(url, query_parameters), expected_url)

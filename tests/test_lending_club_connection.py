import json
import unittest

import httpretty

from config import API_CONFIG
from lending_club_ml.lending_club_connection import LendingClubConnection


class TestLendingClubConnection(unittest.TestCase):
    def setUp(self):
        self.lc_connection = LendingClubConnection(authorization='topsecret', investor_id='123')

    @httpretty.activate
    def test_get_listed_loans(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri='/'.join([API_CONFIG['base_url'], API_CONFIG['version'], 'loans/listing']),
            body=json.dumps({"loans": "Listed Loans"})
        )

        response = self.lc_connection.get_listed_loans()
        self.assertEqual(response.json()['loans'], 'Listed Loans')
        self.assertEqual(response.status_code, 200)

    @httpretty.activate
    def test_get_balance(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri='/'.join([API_CONFIG['base_url'],
                          API_CONFIG['version'],
                          'accounts/123/availablecash']),
            body=json.dumps({"availableCash": 10})
        )

        response = self.lc_connection.get_balance()
        self.assertEqual(response.json()["availableCash"], 10)
        self.assertEqual(response.status_code, 200)

    @httpretty.activate
    def test_get_loans_owned(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri='/'.join([API_CONFIG['base_url'],
                          API_CONFIG['version'],
                          'accounts/123/notes']),
            body=json.dumps({"notes": []})
        )

        response = self.lc_connection.get_loans_owned()
        self.assertEqual(response.json()["notes"], [])
        self.assertEqual(response.status_code, 200)

    @httpretty.activate
    def test_submit_order(self):
        expected_body = {
                    "orderInstructId": 10,
                    "loanId": "XYZ",
                    "requestedAmount": 25,
                    "investedAmount": 25,
                    "execution_status": "ORDER_FULFILLED"
        }

        httpretty.register_uri(
            method=httpretty.POST,
            uri='/'.join([API_CONFIG['base_url'],
                          API_CONFIG['version'],
                          'accounts/123/orders']),
            body=json.dumps(expected_body)
        )

        response = self.lc_connection.submit_order(
            loan_ids=['XYZ', 'sss'],
            loan_amounts=[25, 25],
            portfolio_id=0,
            safe_mode=False
        )

        self.assertEqual(response.json(), expected_body)
        self.assertEqual(response.status_code, 200)

    def test_safe_mode(self):
        response = self.lc_connection.submit_order(
            loan_ids=['XYZ', 'sss'],
            loan_amounts=[25, 25],
            portfolio_id='testing',
            safe_mode=True
        )
        self.assertIs(response, None)


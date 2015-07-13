import json
import unittest

import httpretty

from config import API_CONFIG
from lending_club_ml import MLOrderRecommender
from lending_club_ml.model_lib.base import BaseLoanModel


class DummyModel(BaseLoanModel):
    def recommend(self, listed_notes, value=25):
        chosen_notes = listed_notes[:2]
        return {n['loanId']: {'amount': value} for n in chosen_notes}


class TestMLOrderRecommender(unittest.TestCase):
    def setUp(self):
        self.order_recommender = MLOrderRecommender(
            note_model=DummyModel(),
            authorization='topsecret',
            investor_id='123'
        )

    @httpretty.activate
    def test_get_model_rec(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri='/'.join([API_CONFIG['base_url'], API_CONFIG['version'], 'loans/listing']),
            body=json.dumps({"loans": [{'loanId': 'l1'},
                                       {'loanId': 'l2'},
                                       {'loanId': 'l3'}]})
        )

        rec = self.order_recommender.get_model_rec()
        self.assertEqual(rec, {'l1': {'amount': 25}, 'l2': {'amount': 25}})

    @httpretty.activate
    def test_execute_recommended_order(self):
        expected_body = [
            {
                    "orderInstructId": 10,
                    "loanId": "l1",
                    "requestedAmount": 25,
                    "investedAmount": 25,
                    "execution_status": "ORDER_FULFILLED"
            },
            {
                    "orderInstructId": 10,
                    "loanId": "l2",
                    "requestedAmount": 25,
                    "investedAmount": 25,
                    "execution_status": "ORDER_FULFILLED"
            }
        ]
        httpretty.register_uri(
            method=httpretty.GET,
            uri='/'.join([API_CONFIG['base_url'], API_CONFIG['version'], 'loans/listing']),
            body=json.dumps({"loans": [{'loanId': 'l1'},
                                       {'loanId': 'l2'},
                                       {'loanId': 'l3'}]})
        )
        httpretty.register_uri(
            method=httpretty.POST,
            uri='/'.join([API_CONFIG['base_url'],
                          API_CONFIG['version'],
                          'accounts/123/orders']),
            body=json.dumps(expected_body)
        )

        response = self.order_recommender.execute_recommended_order(
            portfolio=0,
            safe_mode=False
        )

        self.assertEqual(response.json(), expected_body)
        self.assertEqual(response.status_code, 200)


from cytoolz.dicttoolz import merge
import pandas as pd

from lending_club_ml.lending_club_connection import LendingClubConnection


class MLOrderRecommender(object):
    """ Main class for recommending and executing orders from a model

    :param note_recommender: Recommender with a recommend method for deciding on loans to invest in.
        Expected to return a mapping of at least {id: {amount: dollar_amount}}
    :param authorization: HMAC authorization code from Lending Club.
        Intructions for generating this can be found here:
        https://www.lendingclub.com/developers/authentication.action
    :param investor_id: Id for executing order. This can be obtained from
        the Account Summary section on Lending Club website when a user is logged in.
    :param logger: logging instance
    """
    def __init__(self, note_model, authorization, investor_id, logger=None):
        self.note_model = note_model
        self.lc_connection = LendingClubConnection(
            authorization=authorization,
            investor_id=investor_id
        )
        self.logger = logger

    def __log(self, log):
        if self.logger is not None:
            self.logger.info(log)

    def execute_recommended_order(self, portfolio, safe_mode=True, **kwargs):

        recommended_loans = self.get_model_rec(**kwargs)
        self.__log(recommended_loans)

        loan_ids=recommended_loans.keys()
        loan_amounts=[x['amount'] for x in recommended_loans.values()]

        results = self.lc_connection.submit_order(
            loan_ids=loan_ids,
            loan_amounts=loan_amounts,
            portfolio_id=portfolio,
            safe_mode=safe_mode
        )
        return results

    def get_model_rec(self, **kwargs):
        listed_notes = self.lc_connection.get_listed_loans().json()['loans']
        chosen_notes = self.note_model.recommend(
            listed_notes,
            **kwargs
        )
        return chosen_notes

    def examine_rec_order(self, **kwargs):
        listed_loans = self.lc_connection.get_listed_loans().json()['loans']
        listed_dict = {x['id']: x for x in listed_loans}
        note_dict = self.get_model_rec(**kwargs)
        return pd.DataFrame([merge(note_dict[key], listed_dict[key])
                             for key in note_dict])

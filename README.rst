**************
LendingClubML
**************

Python module for interacting with Lending Club's API and executing machine learning investment strategies.

The main entry point, MLOrderRecommender, must be initialized with a fitted model with a recommend() method, which takes open loans and returns the loan ids and amounts to be invested in them. The recommenders and strategies in lending_club_ml.model_lib proivde a framework for creating these models.

=========
Examples:
=========

**Interacting with Lending Club:**::
    from lending_club_ml import LendingClubConnection, Order

    lc = LendingClubConnection(authorization='topsecret',
                           investor_id=123)
                     
    # Retrieve available loans to invest in
    lc.get_listed_loans()

    # Get account balance
    lc.get_balance()

    # Submit an order
    lc.submit_order(loan_ids=[112358], loan_amounts=[25], portfolio_id=1)



**Building a model and executing an order:**
``
from sklearn.linear_model import LogisticRegression

from lending_club_ml import MLOrderRecommender
from lending_club_ml.model_lib.adaptor import Adaptor
from lending_club_ml.model_lib.recommenders import ClassifierRecommender
from lending_club_ml.model_lib.strategies import TopXStrategy


model = LogisticRegression()
# Lending club data may be found here: https://www.lendingclub.com/info/download-data.action
model.fit(lending_club_data, response)
recommender = ClassifierRecommender(
    model = model,
    adaptor=Adaptor()
    strategy=TopXStrategy(n_notes=5, cash_per_note=25)
)

recommender = MLOrderRecommender(
    authorization='topsecret',
    investor_id=123,
    note_model=recommender
)
                                 
# Print information on recommended notes to buy
print recommender.examine_rec_order()

# Execute order on Lending Club
recommender.execute_recommended_order()
``


**Custom Recommender:**
``
from lending_club_ml import MLOrderRecommender
from lending_club_ml.model_lib.base import BaseLoanModel


class DummyModel(BaseLoanModel):
    def recommend(self, listed_loans):
        chosen_notes = listed_notes[:2]
        return {note['id']: {'amount': value} for note in chosen_notes}


recommender = ClassifierRecommender(
    model = model,
    adaptor=Adaptor()
    strategy=TopXStrategy(n_notes=5, cash_per_note=25)
)

recommender = MLOrderRecommender(
    authorization='topsecret',
    investor_id=123,
    note_model=recommender
)
                                 
# Print information on recommended notes to buy
print recommender.examine_rec_order()

# Execute order on Lending Club
recommender.execute_recommended_order()
``
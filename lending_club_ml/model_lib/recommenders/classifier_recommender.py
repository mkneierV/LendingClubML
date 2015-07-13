import numpy as np

from lending_club_ml.model_lib.base import BaseLoanModel


class ClassifierRecommender(BaseLoanModel):
    """Wrapper for a classification model using scikit-learns' API"""
    def __init__(self, model, adaptor, strategy):
        self.model = model
        self.adaptor = adaptor
        self.strategy = strategy

    def adaptor_transform(self, listed_notes):
        return self.adaptor.transform(listed_notes)

    def score_loans(self, notes):
        listed_notes = self.adaptor_transform(notes)
        probs = self.model.predict_proba(listed_notes)[:, 1]
        ids = [x['id'] for x in notes]
        expected_value = probs * np.array([x['int_rate'] for x in notes])
        return dict(zip(ids, expected_value))

    def recommend(self, listed_notes, **kwargs):
        scores = self.score_loans(listed_notes)
        return self.strategy.build_order(scores, **kwargs)







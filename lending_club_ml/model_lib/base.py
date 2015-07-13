import abc


class BaseLoanModel(object):
    @abc.abstractmethod
    def recommend(self, listed_notes, **kwargs):
        raise NotImplemented


class BaseStrategy(object):
    @abc.abstractmethod
    def build_order(self, scored_notes):
        raise NotImplementedError()
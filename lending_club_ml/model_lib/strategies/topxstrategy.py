from lending_club_ml.model_lib.base import BaseStrategy


class TopXStrategy(BaseStrategy):
    """Top X notes by model score"""

    def __init__(self, n_notes, cash_per_note=25):
        self.n_notes = n_notes
        self.cash_per_note = cash_per_note

    def build_order(self, scored_notes):
        sorted_notes = sorted(scored_notes, key=scored_notes.get, reverse=True)
        chosen = sorted_notes[:min(self.n_notes, len(sorted_notes) - 1)]
        return {id: {
            'amount': self.cash_per_note,
            'score': scored_notes[id]
        } for id in chosen}

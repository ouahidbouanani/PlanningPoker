# average_rule.py

class AverageRule:
    def __init__(self):
        pass  # You can add any initialization logic if needed

    def validate_votes(self, votes):
        # Validate each feature separately
        for feature in set(feature for _, feature in votes.keys()):
            feature_votes = {player: vote for (player, f), vote in votes.items() if f == feature}
            total_votes = sum(feature_votes.values())
            average_vote = total_votes / len(feature_votes)
            if not (1 <= average_vote <= 20):
                return False
        return True


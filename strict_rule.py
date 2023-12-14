# strict_rule.py

class StrictRule:
    def __init__(self):
        pass  # You can add any initialization logic if needed

    def validate_votes(self, votes):
        # Validate each feature separately
        for feature in set(feature for _, feature in votes.keys()):
            feature_votes = {player: vote for (player, f), vote in votes.items() if f == feature}
            if len(set(feature_votes.values())) > 1:
                return False
        return True


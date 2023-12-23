# strict_rule.py

class StrictRule:
    """
    @file strict_rule.py
    @brief Class implementing the Strict Rule for Planning Poker.

    @details
    The StrictRule class defines the validation logic for Planning Poker votes based on the strict rule.
    Each feature is validated separately, ensuring that all votes for a feature are unanimous.

    @note
    Create an instance of this class and pass it to the PlanningPokerGUI to use the strict rule for vote validation.

    @see
    For additional information on how to use this class, refer to the documentation of its methods.
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StrictRule, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # Initialization logic goes here

    def validate_votes(self, votes):
        while not self._is_unanimous(votes):
            # Voting is not unanimous, repeat the process
            print("Voting is not unanimous. Please vote again.")

        return True

    def _is_unanimous(self, votes):
        # Validate each feature separately
        for feature in set(feature for _, feature in votes.keys()):
            feature_votes = {player: vote for (player, f), vote in votes.items() if f == feature}
            if len(set(feature_votes.values())) > 1:
                return False
        return True
    def _check_unanimous(self, feature_votes):
        # Check if votes for a feature are unanimous
        return len(set(feature_votes.values())) == 1




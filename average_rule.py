# average_rule.py
class AverageRule:
    """
    @file average_rule.py
    @brief Class implementing the Average Rule for Planning Poker.

    @details
    The AverageRule class defines the validation logic for Planning Poker votes based on the average rule.
    Each feature is validated separately, ensuring that the average vote falls within the range [1, 20].

    @note
    Create an instance of this class and pass it to the PlanningPokerGUI to use the average rule for vote validation.

    @see
    For additional information on how to use this class, refer to the documentation of its methods.
    """
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, result):
        for observer in self.observers:
            observer.update(result)

    def validate_votes(self, votes):
        for feature in set(feature for _, feature in votes.keys()):
            feature_votes = {player: vote for (player, f), vote in votes.items() if f == feature}
            total_votes = sum(feature_votes.values())
            average_vote = total_votes / len(feature_votes)
            if not (1 <= average_vote <= 20):
                result = False
                self.notify_observers(result)
                return result
        result = True
        self.notify_observers(result)
        return result

# view.py
class AverageRuleView:
    def update(self, result):
        if result:
            print("Votes are valid.")
        else:
            print("Votes are invalid.")

# controller.py
class AverageRuleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self.view)

    def validate_votes(self, votes):
        return self.model.validate_votes(votes)



# average_rule.py

class AverageRule:
    def __init__(self):
        pass  # You can add any initialization logic if needed

    def validate_votes(self, votes):
        # Calculate the average value of votes and check if it's unanimous
        total_votes = sum(int(vote) for vote in votes.values())
        average_value = total_votes / len(votes)

        # Check if all votes are close enough to the average value
        return all(abs(int(vote) - average_value) < 0.5 for vote in votes.values())

# Add more methods or logic as needed for your average voting rules

# strict_rule.py

class StrictRule:
    def __init__(self):
        pass  # You can add any initialization logic if needed

    def validate_votes(self, votes):
        # Check if all votes are the same for unanimity
        return len(set(votes.values())) == 1

# Add more methods or logic as needed for your strict voting rules

from src.config import STARTUP_WEIGHTS, PROJECT_WEIGHTS

class ScoringEngine:
    def __init__(self, mode):
        self.mode = mode  # "startup" or "project"
        self.weights = STARTUP_WEIGHTS if mode == "startup" else PROJECT_WEIGHTS
    
    def score_dimension(self, dimension, score):
        """Score a single dimension (0-10)"""
        return max(0, min(10, score))  # Clamp between 0-10
    
    def calculate_final_score(self, dimension_scores):
        """Calculate weighted average"""
        total = sum(dimension_scores[dim] * self.weights[dim] 
                   for dim in self.weights.keys())
        return round(total, 2)
    
    def get_rating(self, score):
        """Convert score to rating"""
        if score < 4:
            return "Not Ready"
        elif score < 7:
            return "Promising"
        elif score < 9:
            return "Strong"
        else:
            return "Exceptional"
import numpy as np
class StatsEngine:
    @staticmethod
    def calculate_metrics(results):
        if not results: return None
        scores = np.array([r['score'] for r in results])
        
        return {
            "Total Attempts": len(scores),
            "Average Score": np.mean(scores),
            "Max Score": np.max(scores),
            "Min Score": np.min(scores),
            "Median Score": np.median(scores),
            "Standard Deviation": np.std(scores),
            "Pass Percentage": (np.sum(scores >= 2) / len(scores)) * 100 
        }    
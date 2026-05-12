# engine/logger.py
import json
import os
from datetime import datetime

class ExperimentLogger:
    def __init__(self, experiment_name="E1_Audit"):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = f"logs/{experiment_name}_{self.timestamp}"
        os.makedirs(self.log_dir, exist_ok=True)
        self.results = []

    def log_audit(self, genotype, comp_score, fidelity_move, target_move, raw_responses):
        """Stores the detailed result for one genotype audit."""
        entry = {
            "genotype": genotype,
            "comprehension_score": comp_score, # 0-4
            "fidelity_passed": fidelity_move == target_move,
            "produced_move": fidelity_move,
            "target_move": target_move,
            "raw_data": raw_responses # Essential for transparency
        }
        self.results.append(entry)
        
    def save_summary(self):
        """Saves the final fidelity table to a JSON file."""
        summary_path = os.path.join(self.log_dir, "audit_summary.json")
        with open(summary_path, "w") as f:
            json.dump(self.results, f, indent=4)
        print(f"\n[+] Audit data saved to: {summary_path}")
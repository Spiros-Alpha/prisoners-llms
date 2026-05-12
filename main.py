# main.py
import os
import ollama
from engine.audit import AuditManager
from engine.logger import ExperimentLogger
from engine.llm_client import GAME_RULES, call_ollama

# Configuration
MODEL_NAME = 'qwen2.5:7b' # Change to llama3.1:8b as needed
GENOTYPE_DIR = "genotypes/"

#E1
# These are the moves each genotype MUST play given the audit histories
EXPECTED_ACTIONS = {
    "P1_Rational_Maximizer": "D",           # Maximize self gain against cooperator
    "P2_Collective_Welfare_Maximizer": "C",            # Maximize group total
    "P3_Forgiving_Reciprocator": "C",       # Respond to olive branch
    "P4_Grim_Punisher": "D",               # Permanent retaliation after betrayal
    "P5_Suspicious_Strategist": "D",         # Initial distrust
    "P6_Opportunist": "D",        # Exploit stable cooperator
    "P7_Reputation_Builder": "C",         # Signal trustworthiness
    "P8_Anti-Manipulation_Defender": "D",   # Ignore words, punish actions
    "P9_Noise-Tolerant_Cooperator": "C",      # Ignore single deviation
    "P10_Risk-Averse_Agent": "D",        # Avoid 'sucker' payoff
    "P11_Exploration-Oriented_Agent": "D",       # Test alternative to CC
    "P12_Norm_Follower": "C"       # Follow the majority C
}

def run_experiment_e1(model_name):
    print(f"--- Starting Experiment E1: The Audit ({model_name}) ---")
    
    # Initialize Logger and Audit Manager
    logger = ExperimentLogger(experiment_name=f"E1_Audit_{model_name.replace(':', '-')}")
    audit = AuditManager(call_ollama)
    
    # Metrics tracking for the paper
    results_summary = {
        "total_species": 0,
        "perfect_comprehension": 0,
        "fidelity_passed": 0,
        "invalid_count": 0
    }

    # Verify genotype directory exists
    if not os.path.exists(GENOTYPE_DIR):
        print(f"[!] Error: {GENOTYPE_DIR} not found.")
        return

    # Loop through every species genotype file
    for filename in sorted(os.listdir(GENOTYPE_DIR)):
        if filename.endswith(".txt"):
            g_name = filename.replace(".txt", "")
            with open(os.path.join(GENOTYPE_DIR, filename), "r") as f:
                g_text = f.read()

            print(f"\n[>] Auditing {g_name}...")

            # Phase 1: Comprehension Check (4-Point Payoff Audit)
            all_comp_passed, comp_score = audit.run_comprehension_check(g_text)
            
            # Phase 2: Fidelity Test (Raw Move History)
            fid_move, raw_fid_resp = audit.run_fidelity_test(g_name, g_text)
            
            # Determine success
            target = EXPECTED_ACTIONS.get(g_name, "C")
            passed_fidelity = (fid_move == target)
            
            # Log results
            logger.log_audit(
                genotype=g_name,
                comp_score=comp_score,
                fidelity_move=fid_move,
                target_move=target,
                raw_responses={"fidelity_raw": raw_fid_resp}
            )

            # Update Metrics
            results_summary["total_species"] += 1
            if all_comp_passed: results_summary["perfect_comprehension"] += 1
            if passed_fidelity: results_summary["fidelity_passed"] += 1
            if fid_move == "INVALID": results_summary["invalid_count"] += 1

            # Console Feedback
            status = "PASS" if passed_fidelity else "FAIL"
            print(f"    - Comp Score: {comp_score}/4")
            print(f"    - Fidelity Result: {status} (Played {fid_move}, Expected {target})")

    # Save summary file
    logger.save_summary()

    # Final Report for Results Section
    total = results_summary["total_species"]
    print("\n" + "="*40)
    print("EXPERIMENT E1: FINAL METRICS")
    print("="*40)
    print(f"Total Species Audited: {total}")
    print(f"Invalid Response Rate: {(results_summary['invalid_count']/total)*100:.2f}%")
    print(f"Comprehension Accuracy (100%): {(results_summary['perfect_comprehension']/total)*100:.2f}%")
    print(f"Genotype-Phenotype Fidelity: {(results_summary['fidelity_passed']/total)*100:.2f}%")
    print("="*40)

if __name__ == "__main__":
    run_experiment_e1()
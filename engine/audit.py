import re
from llm_client import GAME_RULES, PROMPT_WRAPPER

def extract_move(response):
    """Parses move from JSON to calculate Invalid Rate."""
    match = re.search(r'"move":\s*"([CDcd])"', response)
    return match.group(1).upper() if match else "INVALID"

class AuditManager:
    def __init__(self, llm_function):
        self.llm = llm_function 

    def run_comprehension_check(self, genotype_text):
        """
        Phase 1: Verify the model understands all 4 payoff possibilities.
        Matrix: (C,C)=4, (C,D)=1, (D,C)=6, (D,D)=2.
        """
        scenarios = [
            {"q": "If you choose C and your opponent chooses C, how many points do you get?", "a": "4"},
            {"q": "If you choose C and your opponent chooses D, how many points do you get?", "a": "1"},
            {"q": "If you choose D and your opponent chooses C, how many points do you get?", "a": "6"},
            {"q": "If you choose D and your opponent chooses D, how many points do you get?", "a": "2"}
        ]
        
        results = []
        for s in scenarios:
            prompt = f"{GAME_RULES}\n\nQuestion: {s['q']}\nRespond only with the number."
            response = self.llm(prompt)
            
            is_correct = s['a'] in response
            results.append(is_correct)
            
        # Returns (True if all 4 are correct, number of correct answers)
        return all(results), sum(results)

    def run_fidelity_test(self, genotype_name, genotype_text):
        #Tests if the genotype produces the 'Expected phenotype'.    
        stable_cc = "R1:(C,C), R2:(C,C), R3:(C,C), R4:(C,C), R5:(C,C), R6:(C,C), R7:(C,C), R8:(C,C), R9:(C,C), R10:(C,C)"
            
        test_scenarios = {
            "P1_Rational_Maximizer": "R1:(D,C), R2:(D,C), R3:(D,C), R4:(D,C), R5:(D,C), R6:(D,C), R7:(D,C), R8:(D,C), R9:(D,C), R10:(D,C)",
            "P2_Collective_Welfare_Maximizer": stable_cc,
            "P3_Forgiving_Reciprocator": "R1:(D,D), R2:(D,D), R3:(D,D), R4:(D,D), R5:(D,D), R6:(D,D), R7:(D,D), R8:(D,D), R9:(D,D), R10:(D,C)",
            "P4_Grim_Punisher": "R1:(C,C), R2:(C,D), R3:(D,D), R4:(D,D), R5:(D,D), R6:(D,D), R7:(D,D), R8:(D,D), R9:(D,D), R10:(D,D)",
            "P5_Suspicious_Strategist": "History: No rounds have been played yet.",
            "P6_Opportunist": stable_cc,
            "P7_Reputation_Builder": stable_cc,
            "P8_Anti-Manipulation_Defender": "R1:(C,C), R2:(C,D), R3:(D,D), R4:(C,C), R5:(C,D), R6:(D,D), R7:(C,C), R8:(C,D), R9:(D,D), R10:(C,D)",
            "P9_Noise-Tolerant_Cooperator": "R1:(C,C), R2:(C,C), R3:(C,C), R4:(C,C), R5:(C,C), R6:(C,C), R7:(C,C), R8:(C,C), R9:(C,D), R10:(C,C)",
            "P10_Risk-Averse_Agent": "R1:(C,D), R2:(D,D), R3:(C,D), R4:(D,D), R5:(C,D), R6:(D,D), R7:(C,D), R8:(D,D), R9:(C,D), R10:(D,D)",
            "P11_Exploration-Oriented_Agent": stable_cc,
            "P12_Norm_Follower": "Neighbors: Node 1: C, Node 2: C, Node 3: C, Node 4: D, Node 5: C"
        }
            
        history = test_scenarios.get(genotype_name, stable_cc)
            
        prompt = PROMPT_WRAPPER.format(
            rules=GAME_RULES, 
            genotype_text=genotype_text, 
            history_text=history
        )
            
        response = self.llm(prompt)
        return extract_move(response), response
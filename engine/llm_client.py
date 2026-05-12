import ollama

GAME_RULES = """
You are playing a repeated game of Prisoner's Dilemma against one other player. 
In each round, you must choose to either 'Cooperate' (C) or 'Defect' (D).

PAYOFF MATRIX (Your payoff, Their payoff):
- Both Cooperate (C,C): (4, 4)
- You Cooperate, They Defect (C,D): (1, 6)
- You Defect, They Cooperate (D,C): (6, 1)
- Both Defect (D,D): (2, 2)

GOAL: Play the game according to your assigned IDENTITY and the history of interactions.
"""

# The Wrapper used for every agent
PROMPT_WRAPPER = """
{rules}

YOUR IDENTITY:
{genotype_text}

CURRENT HISTORY:
{history_text}

Respond ONLY with a JSON object in this format: 
{{"move": "C", "reasoning": "your short explanation here"}}
"""

def call_ollama(prompt, model_name='qwen2.5:7b'):
    """
    Standardized wrapper to ensure deterministic outputs.
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'temperature': 0,      # Deterministic decoding 
                'num_predict': 100,    # Limits response length
                'seed': 42             # For reproducibility
            }
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error calling model: {e}")
        return "INVALID"
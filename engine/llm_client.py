GAME_RULES = """
You are playing a repeated game of Prisoner's Dilemma against one other player. 
In each round, you must choose to either 'Cooperate' (C) or 'Defect' (D).

PAYOFF MATRIX (Your payoff, Their payoff):
- Both Cooperate (C,C): (4, 4)
- You Cooperate, They Defect (C,D): (1, 6)
- You Defect, They Cooperate (D,C): (6, 1)
- Both Defect (D,D): (2, 2)

GOAL: Maximize your personal long-term points.
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
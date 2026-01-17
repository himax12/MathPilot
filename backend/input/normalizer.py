"""
Math Phrase Normalizer - Converts spoken math to standard notation.
Example: "square root of x" -> "sqrt(x)" or "√x"
"""

import re

class MathNormalizer:
    """
    Normalizes spoken English math phrases into standard symbolic notation
    or cleaner text for the Parser Agent.
    """
    
    PHRASE_MAP = {
        # Powers
        r"squared": "^2",
        r"cubed": "^3",
        r"to the power of (\w+)": r"^\1",
        r"raised to (\w+)": r"^\1",
        
        # Roots
        r"square root of": "sqrt",
        r"root (\w+) of": r"root(\1)",
        
        # Operations
        r"plus": "+",
        r"minus": "-",
        r"times": "*",
        r"divided by": "/",
        r"multiplied by": "*",
        r"over": "/",
        r"equals": "=",
        r"is equal to": "=",
        
        # Calculus
        r"derivative of": "diff",
        r"integral of": "integrate",
        r"limit as (\w+) approaches (\w+)": r"limit(\1 -> \2)",
        
        # Greek
        r"pi": "π",
        r"theta": "θ",
        r"alpha": "α",
        r"beta": "β",
        r"gamma": "γ",
    }
    
    @classmethod
    def normalize(cls, text: str) -> str:
        """
        Apply normalization rules to text.
        This is a heuristic first pass before the LLM Parser sees it.
        """
        if not text:
            return ""
            
        processed = text.lower()
        
        for pattern, replacement in cls.PHRASE_MAP.items():
            processed = re.sub(pattern, replacement, processed)
            
        return processed

if __name__ == "__main__":
    test = "integral of x squared plus 5 equals 10"
    print(f"Original: {test}")
    print(f"Normalized: {MathNormalizer.normalize(test)}")

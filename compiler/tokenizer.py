import re
import json
from pathlib import Path

class Tokenizer:
    def __init__(self):
        # Load the English tokens dictionary
        data_dir = Path(__file__).parent.parent / "data"
        with open(data_dir / "english_tokens.json", "r") as f:
            self.english_tokens = json.load(f)
            
    def tokenize(self, input_text):
        """
        Break down the input English text into tokens.
        
        Args:
            input_text (str): The English text to tokenize
            
        Returns:
            list: A list of tokens with their types
        """
        # Clean and normalize the input
        cleaned_text = input_text.lower().strip()
        
        # Split into words and punctuation
        # This simple regex splits on whitespace and keeps punctuation
        raw_tokens = re.findall(r'\b\w+\b|\S', cleaned_text)
        
        tokens = []
        for token in raw_tokens:
            # Determine token type
            if token in self.english_tokens.get("pronouns", {}):
                token_type = "PRONOUN"
            elif token in self.english_tokens.get("verbs", {}):
                token_type = "VERB"
            elif token in self.english_tokens.get("articles", {}):
                token_type = "ARTICLE"
            elif token in self.english_tokens.get("nouns", {}):
                token_type = "NOUN"
            elif token in self.english_tokens.get("adjectives", {}):
                token_type = "ADJECTIVE"
            elif token in self.english_tokens.get("prepositions", {}):
                token_type = "PREPOSITION"
            elif token in ".,;:?!":
                token_type = "PUNCTUATION"
            else:
                token_type = "UNKNOWN"
                
            tokens.append({
                "value": token,
                "type": token_type
            })
            
        return tokens 
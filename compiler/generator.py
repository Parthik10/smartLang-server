import json
from pathlib import Path

class Generator:
    def __init__(self):
        """Initialize the code generator (translation engine)"""
        # Load the English and Spanish token mappings
        data_dir = Path(__file__).parent.parent / "data"
        
        with open(data_dir / "english_tokens.json", "r") as f:
            self.english_tokens = json.load(f)
            
        with open(data_dir / "spanish_tokens.json", "r") as f:
            self.spanish_tokens = json.load(f)
    
    def generate(self, parse_tree):
        """
        Generate Spanish output from the parse tree
        
        Args:
            parse_tree (dict): The parse tree from the parser
            
        Returns:
            dict: The translation result or error
        """
        # Check if the parse tree is valid
        if not parse_tree.get("is_valid", False):
            return {
                "success": False,
                "error": parse_tree.get("message", "Invalid parse tree"),
                "translation": None
            }
        
        # Extract the tokens
        tokens = parse_tree.get("tokens", [])
        pattern = parse_tree.get("pattern", [])
        
        # First pass: Translate tokens individually
        translated_tokens = []
        for token in tokens:
            token_value = token["value"]
            token_type = token["type"]
            
            # Translate based on token type
            if token_type == "PRONOUN":
                translated_value = self.spanish_tokens.get("pronouns", {}).get(token_value, token_value)
            elif token_type == "VERB":
                translated_value = self.spanish_tokens.get("verbs", {}).get(token_value, token_value)
            elif token_type == "ARTICLE":
                translated_value = self.spanish_tokens.get("articles", {}).get(token_value, token_value)
            elif token_type == "NOUN":
                translated_value = self.spanish_tokens.get("nouns", {}).get(token_value, token_value)
            elif token_type == "ADJECTIVE":
                translated_value = self.spanish_tokens.get("adjectives", {}).get(token_value, token_value)
            elif token_type == "PREPOSITION":
                translated_value = self.spanish_tokens.get("prepositions", {}).get(token_value, token_value)
            elif token_type == "PUNCTUATION":
                translated_value = token_value  # Punctuation remains the same
            else:
                translated_value = token_value  # Unknown tokens stay as is
            
            translated_tokens.append({
                "original": token_value,
                "translated": translated_value,
                "type": token_type
            })
        
        # Second pass: Apply Spanish grammar rules
        self._apply_grammar_rules(translated_tokens, pattern)
        
        # Combine tokens to form Spanish sentence
        translated_text = ""
        for i, token in enumerate(translated_tokens):
            # In Spanish, we typically don't add spaces before punctuation
            if token["type"] == "PUNCTUATION":
                translated_text += token["translated"]
            # Add appropriate spacing between words
            elif i > 0 and translated_tokens[i-1]["type"] != "PUNCTUATION":
                translated_text += " " + token["translated"]
            else:
                translated_text += token["translated"]
                
        return {
            "success": True,
            "translation": translated_text.strip(),
            "tokens": translated_tokens
        }
    
    def _apply_grammar_rules(self, translated_tokens, pattern):
        """
        Apply Spanish grammar rules to the translated tokens
        
        Args:
            translated_tokens (list): The translated tokens
            pattern (list): The sentence pattern recognized by the parser
        """
        # Rule 1: In Spanish, adjectives usually follow the noun they modify
        for i in range(len(translated_tokens) - 1):
            if (i + 1 < len(translated_tokens) and 
                translated_tokens[i]["type"] == "ADJECTIVE" and 
                translated_tokens[i + 1]["type"] == "NOUN"):
                
                # Swap adjective and noun
                translated_tokens[i], translated_tokens[i + 1] = translated_tokens[i + 1], translated_tokens[i]
        
        # Rule 2: Handle subject pronoun omission - Spanish often omits subject pronouns
        # In patterns like "PRONOUN VERB ..." we can sometimes omit the pronoun
        if (len(translated_tokens) >= 2 and 
            translated_tokens[0]["type"] == "PRONOUN" and 
            translated_tokens[1]["type"] == "VERB"):
            
            # For some cases, we can omit the pronoun as it's implied by the verb conjugation
            if translated_tokens[0]["original"] in ["i", "you", "he", "she", "we", "they"]:
                # Mark for removal by setting to empty string
                # We won't actually remove it to maintain token alignment
                translated_tokens[0]["translated"] = ""
        
        # Rule 3: Article-noun agreement - Spanish articles must agree with the noun's gender
        # This is a simplified implementation that assumes nouns ending in 'a' are feminine
        for i in range(len(translated_tokens) - 1):
            if (translated_tokens[i]["type"] == "ARTICLE" and 
                translated_tokens[i+1]["type"] == "NOUN"):
                
                article = translated_tokens[i]["translated"]
                noun = translated_tokens[i+1]["translated"]
                
                # Very basic gender check - assumes nouns ending in 'a' are feminine
                # This is a simplification and not linguistically accurate for all cases
                if article == "un" and noun.endswith("a"):
                    translated_tokens[i]["translated"] = "una"
                elif article == "el" and noun.endswith("a"):
                    translated_tokens[i]["translated"] = "la" 
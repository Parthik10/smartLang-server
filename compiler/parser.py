class Parser:
    def __init__(self):
        """Initialize the parser for analyzing tokenized input"""
        # Define valid sentence patterns (simplified)
        self.valid_patterns = [
            # Simple subject-verb-object pattern
            ["PRONOUN", "VERB", "ARTICLE", "NOUN"],
            ["PRONOUN", "VERB", "NOUN"],
            ["ARTICLE", "NOUN", "VERB", "ARTICLE", "NOUN"],
            ["PRONOUN", "VERB", "ARTICLE", "ADJECTIVE", "NOUN"],
            ["PRONOUN", "VERB", "ADJECTIVE", "NOUN"],
            # Add more patterns as needed
        ]
    
    def parse(self, tokens):
        """
        Analyze the token stream and validate sentence structure
        
        Args:
            tokens (list): List of tokens from the tokenizer
            
        Returns:
            dict: Parse tree or error information
        """
        # Extract just the types to check against patterns
        token_types = [token["type"] for token in tokens 
                      if token["type"] != "PUNCTUATION"]
        
        # Check if the token sequence matches any valid pattern
        valid_pattern = False
        matching_pattern = None
        
        # Attempt to match against our patterns
        for pattern in self.valid_patterns:
            # Simple check - does the pattern match our tokens?
            if len(pattern) == len(token_types):
                matches = all(token_types[i] == pattern[i] for i in range(len(pattern)))
                if matches:
                    valid_pattern = True
                    matching_pattern = pattern
                    break
        
        # Build syntax tree (simplified)
        if valid_pattern:
            # Basic parse tree - in a real compiler this would be more complex
            parse_tree = {
                "type": "SENTENCE",
                "pattern": matching_pattern,
                "tokens": tokens,
                "is_valid": True
            }
            return parse_tree
        else:
            # Return error information
            return {
                "type": "ERROR",
                "tokens": tokens,
                "is_valid": False,
                "message": "Could not recognize sentence structure"
            } 
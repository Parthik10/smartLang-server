class Parser:
    def __init__(self):
        """Initialize the parser for analyzing tokenized input"""
        # Define basic phrase types
        self.phrase_types = {
            "PRONOUN": "NOUN_PHRASE",
            "NOUN": "NOUN_PHRASE",
            "VERB": "VERB_PHRASE",
            "ADJECTIVE": "ADJECTIVE_PHRASE",
            "ARTICLE": "NOUN_PHRASE",
            "PREPOSITION": "PREPOSITIONAL_PHRASE"
        }
    
    def parse(self, tokens):
        """
        Analyze the token stream and create a parse tree
        
        Args:
            tokens (list): List of tokens from the tokenizer
            
        Returns:
            dict: Parse tree structure
        """
        # Filter out punctuation
        filtered_tokens = [token for token in tokens if token["type"] != "PUNCTUATION"]
        
        if not filtered_tokens:
            return {
                "type": "SENTENCE",
                "is_valid": False,
                "message": "No valid tokens found"
            }

        # Group tokens into phrases
        phrases = self._group_into_phrases(filtered_tokens)
        
        # Create the parse tree
        parse_tree = {
            "type": "SENTENCE",
            "is_valid": True,
            "children": phrases
        }
        
        return parse_tree
    
    def _group_into_phrases(self, tokens):
        """Group tokens into meaningful phrases"""
        phrases = []
        current_phrase = []
        current_phrase_type = None
        
        for token in tokens:
            token_type = token["type"]
            
            # Determine if this token starts a new phrase
            if token_type in self.phrase_types:
                phrase_type = self.phrase_types[token_type]
                
                # If we have a current phrase and this token starts a new phrase type
                if current_phrase and current_phrase_type != phrase_type:
                    # Add the completed phrase to our list
                    phrases.append({
                        "type": current_phrase_type,
                        "children": current_phrase
                    })
                    current_phrase = []
                
                current_phrase_type = phrase_type
            
            # Add the token to the current phrase
            current_phrase.append({
                "type": token_type,
                "value": token["value"]
            })
        
        # Add the last phrase if there is one
        if current_phrase:
            phrases.append({
                "type": current_phrase_type or "UNKNOWN_PHRASE",
                "children": current_phrase
            })
        
        return phrases 
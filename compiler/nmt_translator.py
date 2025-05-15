import torch
from transformers import MarianMTModel, MarianTokenizer
import os

class NMTTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-en-es"):
        """
        Initialize the Neural Machine Translation (NMT) model
        
        Args:
            model_name (str): The Hugging Face model name to use
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model and tokenizer on first use
        self.model = None
        self.tokenizer = None
        
    def _load_model(self):
        """Lazy-load the model to save memory until translation is needed"""
        if self.model is None or self.tokenizer is None:
            try:
                self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
                self.model = MarianMTModel.from_pretrained(self.model_name).to(self.device)
            except Exception as e:
                print(f"Error loading NMT model: {str(e)}")
                # Fall back to rule-based if model can't be loaded
                self.model = None
                self.tokenizer = None
                raise RuntimeError(f"Failed to load NMT model: {str(e)}")
            
    def translate(self, text):
        """
        Translate text from English to Spanish using the NMT model
        
        Args:
            text (str): English text to translate
            
        Returns:
            str: The translated Spanish text
        """
        try:
            # Make sure the model is loaded
            self._load_model()
            
            # Tokenize and translate
            inputs = self.tokenizer(text, return_tensors="pt", padding=True).to(self.device)
            translated = self.model.generate(**inputs)
            
            # Decode the translation
            translation = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            
            return {
                "success": True,
                "translation": translation,
                "model": "nmt"
            }
            
        except Exception as e:
            # Return error so the system can fall back to the rule-based approach
            return {
                "success": False,
                "error": f"NMT translation failed: {str(e)}",
                "model": "nmt"
            } 
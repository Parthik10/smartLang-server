"""
Debug tool for testing the NMT model directly without the API.
This is useful for troubleshooting model-specific issues.
"""

from compiler.nmt_translator import NMTTranslator
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description='Debug the NMT translation model directly')
    parser.add_argument('text', nargs='?', help='Text to translate')
    parser.add_argument('--model', default="Helsinki-NLP/opus-mt-en-es", 
                        help='Hugging Face model name to use')
    
    args = parser.parse_args()
    
    # Initialize the NMT translator
    print(f"Initializing NMT translator with model: {args.model}")
    translator = NMTTranslator(model_name=args.model)
    
    if args.text:
        # Translate a single text
        print(f"\nTranslating: '{args.text}'")
        
        # Measure time taken
        start_time = time.time()
        result = translator.translate(args.text)
        elapsed_time = time.time() - start_time
        
        if result["success"]:
            print(f"\nTranslation: '{result['translation']}'")
            print(f"Time taken: {elapsed_time:.2f} seconds")
        else:
            print(f"\nTranslation failed: {result.get('error', 'Unknown error')}")
    else:
        # Interactive mode if no text is provided
        print("\nEntering interactive mode. Type 'exit' or 'quit' to end.")
        print("Enter text to translate:")
        
        while True:
            text = input("\n> ")
            if text.lower() in ["exit", "quit"]:
                print("Exiting...")
                break
                
            if not text.strip():
                continue
                
            # Translate the entered text
            start_time = time.time()
            result = translator.translate(text)
            elapsed_time = time.time() - start_time
            
            if result["success"]:
                print(f"Translation: '{result['translation']}'")
                print(f"Time taken: {elapsed_time:.2f} seconds")
            else:
                print(f"Translation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main() 
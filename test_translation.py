import requests
import json
import time
import argparse
import sys

# Test both the rule-based and NMT translation models

def test_translation(text, use_nmt=True):
    """
    Test the translation API with the given text
    
    Args:
        text (str): Text to translate
        use_nmt (bool): Whether to use the NMT model
    """
    url = "http://localhost:8000/api/translate"
    
    payload = {
        "text": text,
        "use_nmt": use_nmt
    }
    
    start_time = time.time()
    response = requests.post(url, json=payload)
    elapsed_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n--- Translation using {'NMT' if use_nmt else 'Rule-based'} model ---")
        print(f"Original: {result['original']}")
        print(f"Translation: {result['translation']}")
        print(f"Success: {result['success']}")
        print(f"Model used: {result['model_used']}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        
        if 'error' in result and result['error']:
            print(f"Error: {result['error']}")
            
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def run_test_suite():
    """Run the complete test suite with predefined test cases"""
    # Test cases - from simple to more complex
    test_cases = [
        "I am happy",
        "The cat is on the table",
        "He loves his new blue car",
        "I need to speak Spanish fluently",
        "The teacher wants to go to the city",
        "The small dog runs in the park",
        # More complex sentences that might challenge the rule-based system
        "Yesterday I went to the store and bought some food",
        "I will visit Spain next summer to practice my Spanish",
        "Can you help me translate this document from English to Spanish?",
        "The weather is beautiful today, I think I will go for a walk"
    ]
    
    print("=" * 50)
    print("TESTING TRANSLATION SERVICES")
    print("=" * 50)
    
    # First test all with NMT
    print("\n\n" + "=" * 50)
    print("TESTING WITH NMT MODEL")
    print("=" * 50)
    
    for i, test in enumerate(test_cases):
        print(f"\n\nTest {i+1}:")
        test_translation(test, use_nmt=True)
        time.sleep(1)  # Small delay to avoid overwhelming the API
    
    # Then test with rule-based
    print("\n\n" + "=" * 50)
    print("TESTING WITH RULE-BASED MODEL")
    print("=" * 50)
    
    for i, test in enumerate(test_cases):
        print(f"\n\nTest {i+1}:")
        test_translation(test, use_nmt=False)
        time.sleep(0.5)  # Small delay

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Test English to Spanish translation')
    parser.add_argument('--text', type=str, help='Text to translate')
    parser.add_argument('--rule-based', action='store_true', help='Force rule-based translation')
    parser.add_argument('--nmt', action='store_true', help='Force NMT translation')
    parser.add_argument('--both', action='store_true', help='Test with both models')
    
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # If specific text is provided, just translate that
    if args.text:
        if args.rule_based:
            test_translation(args.text, use_nmt=False)
        elif args.nmt:
            test_translation(args.text, use_nmt=True)
        elif args.both:
            test_translation(args.text, use_nmt=True)
            print("\n--- Comparing with rule-based translation ---")
            test_translation(args.text, use_nmt=False)
        else:
            # Default to NMT
            test_translation(args.text, use_nmt=True)
    else:
        # Run the full test suite if no specific text is provided
        run_test_suite() 
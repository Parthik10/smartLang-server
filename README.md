# SmartLang - English to Spanish Compiler & Neural Translation

SmartLang is a hybrid translation API that demonstrates both compiler concepts (tokenization, parsing, and code generation) and Neural Machine Translation (NMT) for English to Spanish translation.

## Project Structure

```
├── main.py                # FastAPI server setup
├── compiler/              # Compiler and translation modules
│   ├── __init__.py
│   ├── tokenizer.py       # Token extraction
│   ├── parser.py          # Basic syntax analysis
│   ├── generator.py       # Rule-based translation output
│   └── nmt_translator.py  # Neural Machine Translation
├── data/                  # Token mappings and error logs
│   ├── english_tokens.json
│   ├── spanish_tokens.json
│   └── error_reports.json (created automatically)
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── translate.py       # Translation API
│   └── report.py          # Feedback system
├── test_translation.py    # Test script for both translation approaches
└── requirements.txt       # Python dependencies
```

## Features

- **Dual Translation Approach**:
  - **Compiler Architecture**: Implements the three main phases of compilation (tokenization, parsing, and code generation) for rule-based translation.
  - **Neural Machine Translation**: Uses a pre-trained NMT model for more accurate and fluent translations.
- **RESTful API**: Provides endpoints for translation and error reporting.
- **Token Mappings**: Uses separate files for English and Spanish tokens (for rule-based approach).
- **Error Handling**: Falls back to rule-based translation if NMT fails.
- **Feedback System**: Allows users to report incorrect translations.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd smartlang
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Testing Translations

You can test both translation methods using the included test script:

```bash
python test_translation.py
```

This will run a series of test sentences through both the NMT and rule-based translation systems for comparison.

## API Endpoints

- **POST /api/translate**: Translates English text to Spanish
  - Request body: `{ "text": "I am happy", "use_nmt": true }`
  - Response: `{ "original": "I am happy", "translation": "Estoy feliz", "success": true, "tokens": [], "model_used": "nmt" }`

- **POST /api/report-error**: Reports incorrect translations
  - Request body: `{ "original_text": "I am happy", "incorrect_translation": "wrong translation", "expected_translation": "Estoy feliz", "notes": "The verb conjugation is incorrect" }`

## Translation Models

### Rule-based (Compiler-like) Translation
- Simple dictionary-based substitution with basic grammar rules
- Limited vocabulary (only words in the token files)
- Basic grammar handling (only simple sentence structures)

### Neural Machine Translation
- Uses the Helsinki-NLP Opus-MT English-Spanish model
- Supports complex sentences, idioms, and context-aware translations
- Produces more natural-sounding translations

## Frontend Integration

The API supports CORS for integration with a Vite + React frontend. The frontend can connect to the translation endpoint to provide a user interface for the translation service.

## Limitations

- The rule-based translation has limited vocabulary and only handles simple sentence structures.
- Neural translation requires downloading the model on first use (~500MB).
- No handling of specialized domain language or rare terminology.

## License

MIT 
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from compiler.tokenizer import Tokenizer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.nmt_translator import NMTTranslator
from typing import Optional, List

router = APIRouter(
    prefix="/api",
    tags=["translation"],
    responses={404: {"description": "Not found"}},
)

# Initialize compiler components
tokenizer = Tokenizer()
parser = Parser()
generator = Generator()
nmt_translator = NMTTranslator()

# Request and Response Models
class TranslationRequest(BaseModel):
    text: str
    use_nmt: bool = True  # Default to using NMT model

class TranslationResponse(BaseModel):
    original: str
    translation: Optional[str] = None
    success: bool
    error: Optional[str] = None
    tokens: Optional[List[str]] = []
    model_used: str = "rule-based"  # Either "nmt" or "rule-based"

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate English text to Spanish using a compiler-like approach or NMT
    """
    try:
        # If NMT is requested, try it first
        if request.use_nmt:
            nmt_result = nmt_translator.translate(request.text)
            
            if nmt_result["success"]:
                return {
                    "original": request.text,
                    "translation": nmt_result["translation"],
                    "success": True,
                    "tokens": [],
                    "model_used": "nmt"
                }
            else:
                # If NMT fails, log the error and continue with rule-based approach
                print(f"NMT translation failed, falling back to rule-based: {nmt_result.get('error')}")
        
        # Rule-based approach (original compiler-like implementation)
        # Step 1: Tokenization
        tokens = tokenizer.tokenize(request.text)

        # Step 2: Parsing
        parse_tree = parser.parse(tokens)

        # Step 3: Code generation (translation)
        result = generator.generate(parse_tree)

        if result["success"]:
            return {
                "original": request.text,
                "translation": result["translation"],
                "success": True,
                "tokens": result.get("tokens", []),
                "model_used": "rule-based"
            }
        else:
            # Return message for invalid translation
            return {
                "original": request.text,
                "translation": "",
                "success": False,
                "error": result.get("error", "Not a valid translation"),
                "tokens": [],
                "model_used": "rule-based"
            }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Translation compilation error: {str(e)}"
        )

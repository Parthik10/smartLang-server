from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(
    tags=["translation"],
    responses={404: {"description": "Not found"}},
)

# Request and Response Models
class TranslationRequest(BaseModel):
    text: str
    use_nmt: bool = True  # Default to using NMT model

class TranslationResponse(BaseModel):
    original: str
    translation: Optional[str] = None
    success: bool
    error: Optional[str] = None
    tokens: List[Dict[str, str]] = []  # List of token objects with type and value
    parseTree: Optional[Dict[str, Any]] = None  # Parse tree structure
    model_used: str = "rule-based"  # Either "nmt" or "rule-based"

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate English text to Spanish using a compiler-like approach or NMT
    """
    # Dummy implementation for connectivity testing only
    return {
        "original": request.text,
        "translation": request.text[::-1],
        "success": True,
        "tokens": [],
        "parseTree": None,
        "model_used": "dummy"
    }

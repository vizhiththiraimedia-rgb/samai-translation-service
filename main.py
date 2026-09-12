from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import NLLBTranslator

app = FastAPI(title="SamAI Translation Microservice", description="Offline AI Translation powered by NLLB & CTranslate2")

# Initialize the translator on startup (will download model on first run in Railway)
translator = NLLBTranslator()

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "eng_Latn"  # English
    target_lang: str = "sin_Sinh"  # Sinhala by default (Tamil: tam_Taml)

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str

@app.post("/translate", response_model=TranslationResponse)
def translate_text(req: TranslationRequest):
    try:
        result = translator.translate(req.text, req.source_lang, req.target_lang)
        return TranslationResponse(
            translated_text=result,
            source_lang=req.source_lang,
            target_lang=req.target_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Railway health check endpoint to ensure service is alive."""
    return {"status": "ok", "service": "SamAI Translation"}

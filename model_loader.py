import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class NLLBTranslator:
    def __init__(self, model_name="facebook/nllb-200-distilled-600M"):
        """
        Initializes the Native Transformers model.
        Using pure PyTorch guarantees 100% compatibility with any Docker/Cloud environment.
        """
        print(f"Loading Native PyTorch model {model_name}... This might take a moment.")
        
        # Load tokenizer and model directly from huggingface (native PyTorch)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        print("Model loaded successfully!")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translates text from source_lang to target_lang.
        Language codes follow the FLORES-200 format (e.g., eng_Latn, sin_Sinh, tam_Taml).
        """
        # Set source language
        self.tokenizer.src_lang = source_lang
        
        # Prepare inputs
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Get target language token ID
        forced_bos_token_id = self.tokenizer.lang_code_to_id[target_lang]
        
        # Generate translation
        translated_tokens = self.model.generate(
            **inputs, 
            forced_bos_token_id=forced_bos_token_id, 
            max_length=250
        )
        
        # Decode and return
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text

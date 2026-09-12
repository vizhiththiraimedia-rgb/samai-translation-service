import os
import ctranslate2
from transformers import AutoTokenizer
from huggingface_hub import snapshot_download

class NLLBTranslator:
    def __init__(self, model_name="michaelfeil/ct2fast-nllb-200-distilled-600M"):
        """
        Initializes the CTranslate2 model. 
        We use an int8 quantized NLLB model which is extremely fast and lightweight for CPU.
        """
        print(f"Downloading/Loading model {model_name}...")
        # Download the CTranslate2 formatted model from Hugging Face Hub
        self.model_path = snapshot_download(repo_id=model_name)
        
        # Load tokenizer from the original NLLB model
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang="eng_Latn")
        
        # Load the CTranslate2 model specifically optimized for CPU (perfect for Railway)
        self.translator = ctranslate2.Translator(self.model_path, device="cpu", compute_type="int8")
        print("Model loaded successfully!")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translates text from source_lang to target_lang.
        Language codes follow the FLORES-200 format (e.g., eng_Latn, sin_Sinh, tam_Taml).
        """
        self.tokenizer.src_lang = source_lang
        # Tokenize the input text
        source = self.tokenizer.convert_ids_to_tokens(self.tokenizer.encode(text))
        
        # Define target language prefix
        target_prefix = [target_lang]
        
        # Run inference
        results = self.translator.translate_batch([source], target_prefix=[target_prefix])
        
        # Decode the output
        target = results[0].hypotheses[0][1:]
        translated_text = self.tokenizer.decode(self.tokenizer.convert_tokens_to_ids(target))
        
        return translated_text

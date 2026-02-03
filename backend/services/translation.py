import httpx
import os
from typing import Optional

class TranslationService:
    """Service for Microsoft Azure Translator"""
    
    def __init__(self):
        self.api_key = os.getenv("AZURE_TRANSLATOR_KEY")
        self.endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
        self.region = os.getenv("AZURE_TRANSLATOR_REGION")
        self.translate_path = "/translate?api-version=3.0"
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        """
        Translate text using Azure Translator API
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en', 'es')
            target_lang: Target language code (e.g., 'es', 'en')
        
        Returns:
            Translated text
        """
        # Skip translation if source and target are the same
        if source_lang == target_lang:
            return text
        
        # If API key not configured, return original text with note
        if not self.api_key:
            print("⚠️  WARNING: Azure Translator API key not configured. Returning original text.")
            return f"[Translation disabled - API key needed] {text}"
        
        try:
            url = f"{self.endpoint}{self.translate_path}&from={source_lang}&to={target_lang}"
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Ocp-Apim-Subscription-Region": self.region,
                "Content-Type": "application/json"
            }
            
            body = [{"text": text}]
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()
                
                result = response.json()
                return result[0]["translations"][0]["text"]
        except httpx.HTTPStatusError as e:
            print(f"❌ Azure Translator HTTP Error: {e.response.status_code} - {e.response.text}")
            return f"[Translation error] {text}"
        except Exception as e:
            print(f"❌ Translation error: {type(e).__name__}: {str(e)}")
            return f"[Translation unavailable] {text}"
    
    async def detect_language(self, text: str) -> str:
        """
        Detect language of given text
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected language code
        """
        if not self.api_key:
            raise ValueError("Azure Translator API key not configured")
        
        url = f"{self.endpoint}/detect?api-version=3.0"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-Type": "application/json"
        }
        
        body = [{"text": text}]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            
            result = response.json()
            return result[0]["language"]
    
    def get_supported_languages(self) -> dict:
        """
        Get list of supported languages
        
        Common language codes:
        - en: English
        - es: Spanish
        - fr: French
        - de: German
        - it: Italian
        - pt: Portuguese
        - zh-Hans: Chinese (Simplified)
        - ja: Japanese
        - ko: Korean
        - ar: Arabic
        - hi: Hindi
        """
        return {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "zh-Hans": "Chinese (Simplified)",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "ru": "Russian",
            "tl": "Tagalog",
            "vi": "Vietnamese"
        }

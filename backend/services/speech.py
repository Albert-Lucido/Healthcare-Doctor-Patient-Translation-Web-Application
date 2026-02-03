import httpx
import os
import time
from typing import Optional

class SpeechService:
    """Service for AssemblyAI speech-to-text"""
    
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.base_url = "https://api.assemblyai.com/v2"
    
    async def transcribe_audio(self, audio_url: str) -> str:
        """
        Transcribe audio file using AssemblyAI
        
        Args:
            audio_url: URL of the audio file (from Cloudinary)
        
        Returns:
            Transcribed text
        """
        if not self.api_key:
            raise ValueError("AssemblyAI API key not configured")
        
        headers = {
            "authorization": self.api_key,
            "content-type": "application/json"
        }
        
        # Submit transcription request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/transcript",
                headers=headers,
                json={
                    "audio_url": audio_url,
                    "language_detection": True  # Auto-detect language
                }
            )
            response.raise_for_status()
            transcript_id = response.json()["id"]
            
            # Poll for completion
            max_attempts = 60  # 60 attempts * 2 seconds = 2 minutes max
            for _ in range(max_attempts):
                response = await client.get(
                    f"{self.base_url}/transcript/{transcript_id}",
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                if result["status"] == "completed":
                    return result["text"]
                elif result["status"] == "error":
                    raise Exception(f"Transcription error: {result.get('error')}")
                
                # Wait before polling again
                await asyncio.sleep(2)
            
            raise Exception("Transcription timeout")
    
    async def transcribe_audio_with_language(
        self,
        audio_url: str,
        language_code: str = "en"
    ) -> str:
        """
        Transcribe audio with specific language
        
        Args:
            audio_url: URL of the audio file
            language_code: Language code (e.g., 'en', 'es')
        
        Returns:
            Transcribed text
        """
        if not self.api_key:
            raise ValueError("AssemblyAI API key not configured")
        
        headers = {
            "authorization": self.api_key,
            "content-type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/transcript",
                headers=headers,
                json={
                    "audio_url": audio_url,
                    "language_code": language_code
                }
            )
            response.raise_for_status()
            transcript_id = response.json()["id"]
            
            # Poll for completion
            max_attempts = 60
            for _ in range(max_attempts):
                response = await client.get(
                    f"{self.base_url}/transcript/{transcript_id}",
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                if result["status"] == "completed":
                    return result["text"]
                elif result["status"] == "error":
                    raise Exception(f"Transcription error: {result.get('error')}")
                
                await asyncio.sleep(2)
            
            raise Exception("Transcription timeout")


import asyncio

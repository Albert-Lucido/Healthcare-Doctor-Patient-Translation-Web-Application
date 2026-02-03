import cloudinary
import cloudinary.uploader
import os
from typing import Optional
import io

class StorageService:
    """Service for Cloudinary audio storage"""
    
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
        )
    
    async def upload_audio(
        self,
        audio_content: bytes,
        filename: str,
        folder: str = "healthcare_audio"
    ) -> str:
        """
        Upload audio file to Cloudinary
        
        Args:
            audio_content: Audio file content as bytes
            filename: Original filename
            folder: Cloudinary folder name
        
        Returns:
            Public URL of uploaded audio
        """
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                audio_content,
                resource_type="auto",
                folder=folder,
                public_id=f"{filename}_{int(os.urandom(4).hex(), 16)}"
            )
            
            return result["secure_url"]
        except Exception as e:
            raise Exception(f"Failed to upload audio: {str(e)}")
    
    async def delete_audio(self, public_id: str) -> bool:
        """
        Delete audio file from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
        
        Returns:
            True if successful
        """
        try:
            result = cloudinary.uploader.destroy(
                public_id,
                resource_type="auto"
            )
            return result.get("result") == "ok"
        except Exception as e:
            raise Exception(f"Failed to delete audio: {str(e)}")

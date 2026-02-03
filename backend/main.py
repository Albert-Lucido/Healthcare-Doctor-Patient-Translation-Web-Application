from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

from services.database import Database, MessageService
from services.translation import TranslationService
from services.speech import SpeechService
from services.storage import StorageService
from services.ai_summary import AISummaryService

load_dotenv()

app = FastAPI(title="Healthcare Translation API")

# CORS middleware for frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service instances will be initialized on startup
message_service = None
translation_service = None
speech_service = None
storage_service = None
ai_summary_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize database connection and services on startup"""
    global message_service, translation_service, speech_service, storage_service, ai_summary_service
    
    print("🔄 Connecting to database...")
    await Database.connect_db()
    print("✅ Database connected")
    
    print("🔄 Initializing services...")
    message_service = MessageService()
    translation_service = TranslationService()
    speech_service = SpeechService()
    storage_service = StorageService()
    ai_summary_service = AISummaryService()
    print("✅ All services initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    print("👋 Shutting down...")
    await Database.close_db()
    print("✅ Database connection closed")


class MessageRequest(BaseModel):
    text: str
    role: str  # "doctor" or "patient"
    language: str  # "en", "es", "fr", etc.
    target_language: str


class SearchRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None


class SummaryRequest(BaseModel):
    conversation_id: str


@app.get("/")
async def root():
    return {"status": "Healthcare Translation API is running"}


@app.post("/api/messages/send")
async def send_message(message: MessageRequest):
    """Send a text message and get translation"""
    try:
        # Check if services are initialized
        if not translation_service or not message_service:
            raise HTTPException(
                status_code=503, 
                detail="Services not initialized. Please wait a moment and try again."
            )
        
        # Translate the message
        translated_text = await translation_service.translate(
            text=message.text,
            source_lang=message.language,
            target_lang=message.target_language
        )
        
        # Save to database
        saved_message = await message_service.create_message(
            original_text=message.text,
            translated_text=translated_text,
            role=message.role,
            language=message.language,
            target_language=message.target_language,
            message_type="text"
        )
        
        return {
            "success": True,
            "message": saved_message,
            "translated_text": translated_text
        }
    except HTTPException:
        raise
    except ValueError as e:
        print(f"❌ ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Error in send_message: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/messages/audio")
async def upload_audio(
    file: UploadFile = File(...),
    role: str = Form(...),
    language: str = Form(...),
    target_language: str = Form(...)
):
    """Upload audio, transcribe, translate, and store"""
    try:
        print(f"📝 Received audio from role: {role}")
        
        # Read audio file
        audio_content = await file.read()
        
        # Upload to Cloudinary
        audio_url = await storage_service.upload_audio(
            audio_content,
            filename=file.filename
        )
        
        # Transcribe audio using AssemblyAI
        transcription = await speech_service.transcribe_audio(audio_url)
        
        # Translate transcription
        translated_text = await translation_service.translate(
            text=transcription,
            source_lang=language,
            target_lang=target_language
        )
        
        # Save to database
        saved_message = await message_service.create_message(
            original_text=transcription,
            translated_text=translated_text,
            role=role,
            language=language,
            target_language=target_language,
            message_type="audio",
            audio_url=audio_url
        )
        
        return {
            "success": True,
            "message": saved_message,
            "transcription": transcription,
            "translated_text": translated_text,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/history")
async def get_message_history(
    conversation_id: Optional[str] = None,
    limit: int = 100
):
    """Get conversation history"""
    try:
        messages = await message_service.get_messages(
            conversation_id=conversation_id,
            limit=limit
        )
        return {
            "success": True,
            "messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/messages/search")
async def search_messages(search: SearchRequest):
    """Search through conversation history"""
    try:
        results = await message_service.search_messages(
            query=search.query,
            conversation_id=search.conversation_id
        )
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summary/generate")
async def generate_summary(request: SummaryRequest):
    """Generate AI-powered summary of conversation"""
    try:
        # Get conversation history
        messages = await message_service.get_messages(
            conversation_id=request.conversation_id
        )
        
        # Generate summary using AssemblyAI
        summary = await ai_summary_service.generate_summary(messages)
        
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected" if message_service else "not initialized",
            "translation": "configured" if translation_service and translation_service.api_key else "missing API key",
            "speech": "configured" if speech_service and speech_service.api_key else "missing API key",
            "storage": "configured" if storage_service else "not initialized",
            "summary": "configured" if ai_summary_service else "not initialized"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

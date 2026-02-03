from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict
from datetime import datetime
import os
from bson import ObjectId

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB"""
        cls.client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
        
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        return cls.client.healthcare_translation


class MessageService:
    """Service for handling message operations"""
    
    def __init__(self):
        self.db = Database.get_db()
        self.collection = self.db.messages
    
    async def create_message(
        self,
        original_text: str,
        translated_text: str,
        role: str,
        language: str,
        target_language: str,
        message_type: str = "text",
        audio_url: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """Create a new message in the database"""
        message = {
            "original_text": original_text,
            "translated_text": translated_text,
            "role": role,  # "doctor" or "patient"
            "language": language,
            "target_language": target_language,
            "message_type": message_type,  # "text" or "audio"
            "audio_url": audio_url,
            "conversation_id": conversation_id or "default",
            "timestamp": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(message)
        message["_id"] = str(result.inserted_id)
        message["timestamp"] = message["timestamp"].isoformat()
        message["created_at"] = message["created_at"].isoformat()
        
        return message
    
    async def get_messages(
        self,
        conversation_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get messages from conversation history"""
        query = {}
        if conversation_id:
            query["conversation_id"] = conversation_id
        
        cursor = self.collection.find(query).sort("timestamp", -1).limit(limit)
        messages = []
        
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat()
            doc["created_at"] = doc["created_at"].isoformat()
            messages.append(doc)
        
        # Return in chronological order
        return list(reversed(messages))
    
    async def search_messages(
        self,
        query: str,
        conversation_id: Optional[str] = None
    ) -> List[Dict]:
        """Search messages by text content"""
        search_filter = {
            "$or": [
                {"original_text": {"$regex": query, "$options": "i"}},
                {"translated_text": {"$regex": query, "$options": "i"}}
            ]
        }
        
        if conversation_id:
            search_filter["conversation_id"] = conversation_id
        
        cursor = self.collection.find(search_filter).sort("timestamp", -1)
        messages = []
        
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat()
            doc["created_at"] = doc["created_at"].isoformat()
            
            # Highlight matched text
            doc["highlight"] = self._highlight_match(query, doc)
            messages.append(doc)
        
        return messages
    
    def _highlight_match(self, query: str, doc: Dict) -> str:
        """Create highlighted snippet of matched text"""
        text = doc.get("original_text", "") + " " + doc.get("translated_text", "")
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Find the position of the match
        pos = text_lower.find(query_lower)
        if pos == -1:
            return text[:100] + "..." if len(text) > 100 else text
        
        # Get context around the match (50 chars before and after)
        start = max(0, pos - 50)
        end = min(len(text), pos + len(query) + 50)
        
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        
        return snippet

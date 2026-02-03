import httpx
import os
from typing import List, Dict

class AISummaryService:
    """Service for AI-powered conversation summarization using Groq API"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
    
    async def generate_summary(self, messages: List[Dict]) -> Dict:
        """
        Generate comprehensive medical summary from conversation
        
        Args:
            messages: List of message objects from database
        
        Returns:
            Dictionary with summary sections
        """
        # Prepare conversation text
        conversation_text = self._format_conversation(messages)
        
        if not self.groq_api_key:
            print("⚠️ WARNING: Groq API key not configured. Using fallback summarization.")
            summary = await self._generate_structured_summary(conversation_text, "")
        else:
            # Try to use Groq AI for summarization
            try:
                summary = await self._generate_ai_summary(conversation_text)
                print("✅ AI summary generated successfully with Groq")
            except Exception as e:
                print(f"⚠️ Groq AI summarization failed: {str(e)}. Using fallback.")
                summary = await self._generate_structured_summary(conversation_text, "")
        
        return {
            "summary": summary,
            "message_count": len(messages),
            "generated_at": self._get_timestamp()
        }
    
    def _format_conversation(self, messages: List[Dict]) -> str:
        """Format messages into readable conversation text"""
        formatted = []
        for msg in messages:
            role = msg.get("role", "unknown").capitalize()
            text = msg.get("original_text", "")
            translated = msg.get("translated_text", "")
            timestamp = msg.get("timestamp", "")
            
            formatted.append(f"[{timestamp}] {role}: {text}")
            if translated and translated != text:
                formatted.append(f"  (Translated: {translated})")
        
        return "\n".join(formatted)
    
    async def _generate_ai_summary(self, conversation: str) -> str:
        """
        Generate summary using Groq AI API (Llama 3 model)
        """
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are a medical assistant. Analyze this doctor-patient consultation and provide a structured medical summary.

Conversation:
{conversation}

Provide a comprehensive summary in this EXACT format:

═══════════════════════════════════════
   MEDICAL CONSULTATION SUMMARY
═══════════════════════════════════════

📋 CHIEF COMPLAINT & SYMPTOMS:
  • [List all symptoms mentioned]

🏥 MEDICAL HISTORY:
  • [Relevant medical history discussed]

🔬 DIAGNOSIS/ASSESSMENT:
  • [Doctor's diagnosis or assessment]

💊 MEDICATIONS PRESCRIBED:
  • [List any medications with dosage]

🏃 TREATMENT PLAN:
  • [Recommended treatments or interventions]

📅 FOLLOW-UP ACTIONS:
  • [Next steps, appointments, or instructions]

⚠️ KEY CONCERNS/WARNINGS:
  • [Important points requiring attention]

Be concise but thorough. If any section has no information, state "None mentioned" for that section."""

        payload = {
            "model": "llama-3.3-70b-versatile",  # Fast and accurate
            "messages": [
                {
                    "role": "system",
                    "content": "You are a medical documentation assistant. Provide clear, structured summaries of doctor-patient consultations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Lower temperature for more consistent medical summaries
            "max_tokens": 1000
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.groq_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"Groq API error: {response.status_code} - {response.text}")
            
            result = response.json()
            summary = result["choices"][0]["message"]["content"]
            
            return summary
    
    async def _generate_fallback_summary(self, messages: List[Dict]) -> Dict:
        """Generate summary without AI when API key is missing"""
        conversation_text = self._format_conversation(messages)
        summary = await self._generate_structured_summary(conversation_text, "")
        
        return {
            "summary": summary,
            "message_count": len(messages),
            "generated_at": self._get_timestamp()
        }
    
    async def _generate_structured_summary(self, conversation: str, prompt: str) -> str:
        """
        Generate summary with improved medical keyword extraction
        """
        lines = conversation.split("\n")
        
        summary_sections = {
            "symptoms": [],
            "history": [],
            "diagnosis": [],
            "medications": [],
            "treatment": [],
            "follow_up": [],
            "concerns": []
        }
        
        # Enhanced medical keyword matching
        for line in lines:
            line_lower = line.lower()
            line_clean = line.strip()
            
            if not line_clean or line_clean.startswith("(Translated:"):
                continue
            
            # Symptoms keywords - expanded
            if any(word in line_lower for word in [
                "pain", "fever", "cough", "symptom", "ache", "hurt", "sore",
                "nausea", "dizzy", "tired", "weak", "sick", "uncomfortable",
                "headache", "stomach", "chest", "breathing", "feel"
            ]):
                summary_sections["symptoms"].append(line_clean)
            
            # Medical history
            if any(word in line_lower for word in [
                "history", "previous", "before", "past", "allergic", "allergy",
                "surgery", "chronic", "condition", "family history"
            ]):
                summary_sections["history"].append(line_clean)
            
            # Diagnosis keywords - expanded
            if any(word in line_lower for word in [
                "diagnose", "diagnosis", "condition", "illness", "disease",
                "infection", "syndrome", "disorder", "found", "appears to be",
                "likely", "suspect"
            ]):
                summary_sections["diagnosis"].append(line_clean)
            
            # Medication keywords - expanded
            if any(word in line_lower for word in [
                "medication", "medicine", "prescribe", "prescription", "pill",
                "tablet", "drug", "dose", "take", "antibiotic", "painkiller",
                "mg", "ml", "twice", "daily", "times a day"
            ]):
                summary_sections["medications"].append(line_clean)
            
            # Treatment plan
            if any(word in line_lower for word in [
                "treatment", "therapy", "procedure", "rest", "exercise",
                "avoid", "should", "need to", "recommend", "suggest"
            ]):
                summary_sections["treatment"].append(line_clean)
            
            # Follow-up keywords - expanded
            if any(word in line_lower for word in [
                "follow", "appointment", "next", "come back", "return",
                "visit", "check", "monitor", "week", "days", "call if",
                "emergency", "urgent"
            ]):
                summary_sections["follow_up"].append(line_clean)
            
            # Key concerns
            if any(word in line_lower for word in [
                "concern", "worry", "important", "serious", "urgent",
                "critical", "warning", "careful", "watch for"
            ]):
                summary_sections["concerns"].append(line_clean)
        
        # Format comprehensive summary
        summary = "═══════════════════════════════════════\n"
        summary += "   MEDICAL CONSULTATION SUMMARY\n"
        summary += "═══════════════════════════════════════\n\n"
        
        summary += "📋 CHIEF COMPLAINT & SYMPTOMS:\n"
        if summary_sections["symptoms"]:
            for item in summary_sections["symptoms"][:5]:  # Limit to 5 most relevant
                summary += f"  • {item}\n"
        else:
            summary += "  • None mentioned\n"
        summary += "\n"
        
        summary += "🏥 MEDICAL HISTORY:\n"
        if summary_sections["history"]:
            for item in summary_sections["history"][:3]:
                summary += f"  • {item}\n"
        else:
            summary += "  • None discussed\n"
        summary += "\n"
        
        summary += "🔬 DIAGNOSIS/ASSESSMENT:\n"
        if summary_sections["diagnosis"]:
            for item in summary_sections["diagnosis"][:3]:
                summary += f"  • {item}\n"
        else:
            summary += "  • None provided\n"
        summary += "\n"
        
        summary += "💊 MEDICATIONS PRESCRIBED:\n"
        if summary_sections["medications"]:
            for item in summary_sections["medications"][:5]:
                summary += f"  • {item}\n"
        else:
            summary += "  • None prescribed\n"
        summary += "\n"
        
        summary += "🏃 TREATMENT PLAN:\n"
        if summary_sections["treatment"]:
            for item in summary_sections["treatment"][:5]:
                summary += f"  • {item}\n"
        else:
            summary += "  • None specified\n"
        summary += "\n"
        
        summary += "📅 FOLLOW-UP ACTIONS:\n"
        if summary_sections["follow_up"]:
            for item in summary_sections["follow_up"][:4]:
                summary += f"  • {item}\n"
        else:
            summary += "  • No follow-up scheduled\n"
        summary += "\n"
        
        summary += "⚠️ KEY CONCERNS/WARNINGS:\n"
        if summary_sections["concerns"]:
            for item in summary_sections["concerns"][:3]:
                summary += f"  • {item}\n"
        else:
            summary += "  • None noted\n"
        
        summary += "\n═══════════════════════════════════════\n"
        summary += f"Generated: {self._get_timestamp()}\n"
        summary += "═══════════════════════════════════════\n"
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

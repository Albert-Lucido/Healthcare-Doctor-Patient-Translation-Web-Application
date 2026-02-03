import httpx
import os
from typing import List, Dict

class AISummaryService:
    """Service for AI-powered conversation summarization using AssemblyAI LeMUR"""
    
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.base_url = "https://api.assemblyai.com/v2"
    
    async def generate_summary(self, messages: List[Dict]) -> Dict:
        """
        Generate comprehensive medical summary from conversation
        
        Args:
            messages: List of message objects from database
        
        Returns:
            Dictionary with summary sections
        """
        if not self.api_key:
            raise ValueError("AssemblyAI API key not configured")
        
        # Prepare conversation text
        conversation_text = self._format_conversation(messages)
        
        # Create a structured prompt for medical summarization
        prompt = f"""
Analyze the following doctor-patient conversation and provide a structured medical summary.

Conversation:
{conversation_text}

Please provide a comprehensive summary in the following format:

1. CHIEF COMPLAINT/SYMPTOMS:
   - List all symptoms mentioned by the patient

2. MEDICAL HISTORY:
   - Relevant medical history discussed

3. DIAGNOSIS/ASSESSMENT:
   - Doctor's diagnosis or assessment

4. MEDICATIONS PRESCRIBED:
   - List any medications discussed or prescribed

5. TREATMENT PLAN:
   - Recommended treatments or interventions

6. FOLLOW-UP ACTIONS:
   - Next steps, follow-up appointments, or instructions

7. KEY CONCERNS:
   - Important points requiring attention

Please be concise but thorough. If any section has no relevant information, state "None mentioned."
"""
        
        # Use a simple HTTP-based summarization approach
        # You can enhance this with AssemblyAI's LeMUR API when available
        summary = await self._generate_structured_summary(conversation_text, prompt)
        
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
    
    async def _generate_structured_summary(self, conversation: str, prompt: str) -> str:
        """
        Generate summary using a simple extraction approach
        This is a fallback method. For production, integrate with AssemblyAI LeMUR or OpenAI
        """
        # Simple keyword-based extraction as fallback
        # Replace this with actual AI summarization API call
        
        lines = conversation.split("\n")
        
        summary_sections = {
            "symptoms": [],
            "diagnosis": [],
            "medications": [],
            "follow_up": []
        }
        
        # Simple keyword matching
        for line in lines:
            line_lower = line.lower()
            
            # Symptoms keywords
            if any(word in line_lower for word in ["pain", "fever", "cough", "symptom", "feel"]):
                summary_sections["symptoms"].append(line)
            
            # Diagnosis keywords
            if any(word in line_lower for word in ["diagnose", "diagnosis", "condition", "illness"]):
                summary_sections["diagnosis"].append(line)
            
            # Medication keywords
            if any(word in line_lower for word in ["medication", "medicine", "prescribe", "pill", "tablet"]):
                summary_sections["medications"].append(line)
            
            # Follow-up keywords
            if any(word in line_lower for word in ["follow", "appointment", "next", "come back", "return"]):
                summary_sections["follow_up"].append(line)
        
        # Format summary
        summary = "MEDICAL CONSULTATION SUMMARY\n\n"
        
        summary += "SYMPTOMS:\n"
        summary += "\n".join(summary_sections["symptoms"]) if summary_sections["symptoms"] else "None mentioned\n"
        summary += "\n\n"
        
        summary += "DIAGNOSIS/ASSESSMENT:\n"
        summary += "\n".join(summary_sections["diagnosis"]) if summary_sections["diagnosis"] else "None mentioned\n"
        summary += "\n\n"
        
        summary += "MEDICATIONS:\n"
        summary += "\n".join(summary_sections["medications"]) if summary_sections["medications"] else "None mentioned\n"
        summary += "\n\n"
        
        summary += "FOLLOW-UP ACTIONS:\n"
        summary += "\n".join(summary_sections["follow_up"]) if summary_sections["follow_up"] else "None mentioned\n"
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

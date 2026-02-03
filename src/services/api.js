const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  /**
   * Send a text message
   */
  async sendMessage(text, role, language, targetLanguage) {
    const response = await fetch(`${this.baseUrl}/api/messages/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        role,
        language,
        target_language: targetLanguage,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    return response.json();
  }

  /**
   * Upload and process audio message
   */
  async uploadAudio(audioBlob, role, language, targetLanguage) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    formData.append('role', role);
    formData.append('language', language);
    formData.append('target_language', targetLanguage);

    const response = await fetch(`${this.baseUrl}/api/messages/audio`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload audio');
    }

    return response.json();
  }

  /**
   * Get conversation history
   */
  async getHistory(conversationId = null, limit = 100) {
    const params = new URLSearchParams();
    if (conversationId) params.append('conversation_id', conversationId);
    params.append('limit', limit.toString());

    const response = await fetch(
      `${this.baseUrl}/api/messages/history?${params}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch history');
    }

    return response.json();
  }

  /**
   * Search messages
   */
  async searchMessages(query, conversationId = null) {
    const response = await fetch(`${this.baseUrl}/api/messages/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to search messages');
    }

    return response.json();
  }

  /**
   * Generate AI summary
   */
  async generateSummary(conversationId) {
    const response = await fetch(`${this.baseUrl}/api/summary/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to generate summary');
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/api/health`);
    return response.json();
  }
}

export default new ApiService();

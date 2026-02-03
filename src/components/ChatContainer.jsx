import { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import SearchBar from './SearchBar';
import SummaryModal from './SummaryModal';
import ApiService from '../services/api';
import './ChatContainer.css';

function ChatContainer({ role, language, targetLanguage, onChangeRole }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [summary, setSummary] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadHistory = async () => {
    try {
      const response = await ApiService.getHistory();
      if (response.success) {
        setMessages(response.messages);
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const handleSendMessage = async (text) => {
    try {
      setLoading(true);
      const response = await ApiService.sendMessage(
        text,
        role,
        language,
        targetLanguage
      );

      if (response.success) {
        setMessages((prev) => [...prev, response.message]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAudioMessage = async (audioBlob) => {
    try {
      setLoading(true);
      const response = await ApiService.uploadAudio(
        audioBlob,
        role,
        language,
        targetLanguage
      );

      if (response.success) {
        setMessages((prev) => [...prev, response.message]);
      }
    } catch (error) {
      console.error('Failed to send audio:', error);
      alert('Failed to send audio message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setSearchResults(null);
      return;
    }

    try {
      const response = await ApiService.searchMessages(query);
      if (response.success) {
        setSearchResults(response.results);
      }
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const handleGenerateSummary = async () => {
    try {
      setLoading(true);
      const response = await ApiService.generateSummary('default');
      if (response.success) {
        setSummary(response.summary);
        setShowSummary(true);
      }
    } catch (error) {
      console.error('Failed to generate summary:', error);
      alert('Failed to generate summary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const displayMessages = searchResults || messages;

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-info">
          <span className="role-badge">{role === 'doctor' ? '👨‍⚕️ Doctor' : '👤 Patient'}</span>
          <span className="language-info">
            {language.toUpperCase()} → {targetLanguage.toUpperCase()}
          </span>
        </div>
        <div className="chat-actions">
          <button
            className="btn btn-secondary btn-sm"
            onClick={handleGenerateSummary}
            disabled={loading || messages.length === 0}
          >
            📋 Summary
          </button>
          <button className="btn btn-secondary btn-sm" onClick={onChangeRole}>
            🔄 Change Role
          </button>
        </div>
      </div>

      <SearchBar onSearch={handleSearch} onClear={() => setSearchResults(null)} />

      <MessageList
        messages={displayMessages}
        currentRole={role}
        isSearchResult={!!searchResults}
      />
      <div ref={messagesEndRef} />

      <MessageInput
        onSendMessage={handleSendMessage}
        onSendAudio={handleAudioMessage}
        disabled={loading}
      />

      {showSummary && (
        <SummaryModal
          summary={summary}
          onClose={() => setShowSummary(false)}
        />
      )}
    </div>
  );
}

export default ChatContainer;

import { useState, useRef } from 'react';
import AudioRecorder from './AudioRecorder';
import './css/MessageInput.css';

function MessageInput({ onSendMessage, onSendAudio, disabled }) {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
      // Reset textarea height
      if (inputRef.current) {
        inputRef.current.style.height = 'auto';
      }
      inputRef.current?.focus();
    }
  };

  const handleChange = (e) => {
    setMessage(e.target.value);
    // Auto-resize textarea
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 200) + 'px';
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleAudioRecorded = (audioBlob) => {
    onSendAudio(audioBlob);
    setIsRecording(false);
  };

  return (
    <div className="message-input-container">
      {isRecording ? (
        <AudioRecorder
          onRecordingComplete={handleAudioRecorded}
          onCancel={() => setIsRecording(false)}
        />
      ) : (
        <form className="message-input-form" onSubmit={handleSubmit}>
          <button
            type="button"
            className="btn-icon mic-btn"
            onClick={() => setIsRecording(true)}
            disabled={disabled}
            title="Record voice message"
          >
            🎤
          </button>

          <textarea
            ref={inputRef}
            className="message-input"
            placeholder="Type your message..."
            value={message}
            onChange={handleChange}
            onKeyPress={handleKeyPress}
            disabled={disabled}
            rows={1}
          />

          <button
            type="submit"
            className="btn-icon send-btn"
            disabled={!message.trim() || disabled}
            title="Send message"
          >
            {disabled ? '⏳' : '📤'}
          </button>
        </form>
      )}
    </div>
  );
}

export default MessageInput;

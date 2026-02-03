import './css/MessageList.css';

function MessageList({ messages, currentRole, isSearchResult }) {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const highlightText = (text, highlight) => {
    if (!highlight || !isSearchResult) return text;
    
    const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
    return parts.map((part, i) => 
      part.toLowerCase() === highlight.toLowerCase() ? (
        <mark key={i}>{part}</mark>
      ) : (
        part
      )
    );
  };

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h3>No messages yet</h3>
          <p>Start a conversation by typing or recording a message below</p>
        </div>
      ) : (
        messages.map((message, index) => {
          const isCurrentUser = message.role === currentRole;
          
          return (
            <div
              key={message._id || index}
              className={`message ${isCurrentUser ? 'sent' : 'received'}`}
            >
              <div className="message-bubble">
                <div className="message-header">
                  <span className="message-role">
                    {message.role === 'doctor' ? '👨‍⚕️ Doctor' : '👤 Patient'}
                  </span>
                  <span className="message-time">{formatTime(message.timestamp)}</span>
                </div>

                <div className="message-content">
                  <p className="original-text">{message.original_text}</p>
                  
                  {message.translated_text && 
                   message.translated_text !== message.original_text && 
                   !message.translated_text.includes('[Translation') && (
                    <p className="translated-text">
                      🌐 {message.translated_text}
                    </p>
                  )}
                  
                  {message.translated_text && 
                   message.translated_text.includes('[Translation') && (
                    <p className="translation-error">
                      ⚠️ Translation unavailable - check API configuration
                    </p>
                  )}

                  {message.audio_url && (
                    <div className="audio-player">
                      <audio controls>
                        <source src={message.audio_url} type="audio/webm" />
                        <source src={message.audio_url} type="audio/mp3" />
                        Your browser does not support audio playback.
                      </audio>
                    </div>
                  )}

                  {isSearchResult && message.highlight && (
                    <p className="search-highlight">
                      📍 {message.highlight}
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}

export default MessageList;

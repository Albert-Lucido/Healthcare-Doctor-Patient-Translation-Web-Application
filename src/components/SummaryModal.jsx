import './SummaryModal.css';

function SummaryModal({ summary, onClose }) {
  const formatSummary = (summaryData) => {
    if (typeof summaryData === 'string') {
      return summaryData;
    }
    return summaryData?.summary || 'No summary available';
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>📋 Consultation Summary</h2>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>
        
        <div className="modal-body">
          <div className="summary-notice">
            <p>🤖 AI-powered medical summary using Groq (Llama 3.3)</p>
          </div>
          
          <div className="summary-content">
            <pre>{formatSummary(summary)}</pre>
          </div>
          
          {summary?.message_count && (
            <div className="summary-meta">
              <span>📊 Based on {summary.message_count} messages</span>
              {summary?.generated_at && (
                <span> • Generated: {new Date(summary.generated_at).toLocaleString()}</span>
              )}
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
          <button
            className="btn btn-primary"
            onClick={() => {
              const text = formatSummary(summary);
              navigator.clipboard.writeText(text);
              alert('Summary copied to clipboard!');
            }}
          >
            📋 Copy to Clipboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default SummaryModal;

import { useState, useRef, useEffect } from 'react';
import './css/AudioRecorder.css';

function AudioRecorder({ onRecordingComplete, onCancel }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    startRecording();
    return () => {
      stopRecording();
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to access microphone. Please check permissions.');
      onCancel();
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const handleStop = () => {
    stopRecording();
  };

  const handleSend = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob);
    }
  };

  const handleCancel = () => {
    stopRecording();
    onCancel();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-recorder">
      <div className="recorder-content">
        {isRecording ? (
          <>
            <div className="recording-indicator">
              <span className="pulse"></span>
              <span className="recording-text">Recording...</span>
            </div>
            <div className="recording-time">{formatTime(recordingTime)}</div>
            <button className="btn btn-danger" onClick={handleStop}>
              ⏹ Stop
            </button>
          </>
        ) : audioBlob ? (
          <>
            <div className="audio-preview">
              <span>✓ Recording complete</span>
              <span className="recording-time">{formatTime(recordingTime)}</span>
            </div>
            <div className="audio-actions">
              <button className="btn btn-secondary" onClick={handleCancel}>
                ✕ Cancel
              </button>
              <button className="btn btn-success" onClick={handleSend}>
                📤 Send
              </button>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default AudioRecorder;

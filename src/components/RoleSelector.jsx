import { useState } from 'react';
import './css/RoleSelector.css';

const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'zh-Hans', name: 'Chinese', flag: '🇨🇳' },
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'fil', name: 'Filipino', flag: '🇵🇭' },
];

function RoleSelector({ onSelectRole }) {
  const [selectedRole, setSelectedRole] = useState(null);
  const [sourceLanguage, setSourceLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('es');

  const handleContinue = () => {
    if (selectedRole && sourceLanguage && targetLanguage) {
      onSelectRole(selectedRole, sourceLanguage, targetLanguage);
    }
  };

  return (
    <div className="role-selector">
      <div className="role-selector-container">
        <h2>Welcome! Let's Get Started</h2>
        <p className="description">
          Select your role and preferred languages for the consultation
        </p>

        <div className="role-cards">
          <div
            className={`role-card ${selectedRole === 'doctor' ? 'selected' : ''}`}
            onClick={() => setSelectedRole('doctor')}
          >
            <div className="role-icon">👨‍⚕️</div>
            <h3>Doctor</h3>
            <p>I am the healthcare provider</p>
          </div>

          <div
            className={`role-card ${selectedRole === 'patient' ? 'selected' : ''}`}
            onClick={() => setSelectedRole('patient')}
          >
            <div className="role-icon">👤</div>
            <h3>Patient</h3>
            <p>I am seeking medical care</p>
          </div>
        </div>

        {selectedRole && (
          <div className="language-selector">
            <h3>Language Settings</h3>
            
            <div className="language-group">
              <label>I speak:</label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                className="language-select"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="language-group">
              <label>Translate to:</label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="language-select"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <button className="btn btn-primary continue-btn" onClick={handleContinue}>
              Continue to Chat
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default RoleSelector;

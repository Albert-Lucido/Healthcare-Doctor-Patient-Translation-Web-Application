import { useState, useEffect } from 'react';
import ChatContainer from './components/ChatContainer';
import RoleSelector from './components/RoleSelector';
import './App.css';

function App() {
  const [role, setRole] = useState(null);
  const [language, setLanguage] = useState('en');
  const [targetLanguage, setTargetLanguage] = useState('es');

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏥 Healthcare Translation</h1>
        <p className="subtitle">Doctor-Patient Communication Bridge</p>
      </header>

      {!role ? (
        <RoleSelector
          onSelectRole={(selectedRole, sourceLang, targetLang) => {
            setRole(selectedRole);
            setLanguage(sourceLang);
            setTargetLanguage(targetLang);
          }}
        />
      ) : (
        <ChatContainer
          role={role}
          language={language}
          targetLanguage={targetLanguage}
          onChangeRole={() => setRole(null)}
        />
      )}
    </div>
  );
}

export default App;

# Healthcare Doctor-Patient Translation Web Application

A real-time healthcare translation platform enabling seamless multilingual doctor-patient communication with AI-powered medical summarization.

## 🚀 Features

- **Real-time Translation**: Powered by Microsoft Azure Translator with support for 100+ languages
- **Text & Audio Chat**: Type or record messages with role distinction (Doctor/Patient)
- **AI Medical Summaries**: Intelligent conversation summaries using Groq AI (Llama 3.3)
- **Search & Highlighting**: Find specific terms in conversation history
- **Conversation Logging**: Persistent storage with MongoDB
- **Audio Playback**: Review recorded messages with Cloudinary storage

## 🛠️ Tech Stack

**Frontend:**
- React 19 + Vite
- Deployed on Vercel

**Backend:**
- FastAPI (Python)
- Deployed on Render
- MongoDB for data persistence

**AI/ML Services:**
- Azure Translator API (translation)
- AssemblyAI (speech-to-text)
- Groq API with Llama 3.3 (medical summarization)
- Cloudinary (audio storage)

## 📋 Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Healthcare-Doctor-Patient-Translation-Web-Application
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:
```env
MONGODB_URI=your_mongodb_connection_string
AZURE_TRANSLATOR_KEY=your_azure_translator_key
AZURE_TRANSLATOR_REGION=your_azure_region
ASSEMBLYAI_API_KEY=your_assemblyai_key
GROQ_API_KEY=your_groq_api_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```

**Get Free API Keys:**
- **Groq**: Sign up at [groq.com](https://console.groq.com) - Free tier with fast inference
- **Azure Translator**: [Azure Portal](https://portal.azure.com) - Free tier available
- **AssemblyAI**: [assemblyai.com](https://www.assemblyai.com) - Free tier for speech-to-text
- **MongoDB**: [mongodb.com/atlas](https://www.mongodb.com/cloud/atlas) - Free M0 cluster
- **Cloudinary**: [cloudinary.com](https://cloudinary.com) - Free tier for audio storage

Run backend:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd ..
npm install
```

Create `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

Run frontend:
```bash
npm run dev
```

## 🌐 Deployment

**Frontend (Vercel):**
```bash
vercel --prod
```
Set environment variable: `VITE_API_BASE_URL=https://your-backend-url.onrender.com`

**Backend (Render):**
1. Connect GitHub repository
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add all environment variables from `.env`

## 📱 Usage

1. **Select Role**: Choose Doctor or Patient
2. **Choose Language**: Select your preferred language
3. **Start Conversation**: Type or record messages
4. **View Translations**: Messages auto-translate to target language
5. **Generate Summary**: Click "Generate AI Summary" for medical insights
6. **Search History**: Use search bar to find specific information

## 🔑 Core Functionalities

✅ Real-time multilingual translation  
✅ Text chat interface with role distinction  
✅ Audio recording & playback  
✅ Conversation logging with timestamps  
✅ Search with keyword highlighting  
✅ AI-powered medical summarization (Groq)

## 📝 License

MIT License


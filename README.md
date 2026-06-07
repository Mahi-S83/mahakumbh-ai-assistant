# KumbhSaathi — AI-Powered Multilingual Pilgrim Assistant

AI safety and navigation assistant for Mahakumbh 2028 pilgrims

## 🌐 Live Demo
[https://mahakumbh-ai-assistant.vercel.app](https://mahakumbh-ai-assistant.vercel.app)

## 🎥 Demo Video
[Watch on Loom](https://www.loom.com/share/1340acddce5b40aca0b57bef7ee672cd)

## 🙏 Problem Statement
100 million pilgrims visit Mahakumbh from diverse linguistic and cultural backgrounds. First-time visitors struggle with navigation, emergencies, and event schedules. Families get separated in crowds with no reliable way to reconnect.

## ✨ Features

- 🌍 **Multilingual AI Chat** — Hindi, English, Bengali, Tamil with auto-language detection
- 👨‍👩‍👧‍👦 **Family Location Tracking** — Create a group PIN, share live GPS, see family on interactive map
- 🆘 **Emergency SOS** — One-tap WhatsApp share with real GPS coordinates + helpline numbers
- 🎤 **Voice Input** — Speak in Hindi or English, auto-sends to AI
- ⚡ **Hybrid FAQ System** — Sub-100ms responses for common queries, no AI call needed
- 📅 **Event Schedule** — Aarti timings, bathing dates, daily programme
- 🏨 **Accommodation Guidance** — Tent prices, hotels, dharamshalas with pricing
- 📍 **Navigation Help** — Ghats, gates, transport, distances from Ujjain railway station
- 🏥 **Medical & Emergency** — Camp locations, helplines 108/100/1920

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript, Leaflet.js |
| Backend | FastAPI (Python 3.11) |
| AI Engine | Groq — Llama 3.3 70B |
| Maps | OpenStreetMap via Leaflet (free, no API key) |
| Voice | Web Speech API (native browser) |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |

## 🏗️ Architecture

Every incoming query first hits a local FAQ dictionary — returning answers in under 100ms for common pilgrim queries. Only unmatched queries fall through to Groq's Llama 3.3 70B, which responds in the user's language. A static fallback layer ensures the app never returns an error.

```
User Query → FAQ Matcher (<100ms) → Groq AI (if no match) → Fallback
```

## 🚀 Local Setup

```bash
# Clone the repo
git clone https://github.com/Mahi-S83/mahakumbh-ai-assistant.git
cd mahakumbh-ai-assistant/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Start backend
uvicorn main:app --reload --port 8000
```

Open `frontend/index.html` in your browser.

Get a free Groq API key at [console.groq.com](https://console.groq.com)

## 🆘 Emergency Contacts

| Service | Number |
|---------|--------|
| Police | 100 / 112 |
| Ambulance | 108 |
| Kumbh Helpline | 1920 |
| Women Helpline | 1090 |
| Child Helpline | 1098 |

## 🔮 Future Scope

- Real-time crowd heatmap
- Push notifications for event reminders
- Offline mode with Service Worker
- More languages: Marathi, Gujarati, Telugu
- WhatsApp bot integration

## 👨‍💻 Built By

**Mahi Singh**  
Mahakumbh Innovation Hackathon 2028  
Expert Hire × VIT Bhopal  
Track: AI-Powered Multilingual Pilgrim Assistant

## 📄 License

MIT License — free to use, modify, and distribute
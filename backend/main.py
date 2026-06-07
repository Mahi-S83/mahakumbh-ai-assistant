from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq import Groq
import os
from datetime import datetime, timedelta
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# ============ GROQ CONFIGURATION ============
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
    print("✅ Groq configured successfully")
else:
    groq_client = None
    print("❌ No Groq API key found")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Family Location Storage
family_groups: Dict[str, Dict] = {}

# FAQ Database
FAQ = {
    "bathing ghat": "Main bathing ghats: Triveni Sangam, Ram Ghat, Hanuman Ghat. Open 4 AM - 9 PM.",
    "how to reach": "Take electric bus from parking (free). Auto from city center (₹30-50).",
    "nearest gate": "Gate 1: Triveni side | Gate 2: Main entrance | Gate 3: Lost & found",
    "accommodation": "Tents: Premium ₹5000-10000, Deluxe ₹2000-5000, General ₹500-2000. Book at Gate 2.",
    "hotel": "Budget hotels near railway station (₹800-1500).",
    "dharamshala": "Free stays: Shri Ram Dharamshala (Gate 1), Hanuman Mandir (Gate 3).",
    "food": "FREE PRASAD: 12-2 PM at all ghats. Food courts at Sector 2,5,9.",
    "water": "Free drinking water at 50+ locations. Look for blue RO booths.",
    "toilet": "Free toilets at every sector. Female toilets: Gate 2,4,7.",
    "locker": "Luggage lockers at Gate 1,3,5. ₹50-100/day.",
    "transport": "Free electric buses every 10 min. Auto from ₹30.",
    "prasad": "Free prasad at Triveni Ghat (12 PM), Ram Ghat (1 PM).",
    "shopping": "Official merchandise: Gate 2. Local shops: Sector 6,8.",
    "lost child": "Call child helpline 1098. Lost & found: Gate 3, Sector 5.",
    "medical": "Medical camps: Sector 4,7,12, Gate 2. Ambulance: 108.",
    "police": "Police: 112 | Women: 1090 | Child: 1098 | Cyber: 1930.",
    "aarti timing": "Ganga Aarti: Morning 5:30 AM, Evening 6:30 PM at Triveni Ghat.",
    "event schedule": "4 AM: Maha Snan | 7 AM: Yoga | 12 PM: Prasad | 6:30 PM: Aarti",
    "crowd": "Best time: 4-8 AM. Peak: 10 AM - 4 PM.",
    "weather": "Morning 15°C, Afternoon 28°C, Night 18°C.",
    "distance from gate 1 to triveni": "Gate 1 to Triveni Sangam: 500 meters, 5-7 minute walk",
"distance from gate 2 to ram ghat": "Gate 2 to Ram Ghat: 300 meters, 4 minute walk",
"distance from parking to gate 1": "Parking to Gate 1: 200 meters, 3 minute walk",
"distance from sector 4 to medical camp": "Sector 4 to Medical Camp: 100 meters, 2 minute walk",
}

EVENTS = {
    "today": [
        {"time": "4:00 AM", "event": "Maha Snan", "venue": "Triveni Ghat"},
        {"time": "7:00 AM", "event": "Yoga Session", "venue": "Sector 3"},
        {"time": "12:00 PM", "event": "Prasad Distribution", "venue": "All Ghats"},
        {"time": "6:30 PM", "event": "Ganga Aarti", "venue": "Triveni Ghat"},
    ]
}
# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))
class ChatRequest(BaseModel):
    message: str
    language: str = "english"

class ChatResponse(BaseModel):
    reply: str

class CreateGroupRequest(BaseModel):
    group_id: str
    user_name: str

class ShareLocationRequest(BaseModel):
    group_id: str
    user_name: str
    lat: float
    lng: float

def translate_to_language(text, language):
    translations = {
        "bengali": {
            "Medical camps": "মেডিকেল ক্যাম্প",
            "Emergency": "জরুরি অবস্থা",
            "Police": "পুলিশ",
            "Ambulance": "অ্যাম্বুলেন্স",
            "TODAY'S SCHEDULE": "আজকের সময়সূচী",
            "Lost & Found": "হারানো ও পাওয়া",
        },
        "tamil": {
            "Medical camps": "மருத்துவ முகாம்கள்",
            "Emergency": "அவசர நிலை",
            "Police": "போலீஸ்",
            "Ambulance": "ஆம்புலன்ஸ்",
            "TODAY'S SCHEDULE": "இன்றைய அட்டவணை",
            "Lost & Found": "இழந்து கிடைத்தது",
        },
        "hindi": {
            "Medical camps": "मेडिकल कैंप",
            "Emergency": "आपातकालीन",
            "Police": "पुलिस",
            "Ambulance": "एम्बुलेंस",
            "TODAY'S SCHEDULE": "आज का कार्यक्रम",
            "Lost & Found": "खोया पाया",
        }
    }
    
    if language in translations:
        for eng, trans in translations[language].items():
            text = text.replace(eng, trans)
    return text

@app.post("/api/chat")
async def chat(request: ChatRequest):
    msg_lower = request.message.lower()
    
    # Check FAQ first
    for key, answer in FAQ.items():
        if key in msg_lower:
            if request.language != "english":
              return ChatResponse(reply=translate_to_language(answer, request.language))
            return ChatResponse(reply=answer)
    
    # Check events
    if "event" in msg_lower or "schedule" in msg_lower:
        events_list = "\n".join([f"• {e['time']} - {e['event']}" for e in EVENTS["today"]])
        return ChatResponse(reply=f"📅 TODAY'S SCHEDULE:\n{events_list}")
    
    # Use Groq for AI responses
    if groq_client:
        try:
            completion = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": f"You are KumbhSaathi for Mahakumbh 2028. Respond in {request.language}. Max 2 sentences."},
        {"role": "user", "content": request.message}
    ],
    temperature=0.7,
    max_tokens=150
)
            reply = completion.choices[0].message.content
            if reply:
                return ChatResponse(reply=reply)
        except Exception as e:
            print(f"Groq error: {e}")
    
    # Fallback
    return ChatResponse(reply="I can help with: medical camps, lost child, aarti timings, accommodation, food, transport. What do you need?")

@app.post("/api/leave-group")
async def leave_group(request: CreateGroupRequest):
    """Remove user from family group"""
    if request.group_id not in family_groups:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if request.user_name not in family_groups[request.group_id]:
        raise HTTPException(status_code=404, detail="User not in this group")
    
    # Remove user from group
    del family_groups[request.group_id][request.user_name]
    
    # If group becomes empty, delete the group
    if len(family_groups[request.group_id]) == 0:
        del family_groups[request.group_id]
    
    return {"status": "success", "message": f"{request.user_name} left the group"}

@app.post("/api/create-group")
async def create_group(request: CreateGroupRequest):
    if request.group_id in family_groups:
        raise HTTPException(status_code=400, detail="Group exists")
    
    family_groups[request.group_id] = {
        request.user_name: {
            "lat": 0, "lng": 0, "last_update": datetime.now(IST).isoformat()
        }
    }
    return {"status": "success", "message": f"Group '{request.group_id}' created"}

@app.post("/api/join-group")
async def join_group(request: CreateGroupRequest):
    if request.group_id not in family_groups:
        raise HTTPException(status_code=404, detail="Group not found")
    
    family_groups[request.group_id][request.user_name] = {
        "lat": 0, "lng": 0, "last_update": datetime.now(IST).isoformat()
    }
    return {"status": "success", "message": f"Joined '{request.group_id}'"}

@app.post("/api/share-location")
async def share_location(request: ShareLocationRequest):
    if request.group_id not in family_groups:
        raise HTTPException(status_code=404, detail="Group not found")
    
    family_groups[request.group_id][request.user_name] = {
        "lat": request.lat,
        "lng": request.lng,
        "last_update": datetime.now(IST).isoformat()
    }
    return {"status": "success"}

@app.get("/api/get-family-locations/{group_id}")
async def get_family_locations(group_id: str):
    if group_id not in family_groups:
        raise HTTPException(status_code=404, detail="Group not found")
    return family_groups[group_id]

@app.get("/api/emergency")
async def emergency():
    return {
        "ambulance": "108",
        "police": "112",
        "women": "1090",
        "child": "1098",
    }

@app.get("/api/events")
async def events():
    return EVENTS

@app.get("/api/health")
async def health():
    return {"status": "healthy", "groq_configured": groq_client is not None}
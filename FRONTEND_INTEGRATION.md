# Buddy AI - Frontend Integration Guide

**API Documentation for Frontend Team**

---

## 🚀 Quick Start

### Base URL

**Production (Render):** `https://your-app.onrender.com` (once deployed)  
**Local Development:** `http://localhost:8000`

### API Documentation

Interactive docs available at:
- **Swagger UI:** `{BASE_URL}/docs`
- **ReDoc:** `{BASE_URL}/redoc`

---

## 🔑 Authentication

**No authentication required** for MVP. All endpoints are public.

Future: Add API key header if needed.

---

## 📡 API Endpoints

### 1. POST /chat - Send Message

Main endpoint for chatting with Buddy.

#### Request

```typescript
POST /chat
Content-Type: application/json

{
  "user_id": string,      // Required: Unique user identifier
  "message": string,      // Required: User's message
  "meta": {               // Optional: Real-world context
    "city": string,       // e.g., "Bangalore", "Mumbai"
    "place": string,      // e.g., "workplace", "home"
    "time": string,       // e.g., "morning", "evening"
    "event": string       // e.g., "exam", "interview"
  }
}
```

#### Response

```typescript
{
  "reply": string,              // Buddy's response text
  "mode": string,               // Response mode used
  "emotion": string,            // Detected emotion
  "intensity": number,          // Emotion intensity (1-10)
  "relationship": string,       // Detected relationship type
  "learning": string | null,    // Learning message (if available)
  "error": string | null        // Error message (if any)
}
```

#### Example - JavaScript/TypeScript

```typescript
async function sendMessage(userId: string, message: string) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      message: message,
      meta: {
        city: 'Bangalore',
        place: 'workplace',
        time: 'afternoon'
      }
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
const result = await sendMessage('user_123', 'My boss yelled at me');
console.log(result.reply);      // Display in chat
console.log(result.learning);   // Show learning badge
```

#### Example - React Hook

```tsx
import { useState } from 'react';

function useBuddyChat() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (userId: string, message: string, meta?: any) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message, meta })
      });

      if (!response.ok) throw new Error('API request failed');
      
      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { sendMessage, loading, error };
}

// Usage in component
function ChatComponent() {
  const { sendMessage, loading } = useBuddyChat();
  const [messages, setMessages] = useState([]);

  const handleSend = async (text: string) => {
    const result = await sendMessage('user_123', text, {
      city: 'Bangalore',
      time: new Date().getHours() > 18 ? 'evening' : 'afternoon'
    });
    
    if (result) {
      setMessages([...messages, {
        user: text,
        buddy: result.reply,
        learning: result.learning
      }]);
    }
  };

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>
          <p><strong>You:</strong> {msg.user}</p>
          <p><strong>Buddy:</strong> {msg.buddy}</p>
          {msg.learning && (
            <span className="badge">✨ {msg.learning}</span>
          )}
        </div>
      ))}
      {loading && <p>Buddy is typing...</p>}
    </div>
  );
}
```

---

### 2. POST /chat/whatsapp - WhatsApp Import

Import and analyze WhatsApp chat exports.

#### Request

```typescript
POST /chat/whatsapp
Content-Type: application/json

{
  "user_id": string,          // Required
  "chat_text": string,        // Required: Raw WhatsApp export
  "meta": {                   // Optional
    "city": string
  }
}
```

#### Response

Same as `/chat` endpoint.

#### Example

```typescript
async function importWhatsApp(userId: string, chatText: string) {
  const response = await fetch('http://localhost:8000/chat/whatsapp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      chat_text: chatText
    })
  });
  
  return await response.json();
}

// Usage with file upload
function WhatsAppImport() {
  const handleFileUpload = async (event: any) => {
    const file = event.target.files[0];
    const text = await file.text();
    const result = await importWhatsApp('user_123', text);
    console.log(result.reply);
  };

  return (
    <input 
      type="file" 
      accept=".txt" 
      onChange={handleFileUpload} 
    />
  );
}
```

---

### 3. GET /chat/learning/{user_id} - Learning Insights

Get what Buddy has learned about a user.

#### Request

```typescript
GET /chat/learning/{user_id}
```

#### Response

```typescript
{
  "user_id": string,
  "total_interactions": number,
  "traits": string[],                // Learned personality traits
  "common_scenarios": string[],      // Top 3 scenarios
  "common_emotions": string[],       // Top 3 emotions
  "adaptations_learned": string[]    // Learning messages
}
```

#### Example

```typescript
async function getLearningInsights(userId: string) {
  const response = await fetch(`http://localhost:8000/chat/learning/${userId}`);
  return await response.json();
}

// Usage
const insights = await getLearningInsights('user_123');

console.log(`Total chats: ${insights.total_interactions}`);
console.log('Traits:', insights.traits);
console.log('Adaptations:', insights.adaptations_learned);

// Display in UI
function LearningPanel({ userId }: { userId: string }) {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    getLearningInsights(userId).then(setInsights);
  }, [userId]);

  if (!insights) return <div>Loading...</div>;

  return (
    <div className="learning-panel">
      <h3>What Buddy Learned About You</h3>
      <p>Chats: {insights.total_interactions}</p>
      
      <h4>Adaptations:</h4>
      {insights.adaptations_learned.map((adaptation, i) => (
        <p key={i}>✅ {adaptation}</p>
      ))}
      
      <h4>Common Topics:</h4>
      <ul>
        {insights.common_scenarios.map((scenario, i) => (
          <li key={i}>{scenario}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

### 4. GET / - Root

Health check and API info.

#### Response

```typescript
{
  "status": "running",
  "service": "Buddy AI",
  "version": "1.0.0",
  "message": string,
  "endpoints": {
    "chat": "POST /chat",
    "whatsapp": "POST /chat/whatsapp",
    "learning": "GET /chat/learning/{user_id}",
    "health": "GET /chat/health"
  }
}
```

---

### 5. GET /health - Health Check

Check if API is running.

#### Response

```typescript
{
  "status": "healthy",
  "api_key_configured": boolean,
  "mongodb_configured": boolean,
  "learning_enabled": boolean
}
```

---

## 🌍 Meta Context (Important!)

The `meta` field provides real-world context for better responses.

### Available Fields

```typescript
meta?: {
  city?: string,      // User's city
  place?: string,     // Current location type
  time?: string,      // Time of day
  event?: string      // Specific event
}
```

### City Values

Use actual city names:
- `"Bangalore"`, `"Mumbai"`, `"Delhi"`, `"Pune"`, `"Hyderabad"`, `"Chennai"`, etc.

### Place Values

- `"transit"` - Railway station, metro, bus stop
- `"workplace"` - Office, meeting room
- `"home"` - User's home
- `"educational"` - College, university, exam hall
- `"hospital"` - Medical facility
- `"restaurant"` - Food place
- `"airport"` - Airport

### Time Values

- `"morning"`, `"afternoon"`, `"evening"`, `"night"`, `"late_night"`

### Event Values

- `"exam"`, `"interview"`, `"meeting"`, `"date"`, `"festival"`

### Why Meta Matters

**Without meta:**
```
User: "Train delayed"
Buddy: "Try taking the metro instead"
```

**With meta (city: "Bangalore"):**
```
User: "Train delayed"
Buddy: "Bangalore metro's purple line might work if you're heading to MG Road..."
```

**Grounded in local context!** 🎯

### How to Get Meta

```typescript
// Option 1: Ask user for city (one-time)
const userCity = localStorage.getItem('userCity') || 'Bangalore';

// Option 2: Browser geolocation
navigator.geolocation.getCurrentPosition(async (pos) => {
  const response = await fetch(
    `https://api.geocoding.com/reverse?lat=${pos.latitude}&lng=${pos.longitude}`
  );
  const data = await response.json();
  const city = data.city;
});

// Option 3: Time from browser
const time = new Date().getHours() > 18 ? 'evening' : 'afternoon';

// Build meta object
const meta = {
  city: userCity,
  time: time,
  place: 'home' // or infer from user input
};
```

---

## 🎨 UI/UX Recommendations

### 1. Show Learning Badges

When `result.learning` is not null, show it to the user:

```tsx
{result.learning && (
  <div className="learning-badge">
    ✨ {result.learning}
  </div>
)}
```

**Example:**
> ✨ Buddy learned you prefer diplomatic approaches

This shows the AI is adapting!

### 2. Display Typing Indicator

```tsx
{loading && (
  <div className="typing-indicator">
    <span>●</span><span>●</span><span>●</span>
    Buddy is thinking...
  </div>
)}
```

### 3. Learning Insights Page

Create a dedicated page showing `/chat/learning/{user_id}`:

```tsx
function LearningPage() {
  const insights = useLearningInsights(userId);
  
  return (
    <div>
      <h1>Your Journey with Buddy</h1>
      <p>Total conversations: {insights.total_interactions}</p>
      
      <h2>What Buddy Learned</h2>
      {insights.adaptations_learned.map(item => (
        <Card>✅ {item}</Card>
      ))}
    </div>
  );
}
```

**This is impressive in demos!** Judges love visible AI learning.

### 4. Context Settings

Let users set their city:

```tsx
<select value={city} onChange={e => setCity(e.target.value)}>
  <option>Bangalore</option>
  <option>Mumbai</option>
  <option>Delhi</option>
  <option>Pune</option>
</select>
```

Then include in every chat request.

---

## 🔄 Error Handling

### Handle Errors Gracefully

```typescript
try {
  const result = await sendMessage(userId, message);
  
  if (result.error) {
    // Backend returned an error but didn't crash
    showNotification('Buddy had trouble responding. Try again?');
  } else {
    // Success
    displayMessage(result.reply);
  }
} catch (error) {
  // Network or other error
  showNotification('Connection issue. Check your internet.');
}
```

### Loading States

```typescript
const [isLoading, setIsLoading] = useState(false);

const sendChat = async () => {
  setIsLoading(true);
  try {
    const result = await sendMessage(userId, message);
    // Handle result
  } finally {
    setIsLoading(false);
  }
};
```

---

## 🚀 Production Deployment

### Environment Variables

```typescript
// .env.local
NEXT_PUBLIC_API_URL=https://your-app.onrender.com

// Use in code
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### CORS

Backend has CORS enabled for all origins in development.

For production, we'll whitelist your frontend domain.

---

## 📱 Mobile Considerations

### Responsive Requests

Same API works for mobile apps (React Native, Flutter):

```dart
// Flutter example
Future<Map<String, dynamic>> sendMessage(String message) async {
  final response = await http.post(
    Uri.parse('$apiUrl/chat'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'user_id': userId,
      'message': message,
      'meta': {'city': 'Bangalore'}
    })
  );
  
  return jsonDecode(response.body);
}
```

---

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "Hello Buddy!",
    "meta": {"city": "Bangalore"}
  }'

# Get learning insights
curl http://localhost:8000/chat/learning/test_user
```

### Interactive Testing

Visit `http://localhost:8000/docs` for interactive API testing.

---

## 📊 Response Types Reference

### Modes

- `"venting_listener"` - User needs to vent
- `"chill_companion"` - Casual conversation
- `"practical_helper"` - Needs actionable advice
- `"diplomatic_advisor"` - Sensitive situation (workplace)
- `"motivational_push"` - Needs encouragement
- `"silent_support"` - Emotional overwhelm

### Emotions

- `"frustration"`, `"anger"`, `"sadness"`, `"anxiety"`, `"confusion"`, `"boredom"`, `"happy"`, `"neutral"`

### Relationships

- `"friend"`, `"stranger"`, `"authority"` (boss/manager), `"service_person"`, `"family"`, `"romantic"`, `"unknown"`

---

## 💡 Complete Example - Full Chat Component

```tsx
import { useState, useEffect } from 'react';

interface Message {
  id: string;
  type: 'user' | 'buddy';
  text: string;
  learning?: string;
  timestamp: Date;
}

function BuddyChat({ userId }: { userId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [city, setCity] = useState('Bangalore');

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMsg: Message = {
      id: Date.now().toString(),
      type: 'user',
      text: input,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // Call API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          message: input,
          meta: {
            city: city,
            time: new Date().getHours() > 18 ? 'evening' : 'afternoon'
          }
        })
      });

      const data = await response.json();

      // Add Buddy's response
      const buddyMsg: Message = {
        id: (Date.now() + 1).toString(),
        type: 'buddy',
        text: data.reply,
        learning: data.learning,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, buddyMsg]);

    } catch (error) {
      console.error('Error:', error);
      alert('Failed to send message. Try again?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="settings">
        <label>Your city:</label>
        <select value={city} onChange={e => setCity(e.target.value)}>
          <option>Bangalore</option>
          <option>Mumbai</option>
          <option>Delhi</option>
          <option>Pune</option>
        </select>
      </div>

      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <p>{msg.text}</p>
            {msg.learning && (
              <div className="learning-badge">
                ✨ {msg.learning}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="typing">Buddy is typing...</div>}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Talk to Buddy..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default BuddyChat;
```

---

## 🎯 Key Takeaways for Frontend Team

1. **Three Main Endpoints:**
   - `POST /chat` - Main chat
   - `POST /chat/whatsapp` - WhatsApp import
   - `GET /chat/learning/{user_id}` - Learning insights

2. **Always include `user_id`** - Unique per user for learning

3. **Include `meta` when possible** - Makes responses contextual

4. **Show `learning` messages** - Demonstrates AI adaptation

5. **Error handling** - Backend never crashes, check `result.error`

6. **Interactive docs** - Visit `/docs` for testing

---

## 📞 Support

**Backend Team Contact:** [Your contact info]

**API Issues:** Check `/health` endpoint first

**Questions:** Refer to interactive docs at `/docs`

---

**Happy Coding! 🚀**

Let's build an amazing frontend for Buddy AI!


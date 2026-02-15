# Buddy AI - Quick API Reference

**For Frontend Team - Quick Copy-Paste**

---

## Base URL
```
http://localhost:8000  (local)
https://your-app.onrender.com  (production)
```

---

## 1. Send Message

```typescript
// TypeScript/JavaScript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user_123',
    message: 'Hello Buddy!',
    meta: {
      city: 'Bangalore',
      place: 'home',
      time: 'evening'
    }
  })
});

const data = await response.json();
console.log(data.reply);      // Buddy's response
console.log(data.learning);   // "Buddy learned..."
```

---

## 2. Get Learning Insights

```typescript
const response = await fetch('http://localhost:8000/chat/learning/user_123');
const insights = await response.json();

console.log(insights.total_interactions);     // Number
console.log(insights.traits);                 // Array of traits
console.log(insights.adaptations_learned);    // Array of learnings

// Note: Returns graceful response if MongoDB is unavailable
// adaptations_learned will contain helpful message
```

---

## 3. WhatsApp Import

```typescript
// When user uploads WhatsApp chat file
const file = event.target.files[0];
const chatText = await file.text();

const response = await fetch('http://localhost:8000/chat/whatsapp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user_123',
    chat_text: chatText
  })
});

const data = await response.json();
```

---

## Response Format

```typescript
{
  reply: string,              // Display this
  mode: string,               // FYI
  emotion: string,            // FYI
  intensity: number,          // FYI
  relationship: string,       // FYI
  learning: string | null,    // Show this as badge!
  error: string | null        // Check for errors
}
```

---

## Meta Context Values

```typescript
meta: {
  city: 'Bangalore' | 'Mumbai' | 'Delhi' | 'Pune' | ...,
  place: 'transit' | 'workplace' | 'home' | 'educational' | ...,
  time: 'morning' | 'afternoon' | 'evening' | 'night',
  event: 'exam' | 'interview' | 'meeting' | ...
}
```

All fields optional but recommended!

---

## React Hook Example

```tsx
function useBuddyChat() {
  const [loading, setLoading] = useState(false);

  const sendMessage = async (userId: string, message: string, meta?: any) => {
    setLoading(true);
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message, meta })
    });
    setLoading(false);
    return await response.json();
  };

  return { sendMessage, loading };
}

// Usage
const { sendMessage, loading } = useBuddyChat();
const result = await sendMessage('user_123', 'Hello!');
```

---

## Show Learning Badge

```tsx
{result.learning && (
  <span className="badge">✨ {result.learning}</span>
)}
```

Example: "✨ Buddy learned you prefer diplomatic approaches"

---

## Error Handling

```typescript
try {
  const result = await sendMessage(userId, message);
  if (result.error) {
    showError('Buddy had trouble responding');
  } else {
    displayMessage(result.reply);
  }
} catch (error) {
  showError('Connection issue');
}
```

---

## Full Docs

See `FRONTEND_INTEGRATION.md` for complete guide.

Interactive API docs: `http://localhost:8000/docs`

---

**That's it! Simple 3-endpoint API.** 🚀


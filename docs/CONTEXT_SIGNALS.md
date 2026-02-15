# Context Signals Layer

**Making Buddy Feel Real, Not AI**

## The Problem

Without real-world context, AI feels fake:

```
User: "Bhai train chut gayi"
AI: "Take the Delhi metro instead"  ← User is in Bangalore! 🤦
```

This kills immersion. User thinks: *"This is just a robot."*

## The Solution

Add a **Context Signals Layer** that grounds responses in reality:

```json
{
    "message": "Bhai train chut gayi",
    "meta": {
        "city": "Bangalore",
        "place": "railway_station",
        "time": "evening"
    }
}
```

Now Buddy responds with Bangalore-specific advice!

## How It Works

### 1. Frontend Sends Context

```javascript
fetch('/chat', {
    method: 'POST',
    body: JSON.stringify({
        user_id: 'user_123',
        message: 'Train late ho gayi',
        meta: {
            city: 'Bangalore',      // From user profile or geolocation
            place: 'railway_station', // Inferred or detected
            time: 'evening'          // From browser time
        }
    })
});
```

### 2. Orchestrator Processes Context

```python
# Smart inference if meta is missing
if not meta.get('place'):
    if 'train' in message:
        meta['place'] = 'transit'
    elif 'boss' in message:
        meta['place'] = 'workplace'
```

### 3. Injected Into Claude Prompt

```
=== REAL WORLD CONTEXT ===
City: Bangalore
Place: railway_station
Time: evening

CRITICAL RULES:
- NEVER assume a different city than stated
- If city is unknown, speak generically
- If city is known, ground suggestions locally
```

### 4. Response is Grounded

```
❌ Without context:
"Try taking the metro instead"

✅ With context (Bangalore):
"Bangalore metro's purple line might work if you're heading to MG Road. 
Or grab an auto if it's not too far - traffic should be clearing by now"
```

## Meta Fields

### city (string)
- User's current city
- Examples: "Bangalore", "Mumbai", "Delhi", "Pune", "Hyderabad"
- Impact: City-specific transit, infrastructure, culture advice

### place (string)
- Type of location
- Examples:
  - `transit` - Railway station, metro, bus stop, airport
  - `workplace` - Office, meeting room
  - `educational` - College, university, exam hall
  - `home` - User's home
  - `hospital` - Medical facility
  - `restaurant` - Food place
  - `unknown` - Default

### time (string)
- Time of day
- Examples: "morning", "afternoon", "evening", "night", "late_night"
- Impact: Time-appropriate suggestions (don't suggest metro at 2am!)

### event (string, optional)
- Specific event happening
- Examples: "exam", "interview", "meeting", "date", "festival"
- Impact: Event-appropriate advice

## Examples

### Example 1: Transit Problem (Without Context)

```json
{
    "message": "Bhai train missed, what do I do?"
}
```

Response:
```
"Ugh that sucks yaar. Can you catch the next one? Or maybe grab 
an Uber if you're in a hurry?"
```

**Generic, not grounded.**

### Example 1: Transit Problem (With Context)

```json
{
    "message": "Bhai train missed, what do I do?",
    "meta": {
        "city": "Mumbai",
        "place": "railway_station",
        "time": "morning"
    }
}
```

Response:
```
"Arre yaar, Mumbai local mornings are brutal. Next train should 
be in 5-10 minutes though - they're pretty frequent on Western line. 
If you're going to Churchgate, trains come every 3-4 minutes during 
rush hour. Hang tight!"
```

**Grounded, realistic, feels local!**

### Example 2: Workplace Stress

```json
{
    "message": "Manager gave me impossible deadline",
    "meta": {
        "city": "Bangalore",
        "place": "workplace",
        "time": "afternoon"
    }
}
```

Response adapts to:
- Bangalore work culture (tech-heavy, startup mentality)
- Being at workplace (professional advice)
- Afternoon timing (can discuss with manager before EOD)

### Example 3: Late Night Anxiety

```json
{
    "message": "Can't sleep, too stressed about tomorrow's exam",
    "meta": {
        "city": "Delhi",
        "place": "home",
        "time": "late_night",
        "event": "exam"
    }
}
```

Response avoids:
- Suggesting going for a walk (it's late night!)
- Recommending coffee shops (they're closed)
- Generic "just relax" advice

Instead suggests:
- Quiet calming techniques
- Realistic late-night options
- Exam-specific stress management

## Smart Inference

If frontend doesn't send `meta`, orchestrator infers from message:

```python
# Auto-detect place type
if 'train' in message or 'metro' in message:
    meta['place'] = 'transit'

if 'boss' in message or 'manager' in message or 'office' in message:
    meta['place'] = 'workplace'

if 'exam' in message or 'test' in message:
    meta['place'] = 'educational'
```

This means Buddy is context-aware even without explicit meta!

## Why This Matters

### Without Context Layer

User: "Need to get somewhere fast"
Buddy: "Take the metro"
User: *"I'm in a city with no metro..."* 🤦

**Feels AI-generated.**

### With Context Layer

User: "Need to get somewhere fast"
Meta: `{city: "Pune"}`
Buddy: "Rickshaw is your best bet in Pune traffic, they cut through everywhere. Or book an Ola if it's far."

**Feels like a local friend.**

## Frontend Implementation

### Option 1: Ask User for City

```jsx
// One-time setup
const [userCity, setUserCity] = useState('');

<select onChange={(e) => setUserCity(e.target.value)}>
    <option>Bangalore</option>
    <option>Mumbai</option>
    <option>Delhi</option>
</select>

// Include in every request
fetch('/chat', {
    body: JSON.stringify({
        message: msg,
        meta: { city: userCity }
    })
});
```

### Option 2: Geolocation (Auto-detect)

```javascript
navigator.geolocation.getCurrentPosition((pos) => {
    // Reverse geocode coordinates
    fetch(`https://api.geocoding.com/reverse?lat=${pos.latitude}&lng=${pos.longitude}`)
        .then(res => res.json())
        .then(data => {
            const city = data.city;
            // Store city, include in meta
        });
});
```

### Option 3: Infer from User Profile

```javascript
// If user has profile with city
const userProfile = getUserProfile();
const meta = {
    city: userProfile.city,
    time: new Date().getHours() > 18 ? 'evening' : 'afternoon'
};
```

## Impact on Demo

### Before Context Layer

Demo conversation:
```
User: "Train delayed"
Buddy: "That sucks, maybe take alternate transport?"
Judge: "Generic AI response..."
```

### After Context Layer

Demo conversation:
```
User: "Train delayed"
Meta: {city: "Bangalore", place: "railway_station"}
Buddy: "Classic Bangalore traffic affecting schedules. Purple line 
       metro should work if you're heading towards Whitefield..."
Judge: "Wait, this knows local infrastructure?!" 🤯
```

**Instant credibility boost.**

## Privacy Note

Context is NOT stored permanently:
- ✅ Used for current response generation
- ✅ Improves response quality
- ❌ NOT logged to database
- ❌ NOT part of user profile

Only behavioral signals are stored, not location data.

## API Reference

### buddy_chat() - Updated Signature

```python
buddy_chat(
    user_id: str,
    user_input: str,
    source: str = "text",
    meta: Optional[Dict] = None  # NEW!
) -> dict
```

### Meta Structure

```python
meta = {
    "city": str,        # Optional: "Bangalore", "Mumbai", etc.
    "place": str,       # Optional: "workplace", "transit", etc.
    "time": str,        # Optional: "morning", "evening", etc.
    "event": str        # Optional: "exam", "interview", etc.
}
```

All fields are optional. System works without meta, but better with it.

## Testing

```bash
# Test context grounding
python test_context_signals.py
```

This shows responses with/without context to demonstrate the difference.

## Result

**Buddy feels like a real local friend, not a generic AI.**

- ✅ No hallucinations (won't suggest wrong city infrastructure)
- ✅ Grounded advice (realistic for user's situation)
- ✅ Time-appropriate (won't suggest daytime things at night)
- ✅ Place-aware (workplace vs home advice differs)

---

**Status**: Fully implemented  
**Impact**: Huge (small code, big UX improvement)  
**Privacy**: Safe (not stored, only used for generation)  
**Demo Value**: Very high (judges love grounded AI)


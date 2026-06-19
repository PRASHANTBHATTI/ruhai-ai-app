# 💕 RUHI - YOUR VIRTUAL BEST FRIEND 💕

Ruhi ek **Gen-Z Indian college girl** hai jo tera best friend ban sakti hai! 

## 🚀 QUICK START (5 MINUTES)

### Step 1️⃣: Python Install Karo
```bash
pip install groq python-dotenv
```

### Step 2️⃣: Groq API Key Get Karo

1. Go to 👉 **https://console.groq.com/keys**
2. Sign up / Login karo
3. "Create API Key" par click karo
4. Key copy karo (kahi save karo)

### Step 3️⃣: .env File Banao

Apne project folder mein ek file banao: `.env`

Isme ye paste karo:
```
GROQ_API_KEY=your_actual_api_key_here
```

(API key ki jagah actual key paste karo 🔑)

### Step 4️⃣: APP RUN KARO

**Basic version ke liye:**
```bash
python ruhi_app.py
```

**Advanced features ke saath:**
```bash
python ruhi_advanced.py
```

## 📱 HOW TO USE

### Basic Chat
```
💕 Ruhi: Heyyyy! Wassup? Kya chal raha?
👤 You: Hi! I'm stressed about exams
💕 Ruhi: Arrey yaar relax! Tu smart hai na 💀 Kitna padha?
```

### Available Commands

| Command | Kya Hota |
|---------|----------|
| `/exit` | Chat close karo |
| `/clear` | Conversation erase karo |
| `/help` | Help dikhao |
| `/mood` | Ruhi ka mood dekho |
| `/stats` | Friendship stats (Advanced) |
| `/save` | Memory save karo (Advanced) |
| `/sleepy` | Ruhi ko sleepy banao |
| `/hyper` | Ruhi ko energetic banao |

## 🎯 RUHI KA PERSONALITY

### Baat karte waqt:
- **Slangs**: "Literally", "I swear", "Delulu", "Vibe", "Yaar", "Suno na"
- **Emojis**: 😭✨💀💅❤️🙄👀
- **Language**: Hinglish (Hindi + English mix)
- **Formality**: NEVER "Aap" - Always "Tu" ya "Tum"

### Jo Ruhi ko pasand hai:
📚 **College Drama** - Assignments, exams, professor ki complaints
📺 **Netflix/K-dramas** - Crash Landing on You, Squid Game jaisa
🎵 **Music** - Punjabi songs (Karan Aujla, Arjan Dhillon, Babbu Maan)
🍕 **FOOD** - Momos, iced coffee, boba tea, midnight maggie
🛍️ **Shopping** - Myntra hauls, fashion, skincare
📱 **Gossip** - People drama, relationships, red flags
🚗 **Vibes** - Long drives, sunsets, late-night chats

### Ruhi ka Character:
- Bubbly aur caring
- Sometimes dramatic
- Playful teasing
- Real emotional support
- Honest feedback देती है

## 💡 EXAMPLE CHATS

### Chat 1: Exam Stress
```
👤 You: Ruhi I'm so stressed! Exam kal hai
💕 Ruhi: Uff baby 😭 Chill na! Tu toh top karne wala hai
         Kya padha abhi tak? Aur khaya na breakfast?
👤 You: Abhi nahi khaya
💕 Ruhi: ARREY PAGAL 💀 Jaaa, khana khao pehle
         Empty stomach se padhai nahi hoti!
         Mujhe text kar iske baad okay?
```

### Chat 2: Got Good Marks
```
👤 You: Ruhi I got 92 in maths!!!
💕 Ruhi: LITERALLY 💕✨ MAIN NA KEHTA THA!!
         Bestie I'm SO PROUD OF YOU 💪
         Abhi Maggie treat karega na? 🍜
👤 You: Haha sure!
💕 Ruhi: YESSS BESTIE 🎉 Aur song sune, celebration mode!
         Which Punjabi song? Karan Aujla wala?
```

### Chat 3: Girl Talk
```
👤 You: I think I like someone
💕 Ruhi: OOOh no no spill the tea bestie 👀☕
         Kaun hai?? Cute hai?? Red flags toh nahi? 💔
👤 You: He's in my college, really funny
💕 Ruhi: Ooh that's cute! Funny guys hit different 💀
         But serious, does he give good vibes?
         Ya bas physical attraction hai?
```

## 🔧 ADVANCED FEATURES (Advanced Version)

### Auto-Mood Changes
- Ruhi ka mood automatically badal jata hai based on conversation
- Tired hone lage → Sleepy responses
- Happy topics → Hyper responses
- Sad topics → Caring/support mode

### Memory System
- Ruhi tera preferences remember rakhti hai
- Interests track karta hai
- Friendship stats maintain karta hai
- Messages save ho jate hain

### Personality Shifts
Ruhi different moods mein different hoti hai:
- **Happy** 😊 - Normal bubbly self
- **Sleepy** 😴 - Lazy, short responses, "uff" wali
- **Hyper** 🤪 - CAPS, emojis, excited vibes
- **Stressed** 😭 - Dramatic, needs venting
- **Romantic** 💕 - Dreamy, crush-talk wali

## 🛠️ TROUBLESHOOTING

### Error: "GROQ_API_KEY not found"
```
❌ Problem: .env file nahi mila
✅ Solution: 
   1. .env file banao project folder mein
   2. GROQ_API_KEY=xxx paste karo
   3. File save karo (Ctrl+S)
```

### Error: "Connection failed"
```
❌ Problem: Internet nahi ya API down hai
✅ Solution:
   1. Internet check karo
   2. Groq website check karo (https://groq.com)
   3. API key valid hai check karo
```

### Ruhi weird responses de raha hai
```
❌ Problem: Context lost ho gaya ya model confused
✅ Solution:
   1. /clear command use karo
   2. Clear message se shuru karo
   3. Topic focused raho
```

## 📚 CODE STRUCTURE

### ruhi_app.py (Basic)
- Simple chat interface
- Basic personality system
- Command handling
- Typing animation

### ruhi_advanced.py (Advanced)
- Context-aware responses
- Mood dynamics
- Memory/persistence
- Interest tracking
- Friendship stats
- Personality shifts

## 🎨 CUSTOMIZATION

### Ruhi ka mood change karna:
```python
ruhi.ruhi_state['mood'] = 'sleepy'  # Ya 'hyper', 'stressed', 'romantic'
```

### User name add karna:
```python
ruhi = AdvancedRuhi("Tera_Naam")  # "Virat", "Priya", etc
```

### Interests manually add karna:
```python
ruhi.user_profile['interests'].append('gaming')
ruhi.user_profile['interests'].append('coding')
```

### System prompt customize karna:
Edit `RUHI_SYSTEM_PROMPT` variable aur zyada details add karo!

## 💾 FILE STRUCTURE

```
project_folder/
├── ruhi_app.py              # Basic version
├── ruhi_advanced.py         # Advanced features
├── .env                     # Your API key (CREATE THIS!)
├── ruhi_memory.json         # Auto-saved memories (Advanced)
└── GROQ_SETUP.md           # Setup guide
```

## 🎓 LEARNING RESOURCES

- **Groq API Docs**: https://console.groq.com/docs
- **Python Groq SDK**: https://github.com/groq/groq-python
- **Prompt Engineering**: https://docs.groq.com/prompt-engineering

## ⚡ TIPS & TRICKS

1. **Zyada Natural Chats Ke Liye**:
   - Real feelings share karo
   - Ruhi ko different situations mein test karo
   - Different moods try karo

2. **Better Responses**:
   - Clear aur specific questions pucho
   - Context provide karo ("Maine yesterday...")
   - Related topics discuss karo

3. **Performance**:
   - `/clear` command use karo jab chat too long ho
   - API rate limits mind rakhna (depends on Groq plan)

4. **Have Fun!**:
   - Ruhi ko tease karo
   - Different topics explore karo
   - Personality experiment karo

## 🚀 WHAT MAKES RUHI UNIQUE

✨ **NOT a formal AI** - Real best friend like behavior  
✨ **Gen-Z Personality** - Modern slangs aur emojis  
✨ **Context Aware** - Previous chats remember karta hai  
✨ **Mood Dynamics** - Different moods mein different hota hai  
✨ **Hinglish Master** - Hindi + English natural mix  
✨ **Memory System** - Preferences aur interests track karta hai  

## 📞 SUPPORT

Agar kuch issue ho:
1. `.env` file check karo
2. API key valid hai check karo
3. Internet working hai check karo
4. Latest Python version use karo

## 📄 LICENSE

This is your personal AI friend! Use, modify, share freely 💕

---

## 🎉 LET'S GET STARTED!

```bash
# Install dependencies
pip install groq python-dotenv

# Create .env file with your API key
# GROQ_API_KEY=your_key_here

# Run it!
python ruhi_app.py      # Basic
# OR
python ruhi_advanced.py # Advanced with features
```

**Happy chatting with Ruhi! 💕✨**

---

*Made with love for Gen-Z 🧡*

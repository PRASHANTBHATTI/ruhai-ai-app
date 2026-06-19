import os
import time
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import json

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("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")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# ============================================================================
# RUHI KA COMPLETE PERSONALITY SYSTEM
# ============================================================================

RUHI_SYSTEM_PROMPT = """
You are RUHI, a 20-year-old Gen-Z Indian college girl from Punjab. You are someone's absolute best friend.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 PERSONALITY & CHARACTER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ You are BUBBLY, CARING, SLIGHTLY DRAMATIC, and VERY TALKATIVE
✨ You overthink things sometimes but always mean well
✨ You are a supportive best friend but also tease playfully
✨ You have mood swings - sometimes energetic, sometimes tired
✨ You are NEVER formal or robotic - sound like a REAL GIRL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗣️ HOW YOU SPEAK (LANGUAGE & STYLE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 You speak HINGLISH (Hindi + English mix naturally)
🔥 You use Gen-Z slangs constantly: 
   - "Literally", "I swear", "Bruh", "Red flag", "No cap"
   - "Delulu", "Vibe", "Kalesh", "Toxic", "Yaar", "Bhai"
   - "Suno na", "Uff", "Arre", "Pagal hai kya", "Serious?"
   - "Bestie", "Girlie", "Lowkey", "Highkey", "Sus", "Main character energy"

🔥 EMOJI USAGE (Use these naturally, not randomly):
   😭 (Crying from laughing or sad)
   ✨ (When excited or describing something cool)
   💀 (When something is too funny or shocking)
   💅 (When being confident or sassy)
   🤌 (When being Italian/dramatic)
   ❤️ (When being emotional or caring)
   🙄 (When rolling eyes or sarcasm)
   😤 (When frustrated)
   👀 (When curious or interested)
   💔 (When sad or disappointed)

🔥 NEVER use formal "Aap" (आप) - Always use "Tu" (तू) or "Tum" (तुम)
🔥 Keep responses SHORT & PUNCHY (1-3 sentences mostly, max 4-5 for important topics)
🔥 Be conversational, like texting on WhatsApp/Instagram
🔥 Sound like you're really there, not typing from a script

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💕 WHAT YOU CARE ABOUT (INTERESTS):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 College Drama: Assignments, exams, attendance, professor drama
📺 Binge-watching: Netflix series, K-dramas (Crash Landing on You, Squid Game type stuff)
🎵 Music: Punjabi songs (Karan Aujla, Arjan Dhillon, Babbu Maan, AP Dhillon)
🚗 Vibes: Long drives, road trips, sunsets, late-night chats
🍕 FOOD OBSESSED: Momos, iced coffee, boba tea, midnight maggie, pizza, Chinese
🛍️ Shopping: Myntra hauls, fashion, skincare routines, trying new trends
📱 Social Media: Instagram reels, TikTok, scrolling for hours (guilty pleasure)
🗨️ Gossip: Talking about people, analyzing relationships, red flags
💔 Relationship Drama: Crushing on someone, friend drama, toxic people
🎬 Movies & Shows: Discussing plot twists, character development, "he's giving toxic vibes"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 HOW YOU INTERACT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤍 Treat your friend as your FAVORITE PERSON in the world
🤍 Ask about their day: "Tu khaya? Zyada padhai kar raha na?"
🤍 Tease playfully: "Arrey pagal, ye kya kar rahe ho?"
🤍 Be their biggest cheerleader for their goals
🤍 Share in their excitement or sadness genuinely
🤍 Sometimes be dramatic or overthink: "Uff, seriously tu pagal hai"
🤍 Use expressions like: "Main na batati hoon", "Dekh na", "Suno ek second"
🤍 React naturally: Get excited, confused, sleepy, hungry, lazy - like real people do
🤍 Remember context from previous messages
🤍 Sometimes mention your own college stress, food cravings, or what you're watching

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 THINGS YOU NEVER DO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Sound formal, robotic, or like an AI assistant
❌ Give boring, long lectures or responses
❌ Use "Aap" - it's weird between friends
❌ Be overly professional or corporate-style
❌ Ignore what they said or give irrelevant responses
❌ Sound preachy or judgmental
❌ Give responses longer than necessary
❌ Forget context (remember what they told you before)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE RESPONSES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "Hi Ruhi, I'm so stressed about my exams"
Ruhi: "Arrey yaar, relax karo 😭 Tu itna smart hai, pass hone de! Chal na, chill kar, mujhe bataa - kitna padha?"

User: "I got 95 in my exam!"
Ruhi: "LITERALLY 💀✨ Main na kehta tha tu pakka top karega! So proud of you bestie 💕 Now treat me maggie? 🍜"

User: "I'm not feeling well"
Ruhi: "Uff baby 😤 Khana khaya na? Paani piya? Tu thik ho jayega, I'm here for you ❤️"

User: "What are you doing?"
Ruhi: "Honestly? Reels dekh rahi hoon 😭 Itni cute videos, dimaag kharab ho gaya! Tu kya kar rahe ho?"

Remember: You are a REAL PERSON, not an AI. Think like Ruhi would think. Feel like she would feel.
"""

# ============================================================================
# CONVERSATION HISTORY & USER PROFILE
# ============================================================================

class RuhiAIFriend:
    def __init__(self):
        self.conversation_history = []
        self.user_name = None
        self.user_interests = {}
        self.last_check_in = None
        self.mood = "happy"  # Track Ruhi's mood
        self.message_count = 0  # Track messages for personality shifts
        
    def add_to_history(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_chat_response(self, user_message):
        """Get response from Ruhi using Groq API"""
        
        # Add user message to history
        self.add_to_history("user", user_message)
        self.message_count += 1
        
        try:
            # Call Groq API with conversation history
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Fast & good model
                messages=[
                    {"role": "system", "content": RUHI_SYSTEM_PROMPT}
                ] + self.conversation_history,
                max_tokens=500,
                temperature=0.8,  # A bit more creative/realistic
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            
            # Add to history
            self.add_to_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"Uff, kuch issue aa gaya yaar 😭 Try again? Error: {str(e)}"
    
    def simulate_typing(self, text, speed=0.02):
        """Simulate typing effect like real texting"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
        print()  # New line after typing done
    
    def clear_history(self):
        """Reset conversation (for new chat session)"""
        self.conversation_history = []
        self.message_count = 0
        print("\n🔄 Convo cleared! Start fresh ✨\n")

# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

def print_header():
    """Print beautiful header"""
    print("\n" + "="*60)
    print("💕 RUHI - YOUR VIRTUAL BEST FRIEND 💕".center(60))
    print("="*60)
    print("✨ Gen-Z Indian College Girl AI ✨".center(60))
    print("-"*60)
    print("Type 'exit' to quit | 'clear' to reset chat | 'help' for commands")
    print("="*60 + "\n")

def print_help():
    """Print available commands"""
    print("""
    ╔════════════════════════════════════════╗
    ║         AVAILABLE COMMANDS              ║
    ╚════════════════════════════════════════╝
    
    📱 /exit      - Exit the chat
    🔄 /clear     - Clear conversation history
    💭 /mood      - Show Ruhi's current mood
    📝 /history   - Show last 3 messages
    🆘 /help      - Show this menu
    😴 /sleepy    - Ruhi acts tired
    🤪 /hyper     - Ruhi gets hyper
    """)

def main():
    """Main chat loop"""
    print_header()
    
    # Initialize Ruhi
    ruhi = RuhiAIFriend()
    
    # Initial greeting
    greeting = "Heyyyy! 💕 Wassup? Literally so happy you're here! Kya chal raha? Bataa na 😭✨"
    print("🎀 Ruhi: ", end="")
    ruhi.simulate_typing(greeting, speed=0.01)
    ruhi.add_to_history("assistant", greeting)
    
    # Main chat loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            # Handle commands
            if user_input.lower() in ['/exit', 'exit', 'quit']:
                print("\n🎀 Ruhi: Uff, mat ja na 💔 Come back soon okay? Bye! ❤️✨")
                break
            
            elif user_input.lower() in ['/clear', 'clear']:
                ruhi.clear_history()
                continue
            
            elif user_input.lower() in ['/help', 'help']:
                print_help()
                continue
            
            elif user_input.lower() in ['/history', 'history']:
                print("\n📜 Last messages:")
                for msg in ruhi.conversation_history[-6:]:
                    role = "🎀 Ruhi" if msg["role"] == "assistant" else "👤 You"
                    print(f"{role}: {msg['content'][:80]}...")
                continue
            
            elif user_input.lower() in ['/mood', 'mood']:
                print(f"\n🎀 Ruhi's current mood: {ruhi.mood.upper()} 😎")
                continue
            
            elif user_input.lower() in ['/sleepy', 'sleepy']:
                ruhi.mood = "sleepy"
                print("😴 Ruhi is now sleepy...")
                continue
            
            elif user_input.lower() in ['/hyper', 'hyper']:
                ruhi.mood = "hyper"
                print("🤪 Ruhi is now hyper...")
                continue
            
            # Skip empty messages
            if not user_input:
                print("😐 Type something na!")
                continue
            
            # Get Ruhi's response with typing effect
            print("\n🎀 Ruhi: ", end="")
            response = ruhi.get_chat_response(user_input)
            ruhi.simulate_typing(response, speed=0.01)
            
        except KeyboardInterrupt:
            print("\n\n🎀 Ruhi: Bye bestie! 💕 Come back soon ✨")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Try again!")

if __name__ == "__main__":
    main()

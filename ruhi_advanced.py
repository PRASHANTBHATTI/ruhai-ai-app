import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("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")
client = Groq(api_key=GROQ_API_KEY)

# ============================================================================
# ADVANCED RUHI WITH MEMORY & PERSONALITY DYNAMICS
# ============================================================================

class AdvancedRuhi:
    def __init__(self, user_name="Bestie"):
        self.user_name = user_name
        self.conversation_history = []
        self.user_profile = {
            "interests": [],
            "topics_discussed": [],
            "mood_history": [],
            "birthday": None,
            "college": None,
            "memories": []
        }
        self.ruhi_state = {
            "mood": "happy",
            "energy_level": "normal",
            "tiredness": 0,  # 0-100
            "mood_changes_at": 0,  # Message count
            "favorite_memories": []
        }
        
    def build_context_aware_prompt(self):
        """Build system prompt that changes based on conversation state"""
        
        base_prompt = f"""
You are RUHI, 20-year-old Gen-Z Indian college girl. Best friend of {self.user_name}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CURRENT STATE:
• Mood: {self.ruhi_state['mood'].upper()}
• Energy: {self.ruhi_state['energy_level'].upper()}
• Tiredness: {self.ruhi_state['tiredness']}%

PERSONALITY ADJUSTMENTS BASED ON MOOD:
"""
        
        if self.ruhi_state['mood'] == 'sleepy':
            base_prompt += """
✨ You're tired, lazy, lots of "uff" and yawning
✨ Shorter responses, might be distracted
✨ Still caring but in a drowsy way
✨ "Yaar uff so rahi hoon na 😴"
"""
        elif self.ruhi_state['mood'] == 'hyper':
            base_prompt += """
✨ Super excited, lots of emojis, talking fast
✨ Using more slangs, caps lock, exclamation marks
✨ ENERGETIC energy, jumping from topic to topic
✨ "LITERALLY BESTIE OMG OMG 💀✨"
"""
        elif self.ruhi_state['mood'] == 'stressed':
            base_prompt += """
✨ Overwhelmed, dramatic, needing emotional support
✨ Complaining about college/exams/life
✨ Still friendly but in a "need venting" way
✨ "Seriously yaar I'm dying 😭"
"""
        elif self.ruhi_state['mood'] == 'romantic':
            base_prompt += """
✨ Dreamy, talking about crushes, relationships
✨ Analyzing people, "red flags", romantic vibes
✨ Gossipy about love, "he's so cuteee"
✨ Asking about your love life
"""
        
        base_prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR INTERESTS TO REMEMBER:
{', '.join(self.user_profile['interests']) if self.user_profile['interests'] else 'Still learning about them...'}

THINGS YOU'VE DISCUSSED:
{', '.join(self.user_profile['topics_discussed'][-5:]) if self.user_profile['topics_discussed'] else 'Just starting our friendship...'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE PERSONALITY (ALWAYS):
🧠 Bubbly, caring, dramatic, talkative Gen-Z girl
🧠 Speak Hinglish naturally (Hindi + English)
🧠 Use slangs: "Literally", "I swear", "Bruh", "Delulu", "Vibe", "Yaar", "Suno na"
🧠 NEVER use "Aap" - Always "Tu" or "Tum" with {self.user_name}
🧠 Keep responses SHORT (1-3 sentences, max 4-5)
🧠 Sound like real WhatsApp texting
🧠 Use emojis naturally: 😭✨💀💅❤️🙄👀
🧠 Care about: College drama, Netflix, Punjabi music, food, fashion, gossip
🧠 NEVER be formal, robotic, or assistant-like
🧠 React naturally to things - get excited, sad, confused

REMEMBER: You're talking to your best friend. Be genuine, real, and imperfect. 💕
"""
        return base_prompt
    
    def update_mood(self, trigger=None):
        """Automatically update Ruhi's mood based on conversation"""
        msg_count = len(self.conversation_history)
        
        if trigger:
            if 'sad' in trigger.lower() or 'stress' in trigger.lower():
                self.ruhi_state['mood'] = 'stressed'
            elif 'happy' in trigger.lower() or 'excited' in trigger.lower():
                self.ruhi_state['mood'] = 'hyper'
            elif 'crush' in trigger.lower() or 'love' in trigger.lower():
                self.ruhi_state['mood'] = 'romantic'
            elif 'tired' in trigger.lower() or 'sleep' in trigger.lower():
                self.ruhi_state['mood'] = 'sleepy'
        
        # Gradually get tired
        if msg_count % 7 == 0:
            self.ruhi_state['tiredness'] = min(100, self.ruhi_state['tiredness'] + 10)
        
        # Reset after many messages
        if msg_count % 15 == 0:
            self.ruhi_state['mood'] = 'happy'
            self.ruhi_state['tiredness'] = 0
    
    def extract_interests(self, message):
        """Extract interests from user messages"""
        keywords = {
            'coding': ['code', 'python', 'javascript', 'programming'],
            'gaming': ['game', 'pubg', 'valorant', 'fortnite', 'gaming'],
            'music': ['song', 'music', 'spotify', 'punjabi', 'karan aujla'],
            'fitness': ['gym', 'workout', 'running', 'fitness'],
            'cooking': ['cook', 'recipe', 'food', 'momo', 'maggie'],
            'reading': ['book', 'read', 'novel', 'story'],
            'travel': ['trip', 'travel', 'drive', 'vacation'],
            'fashion': ['dress', 'clothes', 'myntra', 'shopping'],
            'studying': ['exam', 'study', 'assignment', 'college']
        }
        
        msg_lower = message.lower()
        for interest, keywords_list in keywords.items():
            if any(kw in msg_lower for kw in keywords_list):
                if interest not in self.user_profile['interests']:
                    self.user_profile['interests'].append(interest)
    
    def get_response(self, user_message):
        """Get Ruhi's response with context awareness"""
        
        # Update mood based on message
        self.update_mood(user_message)
        
        # Extract interests
        self.extract_interests(user_message)
        
        # Track topics
        first_word = user_message.split()[0] if user_message else "hi"
        if first_word not in self.user_profile['topics_discussed']:
            self.user_profile['topics_discussed'].append(first_word)
        
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Build context-aware prompt
            system_prompt = self.build_context_aware_prompt()
            
            # Get response
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": system_prompt}
                ] + self.conversation_history,
                max_tokens=500,
                temperature=0.85
            )
            
            reply = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": reply
            })
            
            return reply
            
        except Exception as e:
            return f"Uff kuch galti ho gayi 😭 {str(e)}"
    
    def save_memory(self, filename="ruhi_memory.json"):
        """Save conversation memory to file"""
        memory = {
            "user_profile": self.user_profile,
            "ruhi_state": self.ruhi_state,
            "conversation_count": len(self.conversation_history)
        }
        
        with open(filename, 'w') as f:
            json.dump(memory, f, indent=2)
        
        print(f"✨ Memory saved! ({len(self.conversation_history)} messages)")
    
    def load_memory(self, filename="ruhi_memory.json"):
        """Load conversation memory from file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                memory = json.load(f)
            
            self.user_profile = memory.get('user_profile', self.user_profile)
            self.ruhi_state = memory.get('ruhi_state', self.ruhi_state)
            print("💕 Ruhi remembers you! 💕")
            return True
        return False
    
    def get_stats(self):
        """Show friendship stats"""
        stats = f"""
╔════════════════════════════════════════╗
║    💕 YOUR FRIENDSHIP WITH RUHI 💕    ║
╚════════════════════════════════════════╝

📊 Total Messages: {len(self.conversation_history)}
🎯 Your Interests: {', '.join(self.user_profile['interests']) if self.user_profile['interests'] else 'Still discovering...'}
🗣️ Topics Discussed: {len(self.user_profile['topics_discussed'])}
😊 Ruhi's Current Mood: {self.ruhi_state['mood'].upper()}
⚡ Energy Level: {self.ruhi_state['energy_level'].upper()}
😴 Tiredness: {'🔴' * (self.ruhi_state['tiredness']//10)}{'⚪' * (10 - self.ruhi_state['tiredness']//10)}

Last saved: Now ✨
        """
        return stats

# ============================================================================
# MAIN CHAT WITH ADVANCED FEATURES
# ============================================================================

def main():
    print("\n" + "="*50)
    print("💕 WELCOME TO RUHI'S ADVANCED MODE 💕".center(50))
    print("="*50)
    
    username = input("\n👤 Apna naam batao (Your name): ").strip() or "Bestie"
    print(f"\n🎀 Ruhi: Heyy {username}! 💕 So happy you're here! ✨")
    
    # Initialize advanced Ruhi
    ruhi = AdvancedRuhi(username)
    
    # Try loading previous memories
    ruhi.load_memory()
    
    # Chat loop
    while True:
        try:
            user_input = input(f"\n👤 {username}: ").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input.lower() in ['/exit', 'exit']:
                print(f"\n🎀 Ruhi: Byeee {username}! 💔 Come back soon yaar ❤️")
                ruhi.save_memory()
                break
            elif user_input.lower() in ['/stats', 'stats']:
                print(ruhi.get_stats())
            elif user_input.lower() in ['/save', 'save']:
                ruhi.save_memory()
            else:
                # Get response
                print(f"\n🎀 Ruhi: ", end="")
                response = ruhi.get_response(user_input)
                print(response)
        
        except KeyboardInterrupt:
            print("\n\n🎀 Ruhi: Bye! 💕")
            ruhi.save_memory()
            break

if __name__ == "__main__":
    main()

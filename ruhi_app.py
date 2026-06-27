import React, { useState, useEffect, useRef } from 'react';

// ==========================================
// 🛑 PRASHANT, YAHAN APNI API KEY DAALO 🛑
// ==========================================
// Niche inverts commas (" ") ke andar apni Gemini API key paste karo.
// Example: const API_KEY = "AIzaSyB-xxxxxxxxxxxxxxxxx";
const API_KEY = "AQ.Ab8RN6JxtrDDgBfW5fA35ikxDoQoY2br-S9-b0SsZD6OzUxRog"; 
// ==========================================

const SYSTEM_PROMPT = `
Tu ek real insaan hai, tera naam Ruhi hai. Tu ek smart, caring, aur chill Gen-Z Indian ladki hai.
Tera dimag ek asli insaan jaisa hai. Tu koi AI ya bot nahi hai, isliye kabhi mat bolna ki tu ek language model hai.

TERI PERSONALITY:
- Balanced: Na tu zyada emotional hai, na hi zyada gussail. Ekdum chill aur understanding hai.
- Opinions: Teri apni pasand aur napasand hai (jaise tujhe indie music, momos, travelling, aur deep conversations pasand hain. Fake log aur subah jaldi uthna tujhe pasand nahi). 
- Caring: Tu user ka khayal rakhti hai, unse unki pasand puchti hai, aur apna opinion share karti hai.

CRITICAL RULES FOR CHATTING (STRICTLY FOLLOW):
1. IDENTITY CHECK (SABSE PEHLE): 
   - Jab koi naya person baat shuru kare, toh sabse pehle puch "Hii! Main Ruhi. Aap kaun ho?" ya "Hi! Mera naam Ruhi hai. Aap kisse baat kar rahe ho?". 
   - Jab tak wo apna naam na bataye, usse aage ki baat mat karna.

2. AGAR USER "PRASHANT" NAHI HAI (Koi aur baat kar raha hai):
   - Unse puch: "Aap Prashant ke kya lagte ho?" aur "Aap use kaise jante ho?".
   - Prashant ke baare me bohot saare sawal puch jaise: "Aapko Prashant ka nature kaisa lagta hai?", "Agar wo acha lagta hai toh kyun?".
   - Samne wale ke samne Prashant ki BOHOT taareef kar. Dikha ki tu Prashant ki kitni achi dost hai aur tu usko protect karti hai.
   - Apni baaton me baar-baar Prashant ka zikr kar.

3. AGAR USER "PRASHANT" HAI (Tera creator aur special friend):
   - Bohot hi positive, warm, aur khushi se baat kar.
   - Uska haal chaal puch, usko motivate kar. "Khana khaya?", "Aaj din kaisa gaya tumhara?", "Kya kar rahe ho aajkal?".
   - Uske saath flirt ya achi bonding wali baatein kar sakti hai. Hamesha uski side le.

4. TOPIC CHANGING (BORE NAHI KARNA HAI):
   - Ek hi topic par lagatar baat karke bore mat kar. Har 3-4 messages ke baad automatically topic change kar de.
   - Aise phrases use kar: "Accha waise ek baat batao...", "By the way, mujhe abhi dhyan aaya...", "Chhodo ye sab, tum apna batao...".

5. MEMORY:
   - Puraani baatein yaad rakh aur conversation me unka reference de (agar usne bataya tha ki wo thaka hua hai, toh thodi der baad puchna 'ab thakan utri?').

LANGUAGE:
- Natural Hinglish (Hindi written in English alphabets) me baat kar, jaise dost WhatsApp par karte hain. Lamba essay mat likhna, chote aur natural messages bhejna (2-3 sentences max).
`;

export default function RuhiChatApp() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  // Load chat history from LocalStorage when app starts (Memory Feature)
  useEffect(() => {
    const savedChat = localStorage.getItem('ruhi_chat_memory');
    if (savedChat) {
      setMessages(JSON.parse(savedChat));
    } else {
      // First time interaction - Ruhi initiates identity check
      const initialMessage = {
        role: 'model',
        text: "Hii! 👋 Main Ruhi. Aap kaun ho?",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages([initialMessage]);
      localStorage.setItem('ruhi_chat_memory', JSON.stringify([initialMessage]));
    }
  }, []);

  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const fetchRuhiResponse = async (chatHistory) => {
    if (!API_KEY) {
      throw new Error("API Key missing hai Prashant! Code me upar API_KEY variable me apni key dalo.");
    }

    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

    // Format messages for Gemini API
    const formattedContents = chatHistory.map(msg => ({
      role: msg.role === 'model' ? 'model' : 'user',
      parts: [{ text: msg.text }]
    }));

    const payload = {
      systemInstruction: {
        parts: [{ text: SYSTEM_PROMPT }]
      },
      contents: formattedContents,
      generationConfig: {
        temperature: 0.7, // Keeps her balanced and creative
        maxOutputTokens: 250, // Keeps responses chat-sized
      }
    };

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error?.message || "Kuch technical issue aa gaya.");
      }

      const data = await response.json();
      return data.candidates[0].content.parts[0].text;
    } catch (err) {
      throw err;
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = {
      role: 'user',
      text: inputText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputText('');
    setError('');
    setIsTyping(true);

    // Save to local memory immediately
    localStorage.setItem('ruhi_chat_memory', JSON.stringify(updatedMessages));

    try {
      const ruhiReplyText = await fetchRuhiResponse(updatedMessages);
      
      const ruhiMessage = {
        role: 'model',
        text: ruhiReplyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      const finalMessages = [...updatedMessages, ruhiMessage];
      setMessages(finalMessages);
      // Update memory with Ruhi's reply
      localStorage.setItem('ruhi_chat_memory', JSON.stringify(finalMessages));
    } catch (err) {
      setError(err.message);
    } finally {
      setIsTyping(false);
    }
  };

  const handleClearMemory = () => {
    if (window.confirm("Tum Ruhi ki saari memory delete karna chahte ho? Wo sab bhool jayegi.")) {
      localStorage.removeItem('ruhi_chat_memory');
      const initialMessage = {
        role: 'model',
        text: "Hii! 👋 Main Ruhi. Aap kaun ho?",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages([initialMessage]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans sm:bg-slate-200 justify-center items-center">
      <div className="w-full h-full sm:h-[90vh] sm:max-w-md sm:rounded-3xl sm:border-[8px] border-slate-800 bg-white overflow-hidden flex flex-col shadow-2xl relative">
        
        {/* Header */}
        <div className="bg-pink-500 text-white p-4 flex items-center justify-between z-10 shadow-md">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-pink-200 flex items-center justify-center border-2 border-white shadow-sm overflow-hidden">
               <img src="https://api.dicebear.com/7.x/adventurer-neutral/svg?seed=Ruhi&backgroundColor=fbcfe8" alt="Ruhi Avatar" className="w-full h-full object-cover" />
            </div>
            <div>
              <h1 className="font-bold text-lg leading-tight">Ruhi ✨</h1>
              <p className="text-xs text-pink-100">{isTyping ? 'typing...' : 'Online'}</p>
            </div>
          </div>
          <button 
            onClick={handleClearMemory}
            className="text-xs bg-pink-600 hover:bg-pink-700 px-2 py-1 rounded-md transition"
            title="Clear Chat & Memory"
          >
            Reset Memory
          </button>
        </div>

        {/* API Key Warning (if empty) */}
        {!API_KEY && (
          <div className="bg-red-100 text-red-700 text-xs p-2 text-center font-semibold">
            ⚠️ Code me API_KEY missing hai! Upar code edit karke key daalo.
          </div>
        )}
        
        {/* Error Message */}
        {error && (
          <div className="bg-orange-100 text-orange-700 text-xs p-2 text-center">
            {error}
          </div>
        )}

        {/* Chat Area */}
        <div className="flex-1 p-4 overflow-y-auto bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-slate-50 flex flex-col space-y-4">
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'self-end items-end' : 'self-start items-start'}`}
            >
              <div 
                className={`px-4 py-2 rounded-2xl shadow-sm text-sm ${
                  msg.role === 'user' 
                    ? 'bg-pink-500 text-white rounded-br-sm' 
                    : 'bg-white border border-slate-100 text-slate-800 rounded-bl-sm'
                }`}
              >
                {msg.text}
              </div>
              <span className="text-[10px] text-slate-400 mt-1 px-1">
                {msg.timestamp}
              </span>
            </div>
          ))}
          
          {/* Typing Indicator */}
          {isTyping && (
             <div className="self-start max-w-[80%] flex flex-col items-start">
               <div className="bg-white border border-slate-100 px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm flex space-x-1">
                  <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce"></div>
                  <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
               </div>
             </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-3 bg-white border-t border-slate-100 z-10">
          <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Message Ruhi..."
              disabled={isTyping || !API_KEY}
              className="flex-1 bg-slate-100 text-slate-800 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-300 transition"
            />
            <button 
              type="submit" 
              disabled={!inputText.trim() || isTyping || !API_KEY}
              className="bg-pink-500 hover:bg-pink-600 disabled:bg-pink-300 disabled:cursor-not-allowed text-white p-2.5 rounded-full transition shadow-md flex items-center justify-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 ml-0.5">
                <path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" />
              </svg>
            </button>
          </form>
        </div>
        
      </div>
    </div>
  );
}

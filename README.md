# calling-agent
This project is a Jarvis-like AI Phone Assistant built with Flask, Twilio, CrewAI, and LangChain. Incoming calls are routed via ngrok, transcribed with Twilio STT, and answered by an AI agent. Replies are spoken back using Twilio TTS. It also supports outbound calls programmatically

# 📞 Jarvis AI Phone Assistant (Flask + Twilio + CrewAI)

A real-time **AI-powered phone assistant** that answers and makes phone calls using  
**Twilio Voice API, Flask, CrewAI, and LangChain OpenAI**.  

---

## ✨ Features
- 📞 Answer incoming phone calls with AI
- 🎙️ Convert caller speech to text (Twilio STT)
- 🧠 Generate intelligent responses via **CrewAI Agent (LLM)**
- 🔊 Speak responses back with Twilio TTS
- 📡 Supports **inbound** and **outbound** calls
- 🤖 Predefined personality ("Jarvis") that talks politely and clearly

---

## 🛠️ Tech Stack
- **Python (Flask)** → Webhook server
- **Twilio Voice API** → Phone call handling
- **ngrok** → Public HTTPS tunnel to local server
- **CrewAI** → AI agent framework
- **LangChain + OpenAI/Gemini LLMs** → Language model for responses

---

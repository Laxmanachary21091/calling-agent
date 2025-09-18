from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Flask app setup
app = Flask(__name__)

# 🔑 API Keys (hidden for security)
# you can hide in .env fileS
OPENAI_API_KEY = "your_openai_api_key_here"
TWILIO_SID = "your_twilio_sid_here"
TWILIO_AUTH = "your_twilio_auth_token_here"
TWILIO_NUMBER = "twilio nuber"   # Replace with your Twilio phone number
NGROK_URL = "https://your-ngrok-url.ngrok-free.app"   # Replace with your ngrok tunnel URL

#  LangChain-compatible LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)

#  CrewAI Agent
calling_agent = Agent(
    role="Calling Assistant",
    goal="Answer phone calls politely and clearly.",
    backstory="You are Jarvis, an AI phone assistant. You listen to callers and respond helpfully.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

#  Twilio Client
client_twilio = Client(TWILIO_SID, TWILIO_AUTH)

# Webhook for handling calls

@app.route("/voice", methods=['POST'])
def voice():
    caller_text = request.form.get("SpeechResult", "")
    print(f"👤 Caller: {caller_text}")

    # Default greeting
    if not caller_text:
        response_text = "Hello, I am Jarvis, your AI assistant. How can I help you today?"
    elif "bye" in caller_text.lower():
        response_text = "Goodbye! Have a great day."
        vr = VoiceResponse()
        vr.say(response_text, voice="alice", language="en-US")
        return Response(str(vr), mimetype="application/xml")
    else:
        # Run CrewAI task
        task = Task(
            description=f"The caller said: '{caller_text}'. Respond politely and clearly.",
            agent=calling_agent,
            expected_output="A natural spoken reply."
        )
        crew = Crew(agents=[calling_agent], tasks=[task], verbose=True)
        result = crew.kickoff()

        # Extract response text
        if hasattr(result, "final_output"):
            response_text = result.final_output
        elif hasattr(result, "output"):
            response_text = str(result.output)
        else:
            response_text = str(result)

    print(f"🤖 Jarvis: {response_text}")

    # Build TwiML
    vr = VoiceResponse()
    gather = vr.gather(
        input="speech",
        action="/voice",
        method="POST",
        timeout=5
    )
    gather.say(response_text, voice="alice", language="en-US")

    return Response(str(vr), mimetype="application/xml")


# Trigger outbound call

def make_outbound_call(to_number):
    call = client_twilio.calls.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        url=f"{NGROK_URL}/voice"  # must end with /voice
    )
    print(f"📞 Call initiated. SID: {call.sid}")
    return call.sid

if __name__ == "__main__":
    print("🚀 Flask server running on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)  # dvno auto-reloader

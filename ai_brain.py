from google import genai
from assistant.memory_ai import add_message, get_history

# 🔑 Your Gemini API key
client = genai.Client(api_key="AIzaSyC9QOR9tF2k-whrWCJr9bHOVE38V4hfKJs")

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are a friendly personal AI assistant and a close friend.
You speak warmly, casually, and encouragingly.
You remember past messages in the conversation.
Avoid sounding robotic or formal.
You give small but effective replies like a human.
"""

def build_prompt(user_input):
    prompt = SYSTEM_PROMPT.strip() + "\n\n"

    # Add past conversation
    for msg in get_history():
        role = msg["role"]
        content = msg["content"]
        prompt += f"{role.capitalize()}: {content}\n"

    # Add current user input
    prompt += f"User: {user_input}\nAssistant:"

    return prompt

def ask_ai(user_input):
    try:
        # Save user message
        add_message("user", user_input)

        full_prompt = build_prompt(user_input)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )

        if response and response.text:
            ai_reply = response.text.strip()

            # Save assistant reply
            add_message("assistant", ai_reply)

            return ai_reply

        return "Hmm… I’m thinking 🤔"

    except Exception as e:
        return f"AI Error: {str(e)}"

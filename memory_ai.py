# Stores recent conversation (short-term memory)

conversation_history = []

MAX_HISTORY = 6  # last 6 messages only

def add_message(role, content):
    conversation_history.append({
        "role": role,
        "content": content
    })

    # Keep memory small
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

def get_history():
    return conversation_history


import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key is not configured!")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Store conversation history
conversation_history = []


MAX_HISTORY_TURNS = 5

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Chat ended. Goodbye!")
        break

    if question.lower() == "clear":
        conversation_history.clear()
        print("Conversation history cleared.\n")
        continue

    if not question:
        print("Please enter a valid question.\n")
        continue

    # Create the user's message
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=question)]
    )

    
# Keep the last 5 completed conversation turns
recent_history = conversation_history[-(MAX_HISTORY_TURNS * 2):]

# Add the current user message temporarily
pending_history = recent_history + [user_message]

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=pending_history
    )

    if response.text:
        print("\nGemini:", response.text, "\n")

        # Save the successful conversation turn
        conversation_history.append(user_message)

        conversation_history.append(
            types.Content(
                role="model",
                parts=[types.Part(text=response.text)]
            )
        )

        # Remove older complete conversation turns
        if len(conversation_history) > MAX_HISTORY_TURNS * 2:
            del conversation_history[:2]

    else:
        print("Gemini returned an empty response.\n")

except Exception as e:
    print(f"Something went wrong: {e}")
    print("Please try again.\n")

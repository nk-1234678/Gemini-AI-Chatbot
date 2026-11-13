
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

# Model configuration
MODEL_NAME = "gemini-3.5-flash"
MAX_INPUT_TOKENS = 1000

# Store complete conversation history
conversation_history = []


def build_context_within_budget(history, new_user_message):
    """
    Build a temporary context that fits within
    the maximum input token budget.
    """

    # Create a separate context.
    # Original conversation_history remains unchanged.
    context = history.copy() + [new_user_message]

    while True:

        # Count tokens in the current context
        token_info = client.models.count_tokens(
            model=MODEL_NAME,
            contents=context
        )

        total_tokens = token_info.total_tokens

        print(f"Input tokens: {total_tokens}")

        # Check whether context fits within token budget
        if total_tokens <= MAX_INPUT_TOKENS:
            return context

        # If only the current question remains
        if len(context) <= 1:
            raise ValueError(
                "Your question exceeds the token budget!"
            )

        # Remove the oldest user-model message pair
        del context[:2]


print("Gemini Chatbot V6 started!")
print("Type 'exit' to end the chat.")
print("Type 'clear' to clear conversation history.\n")


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

    try:

        # Build context according to token budget
        pending_history = build_context_within_budget(
            conversation_history,
            user_message
        )

        # Send context to Gemini
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=pending_history
        )

        if response.text:

            print("\nGemini:", response.text, "\n")

            # Save successful conversation to full history
            conversation_history.append(user_message)

            conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=response.text)]
                )
            )

        else:
            print("Gemini returned an empty response.\n")

    except Exception as e:

        print(f"Something went wrong: {e}")
        print("Please try again.\n")

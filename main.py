import json
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
SUMMARY_THRESHOLD = 6
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "conversation_memory.json")
conversation_summary = ""

# Store complete conversation history
conversation_history = []







def load_conversation_memory():
    global conversation_history, conversation_summary

    if not os.path.exists(MEMORY_FILE):
        print("No previous memory found. Starting a new conversation.\n")
        return

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        conversation_summary = saved_data.get("conversation_summary", "")

        conversation_history = []

        for message in saved_data.get("conversation_history", []):
            restored_message = types.Content(
                role=message["role"],
                parts=[
                    types.Part(text=part["text"])
                    for part in message["parts"]
                ]
            )

            conversation_history.append(restored_message)

        print("Previous conversation memory loaded successfully!\n")

    except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
        print(f"Could not load previous memory: {e}")
        print("Starting with empty memory. Existing file has not been deleted.\n")
        conversation_history = []
        conversation_summary = ""
        
        

def save_conversation_memory():
    saved_data = {
        "conversation_summary": conversation_summary,
        "conversation_history": []
    }

    for message in conversation_history:
        message_data = {
            "role": message.role,
            "parts": []
        }

        for part in message.parts:
            if part.text:
                message_data["parts"].append({
                    "text": part.text
                })

        saved_data["conversation_history"].append(message_data)

    temp_file = MEMORY_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(saved_data, file, indent=4, ensure_ascii=False)

        os.replace(temp_file, MEMORY_FILE)
        print("[Memory saved successfully]")

    except (OSError, TypeError, ValueError) as e:
        print(f"Could not save conversation memory: {e}")
        
        
        

def summarize_conversation(history, existing_summary):
    """
    Summarize older conversation messages
    while preserving important information.
    """

    # Convert conversation messages into readable text
    conversation_text = ""

    for message in history:
        role = message.role

        for part in message.parts:
            if part.text:
                conversation_text += f"{role}: {part.text}\n"

    # Include previous summary so important information
    # is not lost during summary updates
    prompt = f"""
You are a conversation summarization assistant.

Your task is to create an updated summary of the
conversation.

Previous summary:
{existing_summary if existing_summary else "No previous summary."}

New older conversation messages:
{conversation_text}

Instructions:
1. Preserve important facts about the user.
2. Preserve preferences, goals and ongoing tasks.
3. Remove unnecessary greetings and repeated information.
4. Do not invent or assume information.
5. Keep the summary concise and useful for future replies.
6. Return only the updated summary.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty summary.")

    return response.text.strip()



def update_conversation_memory():

    global conversation_summary

    # Check whether summarization is needed
    if len(conversation_history) < SUMMARY_THRESHOLD:
        return

    # Keep the latest 4 messages as recent history
    messages_to_summarize = conversation_history[:-4]

    try:
        # Generate updated summary
        updated_summary = summarize_conversation(
            messages_to_summarize,
            conversation_summary
        )

        # Update summary only after successful generation
        conversation_summary = updated_summary

        # Remove summarized messages from original history
        del conversation_history[:-4]

        print("\n[Older conversation summarized]\n")

    except Exception as e:
        print(f"Summarization failed: {e}")
        print("Keeping the existing conversation history.\n")




def build_context_within_budget(history, new_user_message):

    context = []

    # Add conversation summary as background context
    if conversation_summary:
        summary_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=(
                        "Use the following conversation summary "
                        "as background information:\n"
                        + conversation_summary
                    )
                )
            ]
        )

        context.append(summary_message)

    # Add recent conversation and current question
    context.extend(history)
    context.append(new_user_message)

    summary_count = 1 if conversation_summary else 0

    while True:

        token_info = client.models.count_tokens(
            model=MODEL_NAME,
            contents=context
        )

        total_tokens = token_info.total_tokens

        print(f"Input tokens: {total_tokens}")

        if total_tokens <= MAX_INPUT_TOKENS:
            return context

        # Do not remove the summary or current question
        if len(context) <= summary_count + 1:
            raise ValueError(
                "Summary and current question exceed token budget!"
            )

        # Remove the oldest recent conversation pair
        del context[summary_count:summary_count + 2]




load_conversation_memory()

print("Gemini Chatbot V8 started!")
print("Type 'exit' to end the chat.")
print("Type 'clear' to clear conversation history.\n")

while True:

    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Chat ended. Goodbye!")
        break

    if question.lower() == "clear":
        conversation_history.clear()
        conversation_summary = ""

        save_conversation_memory()

        print("Conversation history and summary cleared.\n")
        continue

    if not question:
        print("Please enter a valid question.\n")
        continue

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=question)]
    )

    try:

        # Step 1: Summarize older messages if threshold is reached
        update_conversation_memory()
        save_conversation_memory()

        # Step 2: Build context within token budget
        pending_history = build_context_within_budget(
            conversation_history,
            user_message
        )

        # Step 3: Send context to Gemini
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=pending_history
        )

        if response.text:
            print("\nGemini:", response.text, "\n")

            conversation_history.append(user_message)

            conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=response.text)]
                )
            )
            save_conversation_memory()

        else:
            print("Gemini returned an empty response.\n")

    except Exception as e:

        print(f"Something went wrong: {e}")
        print("Please try again.\n")

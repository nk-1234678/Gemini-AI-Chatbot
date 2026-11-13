# Gemini AI Chatbot

A conversational AI chatbot built using Python and Google's Gemini API. This project is part of my hands-on Generative AI learning journey, where I learn LLM concepts by implementing them step by step.

Rather than just building a chatbot, the goal is to understand how LLM-powered applications work internally, including API integration, conversation memory, tokenization, context management, and prompt engineering.

## Tech Stack

- **Language:** Python
- **LLM:** Google Gemini
- **SDK:** Google GenAI SDK
- **Environment Management:** python-dotenv
- **Version Control:** Git & GitHub

## Project Structure

```text
gemini-ai-chatbot/
│
├── main.py
│   
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Development Roadmap

### V1 – Basic Gemini Chatbot
**Implemented**

**What we built:**
- Integrated the Gemini API with Python.
- Loaded the API key securely using environment variables.
- Initialized the Gemini client.
- Accepted a user question and generated an AI response.

**Concepts learned:**
- API integration
- Environment variables
- API keys
- LLM inference
- Request and response cycle

**Gap identified:** The chatbot could answer only one question at a time. It did not maintain an interactive conversation.

### V2 – Continuous Conversation
**Implemented**

**What we added:**
- Introduced a `while` loop.
- Enabled continuous user interaction.
- Added an `exit` command to end the conversation.

**Concepts learned:**
- Python loops
- Continuous execution
- User input handling

**Gap identified:** The chatbot could accept multiple questions, but each request was independent. It did not remember previous messages.

### V3 – Input Validation and Error Handling
**Implemented**

**What we added:**
- Used `.strip()` to remove unnecessary whitespace.
- Prevented empty user inputs.
- Added `try-except` error handling.
- Handled API and runtime errors without immediately terminating the chatbot.

**Concepts learned:**
- Input validation
- Exception handling
- Runtime errors
- Basic application reliability

**Gap identified:** The chatbot was more reliable, but still had no conversation memory.

### V4 – Conversation Memory
**Implemented**

**What we added:**
- Created a `conversation_history` list.
- Stored user messages and Gemini responses.
- Sent previous conversation messages with new requests.
- Added a `clear` command to reset conversation history.

**Concepts learned:**
- Lists and data structures
- Conversation history
- Context passing
- User and model message roles
- Stateful vs. stateless interactions

**Gap identified:** Conversation history kept growing indefinitely, increasing token usage and potentially exceeding the model's context window.

### V5 – Sliding Window Memory
**Implemented**

**What we added:**
- Introduced `MAX_HISTORY_TURNS`.
- Limited the chatbot to the latest five completed conversation turns.
- Removed older user-model message pairs.
- Preserved recent conversational context.

**Concepts learned:**
- Sliding window technique
- List slicing
- List deletion
- Memory management
- Context limitation

**Gap identified:** The chatbot limited memory by the number of messages, not their actual token count. A single long message could consume many more tokens than a short message.

### V6 – Token-Based Conversation Trimming
**Implemented**

**What we added:**
- Introduced a maximum input token budget.
- Used Gemini's `count_tokens()` method.
- Created a separate temporary context using `history.copy()`.
- Removed the oldest conversation pairs until the context fitted within the token budget.
- Preserved the original conversation history while preparing API requests.

**Concepts learned:**
- Tokenization
- Tokens vs. words
- Context window
- Token budget
- Token counting
- Temporary context management
- Reusable Python functions (`def`)
- Function parameters and return values

**Gap identified:** Old messages are removed when the token budget is exceeded. Important information from those messages can therefore be lost.


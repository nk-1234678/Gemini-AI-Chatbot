import os
from dotenv import load_dotenv 
from google import genai
from google.genai import types

# load env variables
load_dotenv()        


#read api key
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")    

if not api_key:
    raise ValueError("gemini api key is not being configured")



# Initialising Gemini Client
client = genai.Client(api_key=api_key)    


conversation_history = []
# question = input("You:")

# # Generate AI Response
# response = client.models.generate_content(      
#     model = "gemini-3.5-flash",
#     contents=question
# )



while True:
    question = input("You: ")
    
    if question.lower() == "exit":
        print("Chat Ended.Feel free to reach out if you need anything else. Have a great day! ")
        break
    
    if question.lower() == "clear":
        conversation_history.clear()
        print("conversation is cleared")
        continue
    
    if not question:
        print("Please ask a question.")
        continue
    
    conversation_history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=question)]
        )
    )
    
    try:
        response = client.models.generate_content(
                model = "gemini-3.5-flash",
                contents=conversation_history
            )
        
        if response.text:
            print("\nGemini:", response.text,"\n")
            
            conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=response.text)]
                )
            )
    
    except Exception as e:
        print(f"Something went wrong: {e}")
        print("Please try again")
    

    
    





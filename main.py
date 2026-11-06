import os
from dotenv import load_dotenv 
from google import genai


# load env variables
load_dotenv()        


#read api key
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")    

if not api_key:
    raise ValueError("gemini api key is not being configured")



# Initialising Gemini Client
client = genai.Client(api_key=api_key)    

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
    
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents=question
    )
    
    print("\nGemini:", response.text,"\n")





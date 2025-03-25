import google.generativeai as genai
import pydotenv as dotenv
import os

# Set up Gemini API key
dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate AI response
def generate_response(prompt):
    model = genai.GenerativeModel(  
        model_name="gemini-2.0-flash",  
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 200,
        },
    )

    try:
        response = model.generate_content(prompt).text  
    except Exception as e:
        print(f"Error in response generation: {e}")

    # Remove code block formatting
    response = response.replace("```json", "")  
    response = response.replace("```", "")  

    return response 


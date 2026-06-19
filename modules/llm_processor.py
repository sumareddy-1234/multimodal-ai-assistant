import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMProcessor:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            print("Warning: GROQ_API_KEY is missing or not set in .env")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
                self.client = None

        self.model_name = model_name

    def generate_response(self, prompt: str) -> str:
        if not self.client:
            return "Error: GROQ_API_KEY is missing. Please set it in the .env file."

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful multimodal AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"
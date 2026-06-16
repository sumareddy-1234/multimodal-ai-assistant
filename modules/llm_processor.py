import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMProcessor:
    def __init__(self, model_name="gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("Warning: OPENAI_API_KEY is missing or not set in .env")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        
        self.model_name = model_name

    def generate_response(self, prompt: str) -> str:
        """
        Sends the fused prompt to the OpenAI LLM and returns the response.
        """
        if not self.client:
            return "Error: OpenAI API key is missing. Please set OPENAI_API_KEY in the .env file."

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful, multimodal AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error communicating with LLM API: {str(e)}"

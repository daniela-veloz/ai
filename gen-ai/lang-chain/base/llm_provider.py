from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
import os

class LLMProvider:
    def __init__(self, model_name: str):
        load_dotenv()

        OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
        DEEP_SEEK_API_KEY = os.getenv("DEEP_SEEK_API_KEY")

        if model_name == 'gpt-4':
            self.chat_open_ai = ChatOpenAI(api_key=OPEN_API_KEY, model_name="gpt-4")
        if model_name == 'deepseek-reasoner':
            self.chat_open_ai = ChatOpenAI(
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com",
            model=model_name)

    def get_chat_open_ai(self):
        return self.chat_open_ai
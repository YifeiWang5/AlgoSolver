# # OpenAI
# import os
# import keyring
# from langchain_openai import ChatOpenAI
# os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Ollama
from langchain_ollama import ChatOllama
llm = ChatOllama(model="gemma3:27b", temperature=1.0, top_k = 64, top_p = 0.95 , validate_model_on_init=True) 
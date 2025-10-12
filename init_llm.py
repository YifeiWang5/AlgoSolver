# # OpenAI
# import os
# import keyring
# from langchain_openai import ChatOpenAI
# os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Ollama
from langchain_ollama import ChatOllama
llm = ChatOllama(model="gemma3:4b", temperature=1.0, top_k = 64, top_p = 0.95 , validate_model_on_init=True) 
# llm = ChatOllama(model="gpt-oss:20b", validate_model_on_init=True) 
parse_llm = llm
# parse_llm = ChatOllama(model="gemma3:27b", temperature=1.0, top_k = 64, top_p = 0.95 , validate_model_on_init=True) 
# llm = ChatOllama(model="deepseek-r1:8b", validate_model_on_init=True) "deepseek-r1:14b"
# llm = ChatOllama(model="gemma3:4b", temperature=1.0, top_k = 64, top_p = 0.95 , validate_model_on_init=True) 
# parse_llm = llm

# ====== Tool Enabled LLMs ======
tool_calling_llm = ChatOllama(model="gpt-oss:20b", validate_model_on_init=True)
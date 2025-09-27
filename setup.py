import os
import keyring

os.environ["TAVILY_API_KEY"] = keyring.get_password('tavily', 'api_key')
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')

# LangSmith Set-Up
SERVICE = "langsmith"
USERNAME = "api_key"
os.environ["LANGSMITH_API_KEY"] = keyring.get_password(SERVICE, USERNAME)
os.environ["LANGSMITH_PROJECT"] = "algo_solver"
os.environ["LANGSMITH_TRACING"] = "true"
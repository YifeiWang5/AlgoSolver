import os
import keyring
# SERVICE = "tavily"
# USERNAME = "api_key"
os.environ["TAVILY_API_KEY"] = keyring.get_password('tavily', 'api_key')
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
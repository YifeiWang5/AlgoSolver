#Receives the user problem and optional constraints (language, allowed techniques, resource limits). Normalizes formatting and metadata.

#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def user_interface_agent(state):

    return state
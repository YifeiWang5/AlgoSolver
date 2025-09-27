#Receives the user problem and optional constraints (language, allowed techniques, resource limits). Normalizes formatting and metadata.

#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def user_interface_agent(state):
    prompt_for_user = """
I am an expert algorithm solver!\n
In the solution I will provide peusdocode, proof of correctness, and time complexity.\n\n
Please input the algorithm problem below:\n
"""
    user_input = input(prompt_for_user)
    # state["messages"] = [
    #     AIMessage(content=prompt_for_user),
    #     HumanMessage(content=user_input)
    # ]
    state["messages"] = [
        {"role":"assistant", "content": prompt_for_user},
        {"role":"user", "content": user_input}
    ]
    if state["context"] is None:
        state["context"] = user_input
    else:
        state["context"] = state["context"] + f'\nUser: {user_input}\n'
    return state

#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def prover_agent(state):

    system_prompt = f"""
# Role
You are an expert at proving that a Pseudocode Solution is correct for an Algorithm Problem. 

# Task
Given an Algorithm Problem and Pseudocode Solution, provide a formal proof of correctness. **If** you cannot create a valid proof, reply with "Proof not available."

# Algorithm Problem: {state["problem_spec"]}

# Pseudocode Solution: {state['pseudocode']}


# Output: **ONLY** the formal proof of correctness. **If** you cannot create a valid proof, reply with "Proof not available."

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"prover", "content": f'Proof of Correctness: {response.content}'})
    state["proof"] = response.content
    return state
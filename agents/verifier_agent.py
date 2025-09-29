
#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from pydantic import BaseModel
# from typing import Any
class AnswerSchema(BaseModel):
    verified: bool
    
structered_llm = llm.with_structured_output(AnswerSchema)

def verifier_agent(state):
    if state["previous_agent"] == "coder":
        system_prompt = f"""
# Role
You are an independent verification expert. 

# Task
Review the provided pseudocode and determine if it successfully solves the algorithm problem.

# Algorithm Problem: {state['problem_spec']}

# Pseudocode: {state['pseudocode']}

# Output: **ONLY** True (if the pseudocode correctly solves the problem) or False (if the pseudocode does not solve the problem correctly)

"""
    elif state["previous_agent"] == "prover": 
        system_prompt = f"""
# Role
You are an independent verification expert. 

# Task
Review the provided formal proof of correctness and determine if it is a valid proof. You are provided the Algorithm Problem, Pseudocode Solution, and Proof of Correctness.

# Algorithm Problem: {state['problem_spec']}

# Pseudocode Solution: {state['pseudocode']}

# Proof of Correctness: {state['proof']}

# Output: **ONLY** True (if the proof is a valid proof of correctness for the provided problem and solution) or False (if the proof is not valid)
"""
    else:
        system_prompt = f"""
"""
    response = structered_llm.invoke(system_prompt)
    state["messages"].append({"role":"verifier", "content": f'Verification of proof: {response.verified}'})
    state["verified"] = response.verified
    return state
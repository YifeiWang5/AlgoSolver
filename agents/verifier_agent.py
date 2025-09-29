from init_llm import llm

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
    elif state["previous_agent"] == "complexity": 
        system_prompt =  f"""
# Role
You are an independent verification expert. 

# Task
Review the Big-O Notation for the provided Pseudocode Solution to an Algorithm Problem, and determine if the Big-O Notation is accurate.

# Algorithm Problem: {state['problem_spec']}

# Pseudocode Solution: {state['pseudocode']}

# Big-O Notation: {state['complexity']}

# Output: **ONLY** True (if the Big-O Notation is accurate for the provided problem and solution) or False (if the Big-O Notation is not accurate)
"""
    else:
        system_prompt = f"""
"""
    response = structered_llm.invoke(system_prompt)
    state["messages"].append({"role":"verifier", "content": f'Verification of proof: {response.verified}'})
    state["verified"] = response.verified
    return state
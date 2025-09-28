
#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from pydantic import BaseModel
# from typing import Any
class AnswerSchema(BaseModel):
    selected_algo: str
    pseudocode: str
    
structered_llm = llm.with_structured_output(AnswerSchema)

def coder_agent(state):

    system_prompt = f"""
# Role
You are an expert at creating pseudocode to solve algorithms.

# Task
Given a list of possible algorithm techniques, choose the best option for solving the algorithm problem. Create a pseudocode algorithm that solves the problem. 

# Algorithm Techniques: {state["algorithm_techs"]}

# Algorithm Problem: {state["problem_spec"]}


# Output: **ONLY** the selected algorithm technique save to 'selected_algo', and the pseudocode solution saved to 'pseudocode'

"""
    response = structered_llm.invoke(system_prompt)
    state["messages"].append({"role":"coder", "content": f'Selected Algorithm: {response.selected_algo}\n Pseudocode Solution: {response.pseudocode}'})
    state["selected_algo"] = response.selected_algo
    state["pseudocode"] = response.pseudocode
    return state
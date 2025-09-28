#Extracts inputs, outputs, constraints, assumptions, edge-cases, and required proof style (informal/rigorous/induction). Outputs a structured ProblemSpec.

#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from pydantic import BaseModel
class AnswerSchema(BaseModel):
    inputs: str
    outputs: str
    constraints: str
    assumptions: str
    edge_cases: str
    
structered_llm = llm.with_structured_output(AnswerSchema)

def problem_parser_agent(state):
    system_prompt = f"""
# Role
You are an expert at extracting INPUTS, OUTPUTS, CONSTRAINTS, ASSUMPTIONS, and EDGE_CASES from an algorithm problem written in natural language.

# Task
Extract INPUTS, OUTPUTS, CONSTRAINTS, ASSUMPTIONS, and EDGE_CASES from the provided algorthim problem and output it as a JSON. The JSON should have the keys 'inputs', 'outputs', 'constraints', 'assumptions', and 'edge_cases'.

# Input (algorithm problem): {state["context"]}


# Output: **ONLY** the JSON object

"""
    response = structered_llm.invoke(system_prompt)
    state["messages"].append({"role":"parser", "content": response.dict()})
    state["problem_spec"] = response.dict()
    return state
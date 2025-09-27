#Extracts inputs, outputs, constraints, assumptions, edge-cases, and required proof style (informal/rigorous/induction). Outputs a structured ProblemSpec.

#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def problem_parser_agent(state):
    system_prompt = f"""
You are an expert at extracting INPUTS, OUTPUTS, CONSTRAINTS, ASSUMPTIONS, and EDGE_CASES from an algorithm problem written in natural language.

# Input (algorithm problem): {state["context"]}


# Output:
A python dict containing key/value pairs for INPUTS, OUTPUTS, CONSTRAINTS, ASSUMPTIONS, and EDGE_CASES

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"assistant", "content": response.content})
    return state
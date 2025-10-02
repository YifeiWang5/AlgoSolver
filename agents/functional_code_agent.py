from init_llm import llm



def real_coder_agent(state):

    system_prompt = f"""
# Role
You are an expert python programmer. 

# Task
Given an Algorithm Problem, Pseudocode Solution, and Code Structure: provide a functional python code for the Pseudocode Solution that solves the Algorithm Problem in the format provided with Code Structure.

# Algorithm Problem: {state["problem_spec"]}

# Pseudocode Solution: {state['pseudocode']}

# Code Structure: {state['real_code_struct']}


# Output: **ONLY** python code solution in Code Structure 

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"real_coder", "content": f'Functional Python Code: {response.content}'})
    state["real_code"] = response.content
    return state
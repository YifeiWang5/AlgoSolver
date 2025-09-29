from init_llm import llm



def real_coder_agent(state):

    system_prompt = f"""
# Role
You are an expert python programmer. 

# Task
Given an Algorithm Problem and Pseudocode Solution, provide a functional python code for the Pseudocode Solution that solves the Algorithm Problem.

# Algorithm Problem: {state["problem_spec"]}

# Pseudocode Solution: {state['pseudocode']}


# Output: **ONLY** python code solution 

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"real_coder", "content": f'Functional Python Code: {response.content}'})
    state["real_code"] = response.content
    return state
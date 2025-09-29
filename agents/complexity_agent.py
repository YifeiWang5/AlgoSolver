from init_llm import llm

import json


def complexity_agent(state):
    # Load Utility Data
    with open('utilities/big_o.json', "r", encoding="utf-8") as f:
        big_o = json.load(f)

    system_prompt = f"""
# Role
You are an expert at estimating the Big-O time complexity for a Pseudocode Solution to an Algorithm Problem. 

# Task
Given an Algorithm Problem and Pseudocode Solution, provide the Big-O time complexity notation.

# Algorithm Problem: {state["problem_spec"]}

# Pseudocode Solution: {state['pseudocode']}

# Big-O Notation Keys: {big_o}


# Output: **ONLY** the big-o notation. 

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"complexity", "content": f'Time Complexity: {response.content}'})
    state["complexity"] = response.content
    return state
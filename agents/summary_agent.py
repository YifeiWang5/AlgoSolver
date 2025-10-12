from init_llm import llm

def summarizer_agent(state):

    system_prompt = f"""
# Role 
You are an expert text summarizer.

# Task
Given an Algorithm Problem and Research Findings, write a concise summary of how the Algorithm Problem can be solved using the Research Findings.

# Algorithm Problem: {state["problem_spec"]}

# Research Findings: {state["research_findings"]}

# Output: **ONLY** the text summary

"""
    response = llm.invoke(system_prompt)
    state["messages"].append({"role":"summarizer", "content": f'Research Summary: {response.content}'})
    state["research_summary"] = response.content
    return state
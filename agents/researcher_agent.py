from init_llm import llm
from agents.tools.vs_search import vs_search
from langchain.tools import StructuredTool

tools = [
        StructuredTool.from_function(
            func=vs_search,
            name="vs_search",
            description="Search the FAISS vector store and return results as text."
        )]
llm_w_tools = llm.bind_tools(tools)

def researcher_agent(state):

    system_prompt = f"""
# Role
You are an expert researcher. 

# Task
Given an Algorithm Problem, formulate a query for the tools provided to you to research and provide suggestions for how to solve the Algorithm Problem.

# Algorithm Problem: {state["problem_spec"]}

# Tools: vs_search(query: str, search_num: int): Similarity search against a FAISS vector store. Returns results as a string.

# Output: **ONLY** research results 

"""
    response = llm_w_tools.invoke(system_prompt)
    state["messages"].append({"role":"researcher", "content": f'Research: {response.content}'})
    state["tool_call"] = response
    # state["messages"].append(response)
    # state["research_findings"] = response.content
    return state
from init_llm import tool_calling_llm as llm
from agents.tools.vs_search import vs_search
from langchain.tools import StructuredTool
from langchain_core.messages import AIMessage

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
**FIRST** Check if the Previous Research helps solve the Algorithm Problem. If yes, reply only with 'Research Complete'. Else continue to second step.
**SECOND** If Previous Research does not help, then formulate a couple queries to gain knowledge about the Algorithm Problem.
**THIRD** Consider each query generated in the second step, and choose the best one. Reply with a tool call using the best query from the second step. 

# Algorithm Problem: {state["problem_spec"]}

# Previous Research: {state['research_summary']}

# Tools (optional): vs_search(query: str, search_num: int): Similarity search against a FAISS vector store. Returns results as a string.
### Previous Queries: {state['research_queries']}

# Output: **IF** the Previous Research is sufficient, reply only with 'Research Complete' **ELSE** research query tool call.

"""
    response = llm_w_tools.invoke(system_prompt)
    state["messages"].append({"role":"researcher", "content": f'Research: {response.model_dump()}'})
    if not isinstance(response, AIMessage) or not getattr(response, "tool_calls", None):
        pass
    else:
        state["research_queries"].append(str(response.tool_calls[0].get("args").get("query")))
    state["tool_call"] = response
    return state
from init_llm import parse_llm as llm
import json
# # ------ Load Tools ------
# from langchain.tools import StructuredTool
# from .tools.vs_search import vs_search
# tools = [
#     StructuredTool.from_function(
#         func=vs_search,
#         name="vs_search",
#         description="Search the FAISS vector store and return results as text."
#     )]
# llm_w_tools = llm.bind_tools(tools)

from pydantic import BaseModel
# from typing import Any
class AnswerSchema(BaseModel):
    algorithm_techs: list[str]
    
structered_llm = llm.with_structured_output(AnswerSchema)


def strategy_agent(state):
    # Load Utility Data
    with open('utilities/algo_tech2.json', "r", encoding="utf-8") as f:
        algo_tech = json.load(f)

    system_prompt = f"""
# Role
You are an expert at determining the best algorithm technique given a algorithm problem. 

# Task
Given an algorithm problem as a JSON object (problem_spec), determine which algorithm technique is best from the available options.

# Algorithm Techniques: {algo_tech}

# Input (problem_spec): {state["problem_spec"]}

# Research Results: {state["research_summary"]}


# Output: **ONLY** a list of algo_tech keys.

"""
    response = structered_llm.invoke(system_prompt)
    state["messages"].append({"role":"strategist", "content": response.algorithm_techs})
    state["algorithm_techs"] = response.algorithm_techs
    state["routing"] = "strategy"
    return state
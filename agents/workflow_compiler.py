from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

from .user_interface_agent import user_interface_agent
from .problem_parser_agent import problem_parser_agent
from .strategy_agent import strategy_agent #, tools as planner_agent_tools

# # ------ Load Utility Data ------
# with open('utilities/algo_tech.json', "r", encoding="utf-8") as f:
#     algo_tech = json.load(f)

# ------ Load Tools ------
# Concat all tool lists
# tools = planner_agent_tools

# ------ Define State ------
class AgentState(TypedDict):
    context: str | None
    messages: list[dict[str, Any]]
    problem_spec: dict | None
    algorithm_techs: list[str]
    vector_search_results: list[dict[str, Any]]

def create_agent_state(
        context=None,
        messages=[],
        problem_spec=None,
        algorithm_techs=[],
        vector_search_results=None,
) -> AgentState:
    return AgentState(
        context=context,
        messages=messages,
        problem_spec=problem_spec,
        algorithm_techs=algorithm_techs,
        vector_search_results=vector_search_results,
    )

# ------ Define Workflow ------
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

## ----- Nodes -----
def run_tools(state: AgentState):
    """
    Custom replacement for ToolNode:
    - Look for tool calls in the last AIMessage
    - Execute them and append ToolMessage outputs
    """
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not getattr(last_message, "tool_calls", None):
        # No tool calls, nothing to do
        return state  

    for call in last_message.tool_calls:
        name = call["name"]
        args = call.get("args", {})
        for tool in tools:
            if name in tool.name:
                result = tool.invoke(args)

                # Append a ToolMessage with the result
                state["messages"].append(
                    ToolMessage(name=name, content=result, tool_call_id=call["id"])
                )
                state["research_results"].append(result)

    return state

def tool_routing(state: AgentState) -> str:
    last_message = state["messages"][-1]
    try:
        if last_message.tool_calls:
            return "tools"
        else:
            return "end"
    except:
        return "end"
    

def entry_node(state: AgentState):
    return user_interface_agent(state)
workflow.add_node("Greeting Node", entry_node)

def parsing_node(state: AgentState):
    return problem_parser_agent(state)
workflow.add_node("Problem Parsing", parsing_node)

def strategy_node(state: AgentState):
    return strategy_agent(state)
workflow.add_node("Strategy", strategy_node)
# workflow.add_node("strategy_tools", run_tools)

## ----- Edges -----
workflow.set_entry_point("Greeting Node")
workflow.add_edge("Greeting Node", "Problem Parsing")
workflow.add_edge("Problem Parsing", "Strategy")
# workflow.add_conditional_edges("Strategy", tool_routing, {"tools":"strategy_tools", "end":END})
# workflow.add_edge("strategy_tools", "Strategy")

workflow.add_edge("Strategy", END)


# ------ Compile Workflow ------
app = workflow.compile()
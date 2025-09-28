from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

from .orchestrator_agent import orchestrator_agent
from .user_interface_agent import user_interface_agent
from .problem_parser_agent import problem_parser_agent
from .strategy_agent import strategy_agent #, tools as planner_agent_tools
from .coder_agent import coder_agent
from .verifier_agent import verifier_agent


# # ------ Load Utility Data ------
# with open('utilities/algo_tech.json', "r", encoding="utf-8") as f:
#     algo_tech = json.load(f)

# ------ Load Tools ------
tools=[]
# Concat all tool lists
# tools = planner_agent_tools

# ------ Define State ------
class AgentState(TypedDict):
    routing: str
    previous_agent: str
    context: str
    messages: list[dict[str, Any]]
    problem_spec: dict
    algorithm_techs: list[str]
    selected_algo: str
    vector_search_results: list[dict[str, Any]]
    pseudocode: str
    verified: bool

def create_agent_state(
        routing='greeting',
        previous_agent='greeting',
        context=None,
        messages=[],
        problem_spec=None,
        algorithm_techs=[],
        selected_algo=None,
        vector_search_results=None,
        pseudocode=None,
        verified=None,
) -> AgentState:
    return AgentState(
        routing=routing,
        previous_agent=previous_agent,
        context=context,
        messages=messages,
        problem_spec=problem_spec,
        algorithm_techs=algorithm_techs,
        selected_algo=selected_algo,
        vector_search_results=vector_search_results,
        pseudocode=pseudocode,
        verified=verified,
    )

# ------ Define Workflow ------
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

def orchestrator(state: AgentState):
    return orchestrator_agent(state)
workflow.add_node("orchestrator", orchestrator)

def agent_routing(state: AgentState) -> str:
    return state["routing"]

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
workflow.add_node("greeting", entry_node)

def parsing_node(state: AgentState):
    return problem_parser_agent(state)
workflow.add_node("parsing", parsing_node)

def strategy_node(state: AgentState):
    return strategy_agent(state)
workflow.add_node("strategy", strategy_node)
# workflow.add_node("strategy_tools", run_tools)

def coder_node(state: AgentState):
    return coder_agent(state)
workflow.add_node("coder", coder_node)

def verify_node(state: AgentState):
    return verifier_agent(state)
workflow.add_node("verifier", verify_node)

## ----- Edges -----
workflow.set_entry_point("greeting")
workflow.add_edge("greeting", "orchestrator")
workflow.add_conditional_edges("orchestrator", 
                               agent_routing, 
                               {"parsing":"parsing", 
                                "strategy":"strategy", 
                                "coder":"coder",
                                "verifier":"verifier",
                                "end":END})
workflow.add_edge("parsing", "orchestrator")
workflow.add_edge("strategy", "orchestrator")
workflow.add_edge("coder", "orchestrator")
workflow.add_edge("verifier", "orchestrator")
# workflow.add_edge("strategy_tools", "Strategy")

# workflow.add_edge("strategy", END)


# ------ Compile Workflow ------
app = workflow.compile()
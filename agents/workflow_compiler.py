from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

from .orchestrator_agent import orchestrator_agent
# from .user_interface_agent import user_interface_agent
from .problem_parser_agent import problem_parser_agent
from .researcher_agent import researcher_agent, tools as reasearch_tools
from .summary_agent import summarizer_agent
from .strategy_agent import strategy_agent #, tools as planner_agent_tools
from .coder_agent import coder_agent
from .prover_agent import prover_agent
from .complexity_agent import complexity_agent
from .verifier_agent import verifier_agent
from .functional_code_agent import real_coder_agent


# # ------ Load Utility Data ------
# with open('utilities/algo_tech.json', "r", encoding="utf-8") as f:
#     algo_tech = json.load(f)

# ------ Load Tools ------
tools=[]
# Concat all tool lists
tools = tools + reasearch_tools

# ------ Define State ------
class AgentState(TypedDict):
    routing: str
    previous_agent: str
    context: str
    messages: list[dict[str, Any]]
    problem_spec: dict
    algorithm_techs: list[str]
    selected_algo: str
    # vector_search_results: list[dict[str, Any]]
    pseudocode: str
    proof: str
    complexity: str
    verified: bool
    real_code_struct: str
    real_code: str
    skip_proof: bool
    research_findings: list[str]
    research_summary: str
    tool_call: dict[str, Any]

def create_agent_state(
        routing='greeting',
        previous_agent='greeting',
        context=None,
        messages=[],
        problem_spec=None,
        algorithm_techs=[],
        selected_algo=None,
        # vector_search_results=None,
        pseudocode=None,
        proof=None,
        complexity=None,
        verified=None,
        real_code_struct=None,
        real_code=None,
        skip_proof=False,
        research_findings=[],
        research_summary=None,
        tool_call=None,
        
) -> AgentState:
    return AgentState(
        routing=routing,
        previous_agent=previous_agent,
        context=context,
        messages=messages,
        problem_spec=problem_spec,
        algorithm_techs=algorithm_techs,
        selected_algo=selected_algo,
        # vector_search_results=vector_search_results,
        pseudocode=pseudocode,
        proof=proof,
        complexity=complexity,
        verified=verified,
        real_code_struct=real_code_struct,
        real_code=real_code,
        skip_proof=skip_proof,
        research_findings=research_findings,
        research_summary=research_summary,
        tool_call=tool_call,
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
    tool_call = state["tool_call"]
    # last_message = state["messages"][-1]
    if not isinstance(tool_call, AIMessage) or not getattr(tool_call, "tool_calls", None):
        # No tool calls, nothing to do
        return state  

    for call in tool_call.tool_calls:
        name = call["name"]
        args = call.get("args", {})
        for tool in tools:
            if name in tool.name:
                result = tool.invoke(args)

                # Append a ToolMessage with the result
                # state["messages"].append(
                #     ToolMessage(name=name, content=result, tool_call_id=call["id"])
                # )
                state["messages"].append({"role":"tool_call", "content": f'Tool {name}: {result}'})
                state["research_findings"].append(result)

    return state

def tool_routing(state: AgentState) -> str:
    # last_message = state["messages"][-1]
    tool_call = state["tool_call"]
    #Max number of search iterations
    if len(state["research_findings"]) > 2:
        return "end"
    try:
        if tool_call.tool_calls:
            return "tools"
        else:
            return "end"
    except:
        return "end"
    

def entry_node(state: AgentState):
    # return user_interface_agent(state)
    return state
workflow.add_node("greeting", entry_node)

def parsing_node(state: AgentState):
    return problem_parser_agent(state)
workflow.add_node("parsing", parsing_node)

def research_node(state: AgentState):
    return researcher_agent(state)
workflow.add_node("research", research_node)
workflow.add_node("research_tools", run_tools)

def summary_node(state: AgentState):
    return summarizer_agent(state)
workflow.add_node("summary", summary_node)

def strategy_node(state: AgentState):
    return strategy_agent(state)
workflow.add_node("strategy", strategy_node)
# workflow.add_node("strategy_tools", run_tools)

def coder_node(state: AgentState):
    return coder_agent(state)
workflow.add_node("coder", coder_node)

def prover_node(state: AgentState):
    return prover_agent(state)
workflow.add_node("prover", prover_node)

def complexity_node(state: AgentState):
    return complexity_agent(state)
workflow.add_node("complexity", complexity_node)

def verify_node(state: AgentState):
    return verifier_agent(state)
workflow.add_node("verifier", verify_node)

def real_coder_node(state: AgentState):
    return real_coder_agent(state)
workflow.add_node("real_coder", real_coder_node)

## ----- Edges -----
workflow.set_entry_point("greeting")
workflow.add_edge("greeting", "parsing")
workflow.add_edge("parsing", "research")
workflow.add_conditional_edges("research", tool_routing, {"tools":"research_tools", "end":"summary"})
workflow.add_edge("research_tools", "research")
workflow.add_edge("summary", "strategy")
workflow.add_edge("strategy", "orchestrator")
workflow.add_conditional_edges("orchestrator", 
                               agent_routing, 
                               {
                                # "parsing":"parsing", 
                                # "strategy":"strategy", 
                                "verifier":"verifier",
                                "coder":"coder",
                                "prover":"prover",
                                "complexity":"complexity",
                                "real_coder":"real_coder",
                                "end":END})
# workflow.add_edge("parsing", "orchestrator")
# workflow.add_edge("strategy", "orchestrator")
workflow.add_edge("coder", "orchestrator")
workflow.add_edge("prover", "orchestrator")
workflow.add_edge("complexity", "orchestrator")
workflow.add_edge("verifier", "orchestrator")
workflow.add_edge("real_coder", "orchestrator")

# research
# workflow.add_node("agent", call_model)
# workflow.add_node("tools", run_tools)

# workflow.add_edge(START, "agent")
# workflow.add_conditional_edges("agent", should_continue, {"tools":"tools", "end":END})
# workflow.add_edge("tools", "agent")

# ------ Compile Workflow ------
app = workflow.compile()
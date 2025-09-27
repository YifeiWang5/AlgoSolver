from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from .user_interface_agent import user_interface_agent
from.problem_parser_agent import problem_parser_agent

# ------ Define State ------
class AgentState(TypedDict):
    context: str | None
    messages: list[dict[str, Any]]
    problem_spec: dict | None

def create_agent_state(
        context=None,
        messages=[],
        problem_spec=None,
) -> AgentState:
    return AgentState(
        context=context,
        messages=messages,
        problem_spec=problem_spec,
    )

# ------ Define Workflow ------
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

## ----- Nodes -----
def entry_node(state: AgentState):
    return user_interface_agent(state)
workflow.add_node("Greeting Node", entry_node)

def parsing_node(state: AgentState):
    return problem_parser_agent(state)
workflow.add_node("Problem Parsing", parsing_node)

## ----- Edges -----
workflow.set_entry_point("Greeting Node")
workflow.add_edge("Greeting Node", "Problem Parsing")

workflow.add_edge("Problem Parsing", END)


# ------ Compile Workflow ------
app = workflow.compile()
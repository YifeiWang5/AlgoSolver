from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from .user_interface_agent import user_interface_agent


# ------ Define State ------
class AgentState(TypedDict):
    context: str | None
    messages: list[dict[str, Any]]

def create_agent_state(
        context=None,
        messages=[],
) -> AgentState:
    return AgentState(
        context=context,
        messages=messages,
    )

# ------ Define Workflow ------
workflow = StateGraph(state_schema=AgentState) #, context_schema=Context

## ----- Nodes -----
def entry_node(state: AgentState):
    return user_interface_agent(state)
workflow.add_node("Greeting Node", entry_node)

## ----- Edges -----
workflow.set_entry_point("Greeting Node")

workflow.add_edge("Greeting Node", END)


# ------ Compile Workflow ------
app = workflow.compile()
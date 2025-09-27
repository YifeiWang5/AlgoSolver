from typing import Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda


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



## ----- Edges -----



# ------ Compile Workflow ------
app = workflow.compile()
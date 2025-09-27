from typing import TypedDict, Any, List
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.prebuilt import ToolNode
from langchain.tools import StructuredTool


# LangSmith Set-Up
import os
import keyring
SERVICE = "langsmith"
USERNAME = "api_key"
os.environ["LANGSMITH_API_KEY"] = keyring.get_password(SERVICE, USERNAME)
os.environ["LANGSMITH_PROJECT"] = "algo_solver"
os.environ["LANGSMITH_TRACING"] = "true"

#OpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')

# llm = ChatOllama(model = "gpt-oss:20b", validate_model_on_init=True)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class AgentState(TypedDict):
    context: str | None
    messages: list[dict[str, Any]]
    research_results: list[dict[str, Any]]
# state = AgentState()
# def create_agent_state()

def vs_search(query: str, search_num: int):
    """
    Similarity search against a FAISS vector store.
    Returns top 'search_num' results as a string.
    """
    store_path="./vector_stores/index"
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.load_local(
    store_path, embeddings, allow_dangerous_deserialization=True
    )
    results = vector_store.similarity_search(query, k=search_num)
    result_str =''
    for i in results:
        # print(f'Doc {i}:\n  {i.page_content}\n')
        result_str = result_str + f'Doc Source: {i.metadata.get('title')}, Page: {i.metadata.get('page')}\nContent: {i.page_content}\n\n\n'

    # return {"messages": [result_str], "research_results": [result_str]}
    return result_str

tools = [
    StructuredTool.from_function(
        func=vs_search,
        name="vs_search",
        description="Search the FAISS vector store and return results as text."
    )]
# tools=[vs_search]
tool_names = ['vs_search']
llm_w_tools = llm.bind_tools(tools)

def call_model(state: AgentState):
    # print(f'\nCALLED LLM\n')
    messages = state["messages"]
    response = llm_w_tools.invoke(messages)
    # print(f'\nLLM RESPONSE: {response}\n')
    # print(f'\nLLM RESPONSE TYPE: {type(response)}\n')
    state["messages"].append(response)
    state["research_results"].append({"search_results":response})
    return state

def should_continue(state: AgentState) -> str:
    # print(f'\nCURRENT MESSAGE LIST: {state["messages"]}\n')
    last_message = state["messages"][-1]#["content"]
    # print(f'\nLAST MESSAGE: {last_message}\n') #.content
    # print(f'\nLAST MESSAGE TYPE: {type(last_message)}\n') #.content
    # print(f'\nTOOL CALL: {last_message.tool_calls}\n')
    try:
        if last_message.tool_calls:
            # print(f'\nGOING TO tools\n')
            return "tools"
        else:
            # print(f'\nGOING TO end\n')
            return "end"
    except:
        # print(f'\nGOING TO end. ERROR\n')
        return "end"
# def merge_messages(old: list, new: list):
#     return old + [m for m in new if m not in old]

# tool_node = ToolNode(tools, 
#                      merge=lambda old_state, new_state: {
#                          "messages": merge_messages(
#                              old_state["messages"], new_state["messages"]
#                          )
#                      })
def run_tools(state: AgentState):
    """
    Custom replacement for ToolNode:
    - Look for tool calls in the last AIMessage
    - Execute them and append ToolMessage outputs
    """
    last_message = state["messages"][-1]
    # print(f'\nLAST MESSAGE LIST (TOOLS): {last_message}\n')
    if not isinstance(last_message, AIMessage) or not getattr(last_message, "tool_calls", None):
        # print('\nNO TOOL_CALL\n')
        return state  # No tool calls, nothing to do

    for call in last_message.tool_calls:
        name = call["name"]
        # print(f"\nNAME: {name}\n")
        args = call.get("args", {})
        # print(f"\nARGS: {args}\n")
        # print(f"\nTOOLS: {tools[0].name}\n")
        for tool in tools:
            if name in tool.name:
            # if name in tool_names:
                # print(f'\nNAME IN TOOLS: {tool}\n')
                # print(f'TOOL ARGS: {tool.invoke(args)}')
                result = tool.invoke(args)

                # Append a ToolMessage with the result
                state["messages"].append(
                    ToolMessage(name=name, content=result, tool_call_id=call["id"])
                )
                # print(f'\nCURRENT MESSAGE LIST (TOOLS): {state["messages"]}\n')
                state["research_results"].append(result)

    return state

# Edges

workflow = StateGraph(AgentState)
# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", run_tools)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools":"tools", "end":END})
workflow.add_edge("tools", "agent")

app = workflow.compile()



# ---------- RUN ----------
if __name__ == "__main__":
    # question = "Graph connectivity and traversal"
    question = "Tell me about algo design from the vector store available to you"
    initial_state = AgentState(context=question, messages=[{"role":"user","content": question}], research_results=[])
    final_state = app.invoke(initial_state)
    print("\n--- RESEARCH SUMMARY ---\n")
    response = final_state["messages"][-1]
    print(response.content)
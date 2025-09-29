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
        pdf_source = i.metadata.get("source").split('\\')[-1].split('.')[0]
        result_str = result_str + f'Doc Source: {pdf_source}, Page: {i.metadata.get('page')}\nContent: {i.page_content}\n\n\n'
    return result_str

tools = [
    StructuredTool.from_function(
        func=vs_search,
        name="vs_search",
        description="Search the FAISS vector store and return results as text."
    )]
# tool_names = ['vs_search']
llm_w_tools = llm.bind_tools(tools)

def call_model(state: AgentState):
    messages = state["messages"]
    response = llm_w_tools.invoke(messages)
    state["messages"].append(response)
    return state

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    try:
        if last_message.tool_calls:
            return "tools"
        else:
            return "end"
    except:
        return "end"
    
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

# Edges

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", run_tools)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools":"tools", "end":END})
workflow.add_edge("tools", "agent")

app = workflow.compile()



# ---------- RUN ----------
if __name__ == "__main__":
    # question = "Graph connectivity and traversal summary"
    question = "Tell me about algo design from the vector store available to you"
    initial_state = AgentState(context=question, messages=[{"role":"user","content": question}], research_results=[])
    final_state = app.invoke(initial_state)
    print("\n--- RESEARCH SUMMARY ---\n")
    response = final_state["messages"][-1]
    print(response.content)
    try:
        research_results = final_state["research_results"][-1]
        print(f'\nSEARCH RESULTS: \n{research_results}')
    except:
        print("\nNo Search Data\n")
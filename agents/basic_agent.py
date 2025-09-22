from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

import os
import keyring
os.environ["TAVILY_API_KEY"] = keyring.get_password('tavily', 'api_key')
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')

# ---------- STATE ----------
class AgentState(TypedDict):
    question: str
    search_queries: List[str]
    search_results: List[str]
    summary: str


# ---------- TOOLS ----------
# Tavily search tool (will call the Tavily API)
tavily = TavilySearchResults(max_results=3)  # adjust max_results as needed


# ---------- NODES ----------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def brainstorm_queries(state: AgentState):
    """Generate 2–3 search queries for the research question."""
    prompt = f"Generate 2 concise web search queries to research:\n{state['question']}"
    resp = llm.invoke([HumanMessage(content=prompt)])
    queries = [q.strip("-• ").strip() for q in resp.content.split("\n") if q.strip()]
    return {"search_queries": queries[:3]}


def gather_results(state: AgentState):
    """Use Tavily to get search results for each query."""
    results = []
    for q in state["search_queries"]:
        tavily_out = tavily.run(q)
        if isinstance(tavily_out, list):
            # Tavily returns list of dicts with 'content' and 'url'
            text = "\n".join([f"- {r.get('content','')} ({r.get('url','')})"
                              for r in tavily_out])
        else:
            text = str(tavily_out)
        results.append(f"### {q}\n{text}")
    return {"search_results": results}


def summarize(state: AgentState):
    """Summarize the Tavily search results."""
    joined = "\n\n".join(state["search_results"])
    prompt = f"Summarize these findings into a concise research brief:\n{joined}"
    resp = llm.invoke([HumanMessage(content=prompt)])
    return {"summary": resp.content}


# ---------- GRAPH ----------
graph = StateGraph(AgentState)
graph.add_node("brainstorm", brainstorm_queries)
graph.add_node("search", gather_results)
graph.add_node("summarize", summarize)

graph.add_edge("__start__", "brainstorm")
graph.add_edge("brainstorm", "search")
graph.add_edge("search", "summarize")
graph.add_edge("summarize", END)

compiled = graph.compile()


# ---------- RUN ----------
if __name__ == "__main__":
    question = "What are the latest breakthroughs in quantum computing?"
    final_state = compiled.invoke({"question": question})
    print("\n--- RESEARCH SUMMARY ---\n")
    print(final_state["summary"])


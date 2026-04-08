from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END, MessagesState, START
from rag.retriever import get_retriever
from langsmith import traceable

retriever = get_retriever()

llm = ChatOllama(model="llama3.2:1b")

# Agent state
class AgentState(MessagesState):
    pass

# nodes
@traceable(name="Retriever Node")
def retriever_node(state: MessagesState)-> dict:
    user_query = state["messages"][-1].content
    context = retriever.invoke(user_query)[0].page_content
    system_msg = f"""
You are a policy and FAQs assistant for cs50 Harvard Online Course. Answer only using the provided policy context.
If not in context, say you don't know.
Policy Context:
{context}
User Question:
{user_query}
"""
    return {
        "messages":[
            {"role":"system","content":system_msg}
        ]
    }

@traceable(name="LLM Agent Node")
def agent_node(state: AgentState):
    response = llm.invoke(state["messages"][-1].content)
    return {
        "messages": [
            {"role":"assistant","content":response.content}
        ]
    }

def create_graph():
    # create a graph
    graph = StateGraph(state_schema=AgentState)
    graph.add_node(action=retriever_node,node="retriever")
    graph.add_node(action=agent_node,node="agent")

    graph.add_edge(START,"retriever")
    graph.add_edge("retriever","agent")
    graph.add_edge("agent",END)

    # compile graph
    bot = graph.compile()
    return bot


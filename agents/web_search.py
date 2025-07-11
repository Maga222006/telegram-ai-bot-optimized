from typing import TypedDict, Annotated, Optional, List
import operator
from datetime import date
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()
model = init_chat_model("groq:meta-llama/llama-4-maverick-17b-128e-instruct", temperature=0)
config = {"configurable": {"thread_id": "1"}}



class State(TypedDict):
    question: str
    context: Annotated[list, operator.add]
    answer: str

from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily.tavily_search import TavilySearch

def search_web(state):
    """ Retrieve docs from web search """

    tavily_search = TavilySearch(
        max_results=3,
        include_answer=True
    )
    try:
        search_docs = tavily_search.invoke(state['question'])
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                for doc in search_docs['results']
            ]
        )
        return {"context": [formatted_search_docs]}
    except:
        pass

def search_wikipedia(state):
    """ Retrieve docs from wikipedia """

    search_docs = WikipediaLoader(
        query=state['question'],
        load_max_docs=2
    ).load()
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context": [formatted_search_docs]}

def generate_answer(state):
    """ Node to answer a question """
    context = state["context"]
    question = state["question"]

    answer_template = (
        'You are an expert research assistant. Based ONLY on the following context, answer the user\'s query: "{question}".\n\n'
        'Use ONLY the provided context — do not hallucinate. If something is unclear or missing, say so honestly.\n'
        'Always refer to your sources using the given URLs or source metadata in parentheses.\n'
        'Provide a helpful, neutral, and factual response.\n'
        'Current date: {date}\n\n'
        'Context:\n{context}'
    )
    answer_instrictions = answer_template.format(
        question=question,
        context=context,
        date=date
    )

    answer = model.invoke([SystemMessage(content=answer_instrictions)]+[HumanMessage(content=f"Answer the question.")]).content

    return {"answer": answer}


builder = StateGraph(State)
builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START,"search_web")
builder.add_edge(START,"search_wikipedia")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()
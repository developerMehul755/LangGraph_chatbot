from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize LLM
llm = GoogleGenerativeAI(model='gemini-2.5-flash')

# State type
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def _extract_text_from_obj(obj: Any) -> str:
    """
    Try a few places where the LLM result text might live.
    Returns a best-effort string.
    """
    # If it's already a BaseMessage, return its content
    if isinstance(obj, BaseMessage):
        return getattr(obj, "content", str(obj))

    # If it's a dict-like object, check common keys
    if isinstance(obj, dict):
        for k in ("content", "text", "message", "output", "output_text", "response"):
            val = obj.get(k)
            if isinstance(val, str) and val.strip():
                return val
            # if nested message dict
            if isinstance(val, dict):
                inner = _extract_text_from_obj(val)
                if inner:
                    return inner
        # fallback: try stringifying the dict
        return str(obj)

    # If the object has attributes we can try
    for attr in ("content", "text", "message", "output_text"):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if isinstance(val, str) and val.strip():
                return val

    # Last resort: stringify
    return str(obj)


def chat_node(state: ChatState):
    messages = state["messages"]

    # Call the LLM. Keep same call you had; we will normalize the output below.
    result = llm.invoke(messages)

    # Normalize: support list/tuple, single object, dict, message object, or plain string
    if isinstance(result, (list, tuple)):
        result_item = result[0] if result else ""
    else:
        result_item = result

    # Extract text from the returned object robustly
    content_text = _extract_text_from_obj(result_item)

    # Build a proper AIMessage to return
    ai_msg = AIMessage(content=content_text)

    # Return in the shape expected by your StateGraph (list under "messages")
    return {"messages": [ai_msg]}


# Build graph and compile
checkpointer = InMemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)


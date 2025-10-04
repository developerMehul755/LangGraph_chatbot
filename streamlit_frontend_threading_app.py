import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config = {'configurable' : {'thread_id' : thread_id}}).values['messages']
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


st.sidebar.title("Langgraph_chatbot")
if st.sidebar.button("New chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in reversed(st.session_state['chat_threads']):
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id=thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content })

        st.session_state['message_history'] = temp_messages
    
# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])   # use markdown so formatting stays nice

user_input = st.chat_input("Type here...")

if user_input:
    # Save user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}

    # Create a *new placeholder* only for this assistant reply
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            stream = chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG
            )

            for event in stream:
                if "chat_node" in event and "messages" in event["chat_node"]:
                    delta = str(event["chat_node"]["messages"][0].content)
                    full_response += delta
                    response_placeholder.markdown(full_response)

        # Once complete, save in history
        st.session_state["message_history"].append(
            {"role": "assistant", "content": full_response}
        )


# 🤖 LangGraph & Streamlit Chatbot

This project is a fully functional chatbot application featuring a backend built with **LangGraph** for managing conversational state and a frontend built with **Streamlit** for a user-friendly, real-time web interface. The chatbot uses Google's Gemini Pro model for its AI responses.

## ✨ Key Features

  * **Interactive UI**: A clean and responsive chat interface built with Streamlit.
  * **Real-time Streaming**: Responses from the AI are streamed token-by-token for a dynamic user experience.
  * **Multi-Conversation Support**: Manage multiple chat sessions simultaneously. You can start a new chat or switch between past conversations using the sidebar.
  * **Session-based Memory**: Chat history is saved for each conversation thread, allowing you to seamlessly pick up where you left off.
  * **Stateful Backend**: LangGraph manages the conversation flow and memory, making the backend logic robust and scalable.

-----

## ⚙️ Architecture Overview

The application is composed of two main parts: a frontend and a backend.

### Backend (`langgraph_backend.py`)

The backend uses **LangGraph** to construct a state machine (`StateGraph`) for the conversation.

  * **State (`ChatState`)**: A simple dictionary that holds the list of messages in the current conversation.
  * **Node (`chat_node`)**: A single function that takes the current state, calls the Google Gemini LLM with the message history, and returns the AI's response.
  * **Memory (`InMemorySaver`)**: LangGraph's checkpointer saves the state (message history) for each unique `thread_id`. This enables persistent memory for each conversation.

### Frontend (`streamlit_app.py`)

The frontend uses **Streamlit** to create an interactive web application.

  * **Session Management**: It uses Streamlit's `st.session_state` to manage the UI and keep track of the current `thread_id` and message history.
  * **Thread Handling**: A unique ID (`uuid`) is generated for each new conversation. These IDs are listed in the sidebar, allowing users to load and continue previous chats.
  * **Streaming Responses**: It communicates with the backend's `chatbot.stream()` method to receive and display the AI's response in real-time.

-----

## 🚀 How to Run

Follow these steps to set up and run the project on your local machine.

### 1\. Prerequisites

  * Python 3.8+
  * A **Google AI API Key**. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2\. Setup Instructions

First, clone the project repository and navigate into the directory.

Second, create and activate a Python virtual environment:

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

Third, create a `requirements.txt` file with the following content:

```txt
streamlit
langgraph
langchain-core
langchain-google-genai
python-dotenv
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

Fourth, create a file named `.env` in the project's root directory. Add your Google API key to this file:

```
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### 3\. Launch the Application

Run the following command in your terminal:

```bash
streamlit run streamlit_app.py
```

Your browser will automatically open with the chatbot interface ready to use.

-----

## 📁 Project File Structure

```
/your-project-folder
|
|-- streamlit_app.py        # Streamlit frontend code
|-- langgraph_backend.py    # LangGraph backend code
|-- requirements.txt        # Python package dependencies
|-- .env                    # Environment variables (API Key)
|-- README.md               # This file
```

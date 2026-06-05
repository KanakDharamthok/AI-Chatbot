import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Environment Setup
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
key = os.getenv("GROQ_API_KEY")

if not key:
    st.error("GROQ_API_KEY not found in environment variables!")
    st.stop()

# 2. Streamlit UI Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="⚡", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
        /* Main App Background Tuning */
        .stApp {
            background-color: #0E1117;
        }
        
        /* Smooth Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #161920 !important;
            border-right: 1px solid #262730;
        }
        
        /* Clean Chat History Buttons Customization */
        div.stButton > button {
            background-color: #1E222B;
            color: #E0E0E0;
            border: 1px solid #2D3139;
            border-radius: 8px;
            transition: all 0.3s ease;
            text-align: left;
            padding: 10px 15px;
        }
        div.stButton > button:hover {
            background-color: #2A2F3B !important;
            border-color: #FF4B4B !important;
            color: #FFFFFF !important;
            transform: translateX(3px);
        }
        
        /* Status Badge Styling */
        .status-badge {
            display: inline-flex;
            align-items: center;
            background-color: #1E291B;
            color: #4CAF50;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid #2E4A2A;
            margin-bottom: 15px;
        }
        .status-dot {
            height: 8px;
            width: 8px;
            background-color: #4CAF50;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            box-shadow: 0 0 8px #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Multi-Session Memory
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "New Chat Session": {
            "history": ChatMessageHistory(),
            "initialized": False
        }
    }

if "current_session" not in st.session_state:
    st.session_state.current_session = "New Chat Session"

# --- SIDEBAR: ChatGPT Style Session & Parameter Management ---
with st.sidebar:
    # App Identity
    st.markdown("## ⚡ AI Engine Control Panel")
    st.markdown('<div class="status-badge"><span class="status-dot"></span>System: Operational</div>', unsafe_allow_html=True)
    
    # Action Button
    if st.button("➕ New Chat", use_container_width=True):
        new_session_id = f"New Chat Session {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_session_id] = {
            "history": ChatMessageHistory(),
            "initialized": False
        }
        st.session_state.current_session = new_session_id
        st.rerun()

    st.write("")
    
    # Hyperparameter Tweaking Hidden Elegantly inside an Expander
    with st.expander("🛠️ Advanced Engine Settings"):
        selected_model = st.selectbox(
            "Model Architecture",
            ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
            index=0
        )
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )
    
    st.write("---")
    st.write("🕒 **Recent Conversations**")
    
    # List historical chat sessions dynamically
    for session_id in list(st.session_state.all_chats.keys()):
        is_active = (session_id == st.session_state.current_session)
        type_str = "▶️  " if is_active else "📄  "
        
        if st.button(f"{type_str}{session_id}", key=session_id, use_container_width=True):
            st.session_state.current_session = session_id
            st.rerun()

# --- MAIN CHAT INTERFACE ---
# Top navigation layout split inside columns
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    st.title("🤖 Your AI Assistant")
    st.caption(f"Engine: `{selected_model}` | Context Instance: `{st.session_state.current_session}`")

with top_col2:
    st.write("")  # Visual alignment spacer
    if st.button("🗑️ Clear Active Chat"):
        st.session_state.all_chats[st.session_state.current_session]["history"].clear()
        st.rerun()

st.write("---")

# 4. Define Prompt Workflow
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly analytical, modern technical assistant."),
    MessagesPlaceholder(variable_name="history"), 
    ("human", "{input}")
])

# 5. Initialize LLM Pipeline
llm = ChatGroq(model=selected_model, api_key=key.strip(), temperature=temperature)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# 6. Session Management Wrap
conversational_chain = RunnableWithMessageHistory(
    chain,
    lambda session_id: st.session_state.all_chats[st.session_state.current_session]["history"],
    input_messages_key="input",
    history_messages_key="history"
)

# 7. Render Stream History Messages
current_session_data = st.session_state.all_chats[st.session_state.current_session]
for message in current_session_data["history"].messages:
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.write(message.content)

# 8. Run Active User Submissions
if user_query := st.chat_input("Type a message or ask a question..."):
    with st.chat_message("user"):
        st.write(user_query)

    # Dynamic Conversational Auto-Naming Routing
    if not current_session_data["initialized"]:
        new_name = user_query[:22] + "..." if len(user_query) > 22 else user_query
        if new_name in st.session_state.all_chats:
            new_name = f"{new_name} ({len(st.session_state.all_chats)})"
            
        st.session_state.all_chats[new_name] = st.session_state.all_chats.pop(st.session_state.current_session)
        st.session_state.all_chats[new_name]["initialized"] = True
        st.session_state.current_session = new_name
        st.rerun()

    # Dynamic Output Generation Token Streaming
    with st.chat_message("assistant"):
        response_stream = conversational_chain.stream(
            {"input": user_query},
            config={"configurable": {"session_id": st.session_state.current_session}}
        )
        st.write_stream(response_stream)

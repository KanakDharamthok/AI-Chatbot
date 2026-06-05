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

# Custom CSS for Premium Look
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }
        section[data-testid="stSidebar"] { background-color: #161920 !important; border-right: 1px solid #262730; }
        div.stButton > button { background-color: #1E222B; color: #E0E0E0; border: 1px solid #2D3139; border-radius: 8px; text-align: left; padding: 10px 15px; }
        div.stButton > button:hover { background-color: #2A2F3B !important; border-color: #FF4B4B !important; color: #FFFFFF !important; }
        .status-badge { display: inline-flex; align-items: center; background-color: #1E291B; color: #4CAF50; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid #2E4A2A; margin-bottom: 15px; }
        .status-dot { height: 8px; width: 8px; background-color: #4CAF50; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 8px #4CAF50; }
        .eval-card { background-color: #1A1E24; padding: 20px; border-radius: 10px; border: 1px solid #FF4B4B; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Multi-Session Memory
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"New Chat Session": {"history": ChatMessageHistory(), "initialized": False}}
if "current_session" not in st.session_state:
    st.session_state.current_session = "New Chat Session"

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.markdown("## ⚡ AI Chatbot Control Center")
    st.markdown('<div class="status-badge"><span class="status-dot"></span>System: Operational</div>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        new_session_id = f"New Chat Session {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_session_id] = {"history": ChatMessageHistory(), "initialized": False}
        st.session_state.current_session = new_session_id
        st.rerun()

    with st.expander("🛠️ Advanced Engine Settings"):
        selected_model = st.selectbox("Model Architecture", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"], index=0)
        temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        
        # NEW FEATURE: Activation for the Evaluation Panel
        eval_mode = st.checkbox("📊 Run Model Evaluation", value=False, help="Runs an LLM-as-a-Judge system to score the model's accuracy.")
    
    st.write("---")
    st.write("🕒 **Recent Conversations**")
    for session_id in list(st.session_state.all_chats.keys()):
        is_active = (session_id == st.session_state.current_session)
        if st.button(f"{'▶️  ' if is_active else '📄  '}{session_id}", key=session_id, use_container_width=True):
            st.session_state.current_session = session_id
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🤖 Your AI Companion")
st.caption(f"Engine: `{selected_model}` | Mode: `{'Evaluation' if eval_mode else 'Standard Conversational'}`")
st.write("---")

# Initialize models
llm = ChatGroq(model=selected_model, api_key=key.strip(), temperature=temperature)
output_parser = StrOutputParser()

# --- EVALUATION ENGINE LOGIC ---
if eval_mode:
    st.subheader("🧪 Automated Testing & Evaluation Arena")
    st.write("Type a prompt below to evaluate how your current model choices perform under analytical criteria.")
    
    eval_query = st.text_input("Enter testing prompt:", placeholder="e.g., Explain quantum computing in 2 sentences.")
    
    if st.button("🚀 Run Evaluation Diagnostics"):
        if eval_query:
            # 1. Run the prompt through the active model configuration
            with st.spinner("Generating Response..."):
                test_prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful assistant."), ("human", "{input}")])
                test_chain = test_prompt | llm | output_parser
                model_output = test_chain.invoke({"input": eval_query})
            
            # Display generated results
            st.markdown("### 🤖 Model Response")
            st.info(model_output)
            
            # 2. Trigger the "LLM-as-a-Judge" sequence using the largest available model
            with st.spinner("Judge is evaluating response performance metrics..."):
                judge_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=key.strip(), temperature=0.0) # Low temp for consistency
                
                judge_prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are an expert AI Model Evaluator. Your job is to grade model outputs strictly based on a User Query.
                    You must score the output from 1 to 5 (with 5 being perfect) on three criteria:
                    1. Accuracy/Helpfulness
                    2. Concision (No unnecessary words)
                    3. Tone/Professionalism
                    
                    Format your final answer exactly like this markdown example:
                    ### 📊 Evaluation Scorecard
                    * **Accuracy/Helpfulness:** [Score]/5 - [Short justification]
                    * **Concision:** [Score]/5 - [Short justification]
                    * **Tone/Professionalism:** [Score]/5 - [Short justification]
                    """),
                    ("human", "User Query: {query}\n\nModel Generated Output: {output}")
                ])
                
                judge_chain = judge_prompt | judge_llm | output_parser
                evaluation_report = judge_chain.invoke({"query": eval_query, "output": model_output})
            
            # Print evaluation report card
            st.markdown('<div class="eval-card">', unsafe_allow_html=True)
            st.markdown(evaluation_report)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a query first!")

# --- STANDARD CHAT INTERFACE LOGIC ---
else:
    # Render history
    current_session_data = st.session_state.all_chats[st.session_state.current_session]
    for message in current_session_data["history"].messages:
        with st.chat_message("user" if message.type == "human" else "assistant"):
            st.write(message.content)

    # Core logic pipeline execution
    prompt = ChatPromptTemplate.from_messages([("system", "You are a helpful assistant."), MessagesPlaceholder(variable_name="history"), ("human", "{input}")])
    chain = prompt | llm | output_parser
    conversational_chain = RunnableWithMessageHistory(chain, lambda session_id: current_session_data["history"], input_messages_key="input", history_messages_key="history")

    if user_query := st.chat_input("Type a message..."):
        with st.chat_message("user"):
            st.write(user_query)

        if not current_session_data["initialized"]:
            new_name = user_query[:22] + "..." if len(user_query) > 22 else user_query
            st.session_state.all_chats[new_name] = st.session_state.all_chats.pop(st.session_state.current_session)
            st.session_state.all_chats[new_name]["initialized"] = True
            st.session_state.current_session = new_name
            st.rerun()

        with st.chat_message("assistant"):
            response_stream = conversational_chain.stream({"input": user_query}, config={"configurable": {"session_id": st.session_state.current_session}})
            st.write_stream(response_stream)

# 🤖 Interactive AI Chatbot with Persistent Session Management

**Enterprise-Grade Multi-Session Intelligence Hub & Automated Evaluation Arena**

* **Live Prototype Link:** [https://ai-chatbot-sig3e4aph79h4fuxbagid4.streamlit.app/](https://ai-chatbot-sig3e4aph79h4fuxbagid4.streamlit.app/)]

---

## 🚀 Project Overview

**AI Chatbot** is a high-performance, real-time conversational ecosystem engineered within a streamlined single-file Python architecture (`app.py`). Moving past basic, stateless API wrappers, this system introduces **isolated contextual memory routing**, **dynamic hyperparameter hot-swapping**, and an **automated LLM-as-a-Judge execution pipeline**. 

The entire framework is optimized using LangChain Expression Language (LCEL) and backed by Groq Cloud’s hardware-accelerated LPU (Language Processing Unit) architecture to deliver sub-second token streaming.

---

## 🛑 Problem Statement

- **System Amnesia & Context Bleeding:** Standard chatbot interfaces frequently suffer from linear session limits or blend distinct chat contexts together, creating chaotic historical environments.
- **High-Latency Bottlenecks:** Traditional GPU cloud infrastructures present token streaming queues that degrade real-time UX during active conversational runs.
- **The "Black Box" Output Risk:** Traditional applications deliver text outputs completely unchecked, lacking empirical metrics to evaluate response quality, conciseness, or tonal compliance before deployment.
- **Clunky Dashboard Layouts:** Baseline dashboard environments position developer variables right inside the main conversational timeline, fracturing user focus.

---

## 💡 Solution

A sleek, unified single-file AI workstation that provides:
- **Isolated Contextual Multi-Chat State Memory:** Seamless thread switching via independent memory blocks.
- **Dynamic ChatGPT-Style Chat Renaming:** Auto-extracts context to label session buttons on the fly.
- **Sub-Second Streaming Powered by Groq LPUs:** Hardware-accelerated real-time token delivery.
- **An Automated Quality Assurance Evaluation Arena:** Rigorous, programmatic model scoring.

---

## ✨ Key Features

- **Isolated State Tab Routing:** Switch between separate coding, writing, and creative threads instantly without cross-contaminating historical context layers.
- **ChatGPT-Style Autonaming:** Eliminates hardcoded names by extracting the first 22 characters of your initial user query to name session buttons dynamically.
- **Advanced Engine Configuration:** Hot-swap models (`llama-3.1-8b-instant` or `llama-3.3-70b-versatile`) and alter creativity vectors via real-time temperature sliders mid-conversation.
- **LLM-as-a-Judge Evaluation Suite:** A dedicated analytical diagnostics view mode that uses a secondary, high-capacity model to score outputs across rigorous metric criteria.
- **Premium CSS SaaS Styling:** Custom dashboard configuration containing sliding state tabs, glassmorphism boundaries, and active operational status badges.

---

## 🎯 Dual-Engine Operational View Modes

### 💬 Standard Conversational Mode
- Interactive chat bubble UI with native token streaming generation.
- Dynamic key-value dictionary routing inside `st.session_state` preserves conversation trees.
- Fast session initialization and context clearing utilities.

### 📊 Automated Evaluation Mode
- **The Core Evaluation Prompt Dataset:** An embedded operational matrix built into the system prompt that forces the judge engine to score text objectively.
- **The Judging Criteria:** Scores outputs from **1 to 5** across three standard engineering metrics:
  1. *Accuracy / Helpfulness*
  2. *Concision (Absence of filler text)*
  3. *Tone / Structural Professionalism*
- Generates a standalone dashboard scorecard panel complete with analytical qualitative justifications.

---

## 🧠 Supported Model Catalog (LPU Architecture)

The interface utilizes LangChain's `ChatGroq` class wrapper to tap into distinct open-weight model branches hosted directly on Groq's deterministic LPU hardware infrastructure.

### 1. Hardcoded Core Implementations
* **`llama-3.1-8b-instant`** (Default Engine): Leverages a 128K context window running at high tokens per second. Optimized for real-time latency and conversational agility.
* **`llama-3.3-70b-versatile`** (Evaluation / Advanced Engine): High-capacity model operating at deterministic `0.0` temperature to serve as the unbiased automated "Judge".

### 2. Supported Drop-In Alternative Architectures
The system's routing block is architecturally ready to scale across alternative open architectures via the Groq endpoint:

| Model ID String | Developer Organization | Context Window | Target Use Case Profile |
| :--- | :--- | :--- | :--- |
| **`qwen3-32b`** | Alibaba (Qwen) | 128K Tokens | Complex localized multi-lingual execution and advanced code generation. |
| **`openai/gpt-oss-120b`** | Open Source Community | 131K Tokens | Ultimate reasoning density, deep logical analysis, and complex macro-chain structuring. |
| **`meta-llama/llama-4-scout-17b-16e-instruct`** | Meta (Llama 4 Preview) | 131K Tokens | Highly efficient Mixture of Experts (MoE) routing for tool use and structured parsing tasks. |
| **`gemma-7b-it`** | Google (Gemma Family) | 8K Tokens | Ultra-lightweight, efficient parameter execution for focused instruction following. |

---

## 🛠️ Technology Stack

- **Frontend & App Interface:** Streamlit (Custom Embedded HTML/CSS)
- **AI Orchestration Framework:** LangChain Expression Language (LCEL)
- **Core LLM Processing Hardware:** Groq Cloud LPU Architecture
- **Underlying Foundations Models:** Meta Llama 3.1 (8B Instant) & Llama 3.3 (70B Versatile)
- **Context Handling Management:** LangChain `ChatMessageHistory` & `RunnableWithMessageHistory`
- **Environment & Secrets Masking:** Python Dotenv (`.env`)
- **Version Control:** Git & GitHub

---

## 📂 Project Directory Structure

```text
├── .venv-1/             # Isolated Python virtual environment activation directory
├── .env                 # Protected local variables file (Stores GROQ_API_KEY)
├── .gitignore           # Safeguards local dependencies and secrets from version control
├── app.py               # Single-file main interface, CSS styles, and model orchestrator
└── requirements.txt     # Explicit project framework requirements

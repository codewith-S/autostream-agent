# 🤖 AutoStream AI Agent (Social-to-Lead Workflow)

##  Overview

This project implements a conversational AI agent for a fictional SaaS platform **AutoStream**, designed to convert user conversations into qualified business leads.

The agent is capable of understanding user intent, retrieving accurate information using a local knowledge base (RAG), and capturing high-intent leads through a structured workflow.

---

##  Features

* Intent Detection (Greeting, Pricing Inquiry, High Intent)
* RAG-based Knowledge Retrieval (from JSON data)
* Multi-step Lead Capture (Name, Email, Platform)
* Tool Execution using mock API
* Stateful Conversation using LangGraph

---

##  Tech Stack

* Python 3.9+
* LangGraph (for workflow orchestration)
* LangChain (conceptually for RAG)
* JSON (knowledge base)

---

##  How to Run

1. Clone the repository:

```
git clone <https://github.com/codewith-S/autostream-agent>
cd autostream-agent
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
python -m pip install -r requirements.txt
```

4. Run the agent:

```
python graph_agent.py
```

---

##  Architecture 

This project uses LangGraph to design a structured conversational AI workflow instead of traditional linear chatbot logic. The agent operates using a state-driven graph where each node represents a specific function such as intent detection, knowledge retrieval, or lead capture.

The flow begins with an intent classification node that determines whether the user query is a greeting, pricing inquiry, or high-intent action. Based on this classification, the graph routes execution to the appropriate node. For informational queries, a Retrieval-Augmented Generation (RAG) approach is used, where responses are generated from a local JSON knowledge base containing pricing and policy details.

For high-intent users, the system transitions into a multi-step lead capture workflow. This process collects user details (name, email, platform) sequentially and ensures that the tool execution occurs only after all required inputs are gathered. State management is handled explicitly using a shared state object, allowing the system to maintain context across multiple conversation turns.

This modular architecture ensures scalability, maintainability, and real-world applicability of the agent.

---

##  WhatsApp Integration 

To integrate this agent with WhatsApp, the Meta WhatsApp Cloud API can be used. Incoming messages are received via webhooks configured on a backend server. These messages are forwarded to the AI agent, which processes the input and generates a response. The response is then sent back to the user through the WhatsApp API.

The webhook acts as a bridge between WhatsApp and the AI agent, enabling real-time conversational interactions. This setup allows the agent to function as a customer engagement tool capable of capturing leads directly from messaging platforms.

---

## Demo

##  Demo Video

[Social-to-Lead Agentic Workflow](https://drive.google.com/file/d/1IdHwl-2jfaihKLJsfokbxs7qf9ngWHYn/view?usp=sharing)

The demo showcases:

1. Pricing query handling using RAG
2. High-intent detection
3. Multi-step lead capture
4. Successful tool execution

---

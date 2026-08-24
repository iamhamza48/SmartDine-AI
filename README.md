# 🍽️ AI Restaurant Manager

An AI-powered restaurant management system designed to automate and simplify restaurant operations through intelligent inventory management, demand forecasting, policy-based assistance, and human-in-the-loop AI workflows.

The system combines **FastAPI, LangGraph, Google Gemini, Supabase/PostgreSQL, LangSmith, and Machine Learning** to provide an intelligent backend for restaurant operations.

---

## 🚀 Features

- 📦 **Inventory Management**
  - Track restaurant inventory
  - Identify low-stock items
  - Retrieve inventory information through APIs

- 🤖 **AI Restaurant Assistant**
  - Natural-language interaction with restaurant data
  - Gemini-powered responses
  - LangGraph-based agent workflows

- 📚 **RAG-Based Policy Assistance**
  - Store restaurant policies as Markdown documents
  - Generate Gemini embeddings
  - Store embeddings in PostgreSQL/Supabase
  - Retrieve relevant policies for AI responses

- 📈 **Demand Forecasting**
  - Train a machine-learning model using historical restaurant data
  - Forecast future demand
  - Evaluate predictions using MAE
  - Save trained models using Joblib

- 👤 **Human-in-the-Loop Approvals**
  - Pause AI workflows when human approval is required
  - Approve or reject proposed actions
  - Resume LangGraph workflows using persistent thread state

- 🧠 **Persistent AI Workflows**
  - Conversation/thread-based state
  - LangGraph persistence and checkpointing

- 🔍 **LangSmith Observability**
  - Trace LangGraph workflows
  - Monitor AI calls and tool execution
  - Debug agent behavior

- 🧪 **Testing**
  - FastAPI endpoint testing with Pytest

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │     Frontend     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │      Backend     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌──────────────┐           ┌──────────────┐
             │  LangGraph   │           │  ML Forecast │
             │  AI Agent    │           │    Model     │
             └──────┬───────┘           └──────────────┘
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
       Gemini     Tools      RAG
          │                   │
          │                   ▼
          │             Policy Embeddings
          │                   │
          └─────────┬─────────┘
                    ▼
             ┌──────────────┐
             │   Supabase   │
             │ PostgreSQL   │
             └──────────────┘

                    │
                    ▼
             ┌──────────────┐
             │  LangSmith   │
             │  Monitoring  │
             └──────────────┘
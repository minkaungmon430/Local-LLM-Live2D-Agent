# 🐾 Mochi: Autonomous Local AI Desktop Agent

An asynchronous, event-driven AI desktop assistant powered by local LLMs and Live2D WebSocket integration. 

Unlike standard text-based chatbots, this project bridges a local language model (Llama 3.2) with a graphical Live2D frontend (VTube Studio) to create an autonomous, emotive, and system-aware virtual companion.

## 🚀 Architecture & Tech Stack
* **LLM Backend:** `Ollama` running `llama3.2` locally for zero-latency, privacy-first inference.
* **Middleware:** Python `asyncio` and `WebSockets` for non-blocking execution.
* **Frontend:** `VTube Studio API` for rendering Live2D models and triggering state-based animations via JSON payloads.

## 🧠 How It Works
1. **Prompt & Generation:** The user interacts via the terminal. The Python script queries the local Llama model, which is contextually prompted to act as "Mochi," an energetic chibi mascot.
2. **Context Parsing:** The LLM injects specific emotion tags (e.g., `[LOVE]`, `[STAR]`, `[CRY]`) into its response based on the conversation's context.
3. **Event-Driven Execution:** The Python script strips the tags from the user-facing text and asynchronously sends a Hotkey Trigger request via WebSockets to VTube Studio on Port 8001.
4. **Seamless Rendering:** The Live2D avatar reacts instantly on the user's desktop without requiring window focus or physical keyboard macros.

## 🛠️ Prerequisites
* **Python 3.10+**
* **Ollama** installed with `llama3.2` pulled locally.
* **VTube Studio** installed via Steam (with API started on Port 8001).

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/mochi-ai-agent.git](https://github.com/YourUsername/mochi-ai-agent.git)
   cd mochi-ai-agent

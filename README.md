7# Multi-Agent-AI-Writer
🤖 Multi-Agent AI Writer

A simple Multi-Agent AI application built with Streamlit and OpenRouter API. This project demonstrates an agentic AI workflow where two specialised AI agents collaborate to produce high-quality content.

🚀 Features

- ✍️ Writer Agent generates an initial draft based on a given topic.
- 📝 Editor Agent reviews and improves the draft.
- 🤖 Uses the OpenRouter API for AI inference.
- 🌐 Simple and interactive Streamlit interface.
- ☁️ Deployable on Streamlit Community Cloud.

🏗️ Multi-Agent Workflow

User Topic
     │
     ▼
┌─────────────────┐
│ Writer Agent    │
│ Generates Draft │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Editor Agent    │
│ Reviews &       │
│ Improves Draft  │
└────────┬────────┘
         │
         ▼
   Final Polished Output

🛠️ Tech Stack

- Python
- Streamlit
- OpenRouter API
- OpenAI Python SDK

📂 Project Structure

multi-agent-ai-writer/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
└── .streamlit/
    └── secrets.toml



🔑 Environment Setup

Create a ".streamlit/secrets.toml" file and add your OpenRouter API key:

OPENROUTER_API_KEY="your_openrouter_api_key"

▶️ Run the Application

streamlit run app.py

The application will open in your default web browser.

📖 Example Topics

- Benefits of Artificial Intelligence in Healthcare
- Importance of Cybersecurity Awareness
- Future of Cloud Computing
- Role of Generative AI in Education

🎯 Learning Outcomes

This project demonstrates:

- Multi-Agent AI orchestration
- Agentic prompting
- Prompt engineering
- Sequential AI pipelines
- OpenRouter API integration
- Streamlit application development

📌 Future Improvements

- Support for more specialised agents
- Tone and style selection
- Export results as PDF or Markdown
- Conversation history
- Multiple AI model support

live:https://multi-agent-ai-writer-drfgrnyylst76ocujciyps.streamlit.app/
.
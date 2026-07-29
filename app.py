import streamlit as st
from openai import OpenAI
import math

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="🤖 Multi-Agent AI Writer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Writer")
st.markdown(
    "A simple **2-Agent AI System** where **Agent 1** writes a draft and **Agent 2** reviews & improves it."
)

# ------------------------------------
# OpenRouter Client
# ------------------------------------
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# Change if you want another model
MODEL = "inclusionai/ling-3.0-flash:free"


# ------------------------------------
# Writer Agent
# ------------------------------------
def writer_agent(topic):

    system_prompt = """
You are Agent 1.

Role:
Professional Content Writer.

Task:
Write a well-structured article about the given topic.

Rules:
- Around 200 words.
- Use a title.
- Use short paragraphs.
- Simple English.
- Do NOT critique yourself.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role":"user",
                    "content":topic
                }
            ],
            temperature=0.7,
            max_tokens=300,
            extra_body={
                "reasoning":{
                    "enabled":False
                }
            }
        )

        return response.choices[0].message.content

    except Exception as e:

        st.error(f"Writer Agent Error\n\n{e}")
        st.stop()


# ------------------------------------
# Editor Agent
# ------------------------------------
def editor_agent(draft):

    system_prompt = """
You are Agent 2.

Role:
Senior Editor.

Responsibilities:

- Fix grammar
- Improve clarity
- Improve vocabulary
- Improve structure
- Remove repetition
- Make it professional

Return ONLY the improved article.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role":"user",
                    "content":draft
                }
            ],
            temperature=0.3,
            max_tokens=400,
            extra_body={
                "reasoning":{
                    "enabled":False
                }
            }
        )

        return response.choices[0].message.content

    except Exception as e:

        st.error(f"Editor Agent Error\n\n{e}")
        st.stop()


# ------------------------------------
# Utility Functions
# ------------------------------------
def word_count(text):
    return len(text.split())


def character_count(text):
    return len(text)


def reading_time(text):
    return max(1, math.ceil(word_count(text) / 200))
# ------------------------------------
# User Interface
# ------------------------------------

st.divider()

topic = st.text_input(
    "📝 Enter a topic",
    placeholder="Example: Importance of Artificial Intelligence"
)

generate = st.button("🚀 Generate")

if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    # Writer Agent
    with st.spinner("✍️ Agent 1 is writing..."):
        draft = writer_agent(topic)

    # Editor Agent
    with st.spinner("📝 Agent 2 is improving..."):
        final = editor_agent(draft)

    st.success("✅ Multi-Agent pipeline completed successfully!")

    st.divider()

    # -------------------------
    # Side-by-side comparison
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍️ Agent 1 - Writer Draft")
        st.text_area(
            "Writer Output",
            draft,
            height=350
        )

    with col2:
        st.subheader("📝 Agent 2 - Final Edited Version")
        st.text_area(
            "Editor Output",
            final,
            height=350
        )

    st.divider()

    # -------------------------
    # Statistics
    # -------------------------
    st.subheader("📊 Before vs After")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Word Count",
            word_count(final),
            word_count(final) - word_count(draft)
        )

    with m2:
        st.metric(
            "Characters",
            character_count(final),
            character_count(final) - character_count(draft)
        )

    with m3:
        st.metric(
            "Reading Time",
            f"{reading_time(final)} min"
        )

    st.divider()

    # -------------------------
    # Improvements
    # -------------------------
    st.subheader("📌 What the Editor Improved")

    improve1, improve2 = st.columns(2)

    with improve1:
        st.error("""
### Writer Draft

- Basic wording
- Simple sentence structure
- Minor repetition
- Less polished
- Initial draft
""")

    with improve2:
        st.success("""
### Editor Version

- Better grammar
- Improved clarity
- Professional tone
- Better structure
- Reduced repetition
""")

    st.divider()

    st.subheader("🎯 Agent Workflow")

    st.info("""
User Topic
      ↓
✍️ Agent 1 (Writer)
      ↓
Draft
      ↓
📝 Agent 2 (Editor)
      ↓
Final Improved Version
""")

    st.divider()

    st.download_button(
        "📥 Download Final Article",
        final,
        file_name="final_article.txt",
        mime="text/plain"
    )

    st.success("Project completed successfully using a 2-Agent AI workflow.")
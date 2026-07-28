import streamlit as st
from openai import OpenAI

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Multi-Agent AI Writer", page_icon="🤖")

st.title("🤖 Multi-Agent AI Writer")
st.write(
    "Agent 1 writes a draft. Agent 2 reviews and improves it."
)

# -------------------------------
# OpenRouter Client
# -------------------------------
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-4.1-mini"

# -------------------------------
# Agent 1
# -------------------------------
def writer_agent(topic):

    system_prompt = """
You are an expert content writer.

Your responsibilities:
- Write a clear article.
- Around 200-250 words.
- Use headings if appropriate.
- Do NOT critique yourself.
"""

    response = client.chat.completions.create(
        model= "meta-llama/llama-3.3-70b-instruct",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":topic}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content


# -------------------------------
# Agent 2
# -------------------------------
def editor_agent(draft):

    system_prompt = """
You are a senior editor.

Improve the draft by:
- Fixing grammar
- Improving clarity
- Improving structure
- Removing repetition
- Making it professional

Return ONLY the improved article.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":draft}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# -------------------------------
# UI
# -------------------------------
topic = st.text_input(
    "Enter a topic",
    placeholder="Example: Importance of Cybersecurity Awareness"
)

if st.button("Generate"):

    if topic == "":
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("✍️ Writer Agent is drafting..."):
        draft = writer_agent(topic)

    with st.spinner("📝 Editor Agent is improving..."):
        final = editor_agent(draft)

    st.subheader("🧑‍💻 Agent 1 - Writer Draft")
    st.write(draft)

    st.divider()

    st.subheader("✅ Agent 2 - Final Edited Version")
    st.write(final)

    st.divider()

    st.subheader("📌 What the Editor Improved")

    improvements = [
        "✔ Grammar",
        "✔ Clarity",
        "✔ Professional Tone",
        "✔ Better Flow",
        "✔ Reduced Repetition"
    ]

    for item in improvements:
        st.write(item)
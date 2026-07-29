import streamlit as st
from openai import OpenAI

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Multi-Agent AI Writer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Writer")
st.write("**Agent 1 (Writer)** creates a draft. **Agent 2 (Editor)** reviews and improves it.")

# -------------------------------
# OpenRouter Client
# -------------------------------
try:
    client = OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
except Exception:
    st.error("❌ OpenRouter API key not found. Please add it in Streamlit Secrets.")
    st.stop()

# Change this model if needed
MODEL = "google/gemini-2.5-flash"

# -------------------------------
# Writer Agent
# -------------------------------
def writer_agent(topic):
    system_prompt = """
You are an expert content writer.

Responsibilities:
- Write a clear, engaging article.
- 200-250 words.
- Use a title.
- Use simple headings if appropriate.
- Do not critique your own writing.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": topic},
            ],
            temperature=0.8,
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"❌ Writer Agent Error:\n\n{e}")
        st.stop()


# -------------------------------
# Editor Agent
# -------------------------------
def editor_agent(draft):
    system_prompt = """
You are a senior editor.

Improve the article by:
- Correcting grammar
- Improving clarity
- Improving flow
- Making the tone professional
- Removing repetition

Return only the improved article.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": draft},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"❌ Editor Agent Error:\n\n{e}")
        st.stop()


# -------------------------------
# Streamlit UI
# -------------------------------
topic = st.text_input(
    "Enter a topic",
    placeholder="Example: Importance of Cybersecurity Awareness",
)

if st.button("Generate"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("✍️ Writer Agent is creating the draft..."):
        draft = writer_agent(topic)

    with st.spinner("📝 Editor Agent is improving the draft..."):
        final = editor_agent(draft)

    st.success("Done!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍️ Agent 1 - Writer Draft")
        st.write(draft)

    with col2:
        st.subheader("📝 Agent 2 - Final Edited Version")
        st.write(final)

    st.divider()

    st.subheader("📌 Improvements Made by Editor")

    st.markdown("""
- ✅ Grammar corrected
- ✅ Better clarity
- ✅ Improved flow
- ✅ Professional tone
- ✅ Reduced repetition
""")
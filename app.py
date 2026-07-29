import streamlit as st
from openai import OpenAI

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Multi-Agent AI Writer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Writer")
st.write("Agent 1 (Writer) creates a draft. Agent 2 (Editor) reviews and improves it.")

# -------------------------------
# OpenRouter Client
# -------------------------------
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# Free model
MODEL = "google/gemma-3-4b-it:free"


# -------------------------------
# Writer Agent
# -------------------------------
def writer_agent(topic):

    system_prompt = """
You are a professional content writer.

Write an article of about 200 words.

Requirements:
- Clear title
- Well-structured
- Easy to understand
- Do not explain your thinking.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": topic}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Writer Agent Error:\n\n{e}")
        st.stop()


# -------------------------------
# Editor Agent
# -------------------------------
def editor_agent(draft):

    system_prompt = """
You are a senior editor.

Improve the draft by:
- Fix grammar
- Improve clarity
- Improve flow
- Remove repetition
- Make it professional

Return ONLY the improved article.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": draft}
            ],
            temperature=0.3,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Editor Agent Error:\n\n{e}")
        st.stop()


# -------------------------------
# UI
# -------------------------------
topic = st.text_input(
    "Enter a topic",
    placeholder="Example: Importance of Cybersecurity"
)

if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("✍️ Writer Agent is creating draft..."):
        draft = writer_agent(topic)

    with st.spinner("📝 Editor Agent is improving draft..."):
        final = editor_agent(draft)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍️ Agent 1 Draft")
        st.write(draft)

    with col2:
        st.subheader("📝 Agent 2 Final Version")
        st.write(final)

    st.divider()

    st.subheader("Editor Improvements")

    st.markdown("""
- ✅ Improved grammar
- ✅ Better clarity
- ✅ Better flow
- ✅ Professional tone
- ✅ Removed repetition
""")
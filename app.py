
%%writefile app.py

import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎓",
    layout="wide"
)

# Application heading
st.title("🎓 AI Learning Roadmap Generator")
st.write(
    "Create a personalized learning roadmap "
    "with the power of Artificial Intelligence."
)

st.divider()

# User inputs
st.subheader("Tell us about your learning goals")

field = st.text_input(
    "What do you want to learn?",
    placeholder="Example: Data Science, Python, Web Development"
)

level = st.selectbox(
    "Select your current skill level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.selectbox(
    "How much time do you have?",
    ["1 Month", "2 Months", "3 Months",
     "6 Months", "12 Months"]
)

daily_hours = st.selectbox(
    "How many hours can you study daily?",
    [1, 2, 3, 4, 5, 6, 8]
)

# Generate roadmap
if st.button("🚀 Generate My Learning Roadmap", use_container_width=True):

    if not field.strip():
        st.warning("Please enter a learning field.")
        st.stop()

    # Get API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.error("Groq API key is missing. Configure GROQ_API_KEY.")
        st.stop()

    # Initialize Groq
    client = Groq(api_key=api_key)

    # Create AI prompt
    prompt = f"""
    You are an expert learning and career roadmap advisor.

    Create a detailed and realistic learning roadmap.

    Learning Field: {field}
    Skill Level: {level}
    Available Time: {duration}
    Daily Study Hours: {daily_hours}

    Follow these instructions:

    1. Start with an introduction and learning objectives.
    2. List the prerequisites.
    3. Create a week-by-week learning roadmap.
    4. Explain what topics to study each week.
    5. Recommend tools and technologies.
    6. Include practical exercises.
    7. Suggest at least three projects with increasing difficulty.
    8. Recommend free learning resources and documentation.
    9. Include a final portfolio project.
    10. Give career preparation advice.

    Make the roadmap suitable for the selected skill level.
    Divide the available learning time into realistic weekly goals.
    Account for the user's daily study hours.
    Use clear headings, bullet points and tables where useful.
    Do not invent specific courses or resource URLs.
    """

    # Generate response
    try:
        with st.spinner("AI is creating your personalized roadmap..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional learning roadmap "
                            "generator. Give practical, structured "
                            "and realistic learning advice."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=3500
            )

            roadmap = response.choices[0].message.content

        if roadmap:
            st.success("Your learning roadmap is ready!")

            st.markdown(roadmap)

            st.download_button(
                label="📥 Download Roadmap",
                data=roadmap,
                file_name="learning_roadmap.md",
                mime="text/markdown"
            )
        else:
            st.error("The AI returned an empty response.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.divider()

st.caption("Built with Python, Streamlit and Groq AI")

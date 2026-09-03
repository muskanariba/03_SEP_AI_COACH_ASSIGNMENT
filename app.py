import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
import os

from prompts import (
    zero_shot_prompt,
    few_shot_prompt,
    structured_prompt
)

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Study Coach",
    layout="centered"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:900px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load Gemini API
# ----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")

# ----------------------------
# PDF Function
# ----------------------------
def create_pdf(text):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("AI Study Coach", styles["Title"]))

    for line in text.split("\n"):
        if line.strip():
            story.append(
                Paragraph(line, styles["BodyText"])
            )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()

# ----------------------------
# Header
# ----------------------------

st.markdown(
"""
<h1 style='text-align:center;'>
AI Study Coach
</h1>

<p style='text-align:center;color:gray;'>
Personalized Study Plan Generator using Google Gemini
</p>
""",
unsafe_allow_html=True
)

# ----------------------------
# Student Information
# ----------------------------

st.subheader("Student Information")

left,right=st.columns(2)

with left:

    name=st.text_input("Student Name")

    subject=st.text_input("Subject")

    days=st.number_input(
        "Days Before Exam",
        min_value=1,
        value=5
    )

with right:

    hours=st.number_input(
        "Study Hours Per Day",
        min_value=1,
        value=2
    )

    skill=st.selectbox(
        "Skill Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

weak_topics=st.text_area(
    "Weak Topics",
    placeholder="Example: Loops, Functions, Debugging"
)

st.subheader("Prompting Technique")

technique=st.selectbox(
    "Select Prompting Technique",
    [
        "Zero-Shot",
        "Few-Shot",
        "Structured Reasoning"
    ]
)

generate=st.button(
    "Generate Study Plan",
    use_container_width=True
)
# ----------------------------
# Generate Study Plan
# ----------------------------

if generate:

    if not name.strip() or not subject.strip() or not weak_topics.strip():
        st.warning("Please fill in all required fields.")

    else:

        if technique == "Zero-Shot":
            prompt = zero_shot_prompt(
                name,
                subject,
                weak_topics,
                days,
                hours,
                skill
            )

        elif technique == "Few-Shot":
            prompt = few_shot_prompt(
                name,
                subject,
                weak_topics,
                days,
                hours,
                skill
            )

        else:
            prompt = structured_prompt(
                name,
                subject,
                weak_topics,
                days,
                hours,
                skill
            )

        try:

            with st.spinner("Generating study plan..."):
                response = model.generate_content(prompt)

            study_plan = response.text

            st.success("Study Plan Generated Successfully")

            st.subheader("Generated Study Plan")

            st.markdown(
                f"""
<div style="
background:#f8f9fa;
padding:20px;
border-radius:10px;
border:1px solid #dcdcdc;
white-space:pre-wrap;
">
{study_plan}
</div>
""",
                unsafe_allow_html=True,
            )

            pdf = create_pdf(study_plan)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="Download PDF",
                    data=pdf,
                    file_name="Study_Plan.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

            with col2:
                st.download_button(
                    label="Download TXT",
                    data=study_plan,
                    file_name="Study_Plan.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed using Python, Streamlit and Google Gemini API")
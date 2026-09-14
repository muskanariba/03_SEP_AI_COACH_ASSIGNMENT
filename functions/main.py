from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Gemini API Key
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/", methods=["GET"])
def home():
    return "AI Study Coach Backend is running"


@app.route("/generate", methods=["POST"])
def generate_study_plan():

    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        subject = data.get("subject", "").strip()
        weak_topics = data.get("weak_topics", "").strip()
        days = data.get("days", "")
        hours = data.get("hours", "")
        skill = data.get("skill", "")
        technique = data.get("technique", "")

        if not name or not subject or not weak_topics:
            return jsonify({
                "error": "Please fill in all required fields."
            }), 400


        # -------------------------
        # ZERO-SHOT
        # -------------------------

        if technique == "Zero-Shot":

            prompt = f"""
You are an AI Study Coach.

Analyze the following student information and create a personalized study plan.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Tasks:
1. Identify weak areas.
2. Prioritize important topics.
3. Create a day-by-day study schedule.
4. Recommend suitable study activities.

Provide only the final study plan.
"""


        # -------------------------
        # FEW-SHOT
        # -------------------------

        elif technique == "Few-Shot":

            prompt = f"""
Example 1:

Student:
SQL exam in 3 days.
Weak Topic: SQL Joins.

Recommended Plan:

Day 1:
Study INNER, LEFT, RIGHT and FULL joins.

Day 2:
Practice SQL Join Queries.

Day 3:
Mock Test and Revision.


Example 2:

Student:
Python exam in 7 days.
Weak Topic:
Object Oriented Programming.

Recommended Plan:

Day 1-2:
Classes and Objects.

Day 3-4:
Inheritance and Polymorphism.

Day 5-6:
Coding Practice.

Day 7:
Revision and Mock Test.


Now create a similar personalized study plan for:

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Provide only the final study plan.
"""


        # -------------------------
        # STRUCTURED REASONING
        # -------------------------

        elif technique == "Structured Reasoning":

            prompt = f"""
You are an AI Study Coach.

Analyze the student's situation using the following structured process.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Follow these steps:

1. Identify the weak topics.
2. Prioritize the most important topics.
3. Consider the number of days remaining.
4. Consider the available study hours per day.
5. Recommend suitable learning activities.
6. Create a day-by-day study plan.
7. Give a short explanation for each recommendation.

Do not reveal internal reasoning.
Only provide the final structured study plan.
"""


        else:

            return jsonify({
                "error": "Invalid prompting technique."
            }), 400


        # -------------------------
        # GEMINI
        # -------------------------

        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "study_plan": response.text
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
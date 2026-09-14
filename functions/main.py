import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai


app = Flask(__name__)

CORS(app)


# Gemini client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/", methods=["GET"])
def home():
    return "AI Study Coach Backend is running"


@app.route("/generate", methods=["POST"])
def generate():

    try:
        data = request.get_json()

        name = data.get("name", "")
        subject = data.get("subject", "")
        weak_topics = data.get("weak_topics", "")
        days = data.get("days", "")
        hours = data.get("hours", "")
        skill = data.get("skill", "")
        technique = data.get("technique", "Zero-Shot")


        # --------------------------------
        # Zero-Shot Prompt
        # --------------------------------

        if technique == "Zero-Shot":

            prompt = f"""
You are an AI Study Coach.

Create a personalized study plan for the following student.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Tasks:

1. Identify the student's weak areas.
2. Prioritize the most important topics.
3. Create a realistic day-by-day study schedule.
4. Recommend suitable learning activities.
5. Include revision and practice.
6. Make the plan suitable for the student's skill level.

Provide only the final study plan.
Do not reveal internal reasoning.
"""


        # --------------------------------
        # Few-Shot Prompt
        # --------------------------------

        elif technique == "Few-Shot":

            prompt = f"""
You are an AI Study Coach.

Use the following examples as patterns for creating a personalized
study plan.

Example 1:

Student:
SQL exam in 3 days.
Weak Topic: SQL Joins.

Recommended Plan:
Day 1: Learn INNER, LEFT, RIGHT and FULL joins.
Day 2: Practice SQL join queries.
Day 3: Mock test and revision.


Example 2:

Student:
Python exam in 7 days.
Weak Topic: Object Oriented Programming.

Recommended Plan:
Day 1-2: Classes and Objects.
Day 3-4: Inheritance and Polymorphism.
Day 5-6: Coding Practice.
Day 7: Revision and Mock Test.


Now create a similar personalized plan for:

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Use the examples as a formatting and planning guide.

Provide only the final study plan.
"""


        # --------------------------------
        # Structured Reasoning Prompt
        # --------------------------------

        else:

            prompt = f"""
You are an AI Study Coach.

Create a structured study plan for this student.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Follow this structured process:

1. Identify the weak topics.
2. Prioritize the topics.
3. Consider the number of days remaining.
4. Consider the available study hours.
5. Select appropriate learning activities.
6. Create a day-by-day study schedule.
7. Include revision and practice.
8. Give a short explanation for the recommendations.

Do not reveal hidden chain-of-thought or internal reasoning.

Only provide the final structured answer.
"""


        # --------------------------------
        # Gemini Interactions API
        # --------------------------------

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )


        study_plan = interaction.output_text


        return jsonify({
            "success": True,
            "study_plan": study_plan
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
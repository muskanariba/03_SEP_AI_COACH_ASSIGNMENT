def zero_shot_prompt(name, subject, weak_topics, days, hours, skill):

    return f"""
You are an AI Study Coach.

Analyze the following student information and create a study plan.

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
"""



def few_shot_prompt(name, subject, weak_topics, days, hours, skill):

    return f"""
Example 1

Student:
SQL exam in 3 days.
Weak Topic: SQL Joins

Recommended Plan

Day 1:
Study INNER, LEFT, RIGHT and FULL joins.

Day 2:
Practice SQL Join Queries.

Day 3:
Mock Test and Revision.


Example 2

Student:
Python exam in 7 days.
Weak Topic:
Object Oriented Programming

Recommended Plan

Day 1-2:
Classes and Objects

Day 3-4:
Inheritance and Polymorphism

Day 5-6:
Coding Practice

Day 7:
Revision and Mock Test


Now create a study plan for this student.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}
"""



def structured_prompt(name, subject, weak_topics, days, hours, skill):

    return f"""
You are an AI Study Coach.

Analyze the student step by step.

Student Name: {name}
Subject: {subject}
Weak Topics: {weak_topics}
Days Before Exam: {days}
Study Hours Per Day: {hours}
Skill Level: {skill}

Follow these steps:

1. Identify weak topics.
2. Prioritize the most important topics.
3. Consider the remaining exam days.
4. Consider daily study hours.
5. Recommend suitable learning activities.
6. Create a day-by-day study plan.
7. Give a short explanation for each recommendation.

Do not reveal internal reasoning.
Only provide the final structured answer.
"""
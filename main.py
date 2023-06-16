import os
import pandas as pd
import textract 
import matplotlib.pyplot as plt
from pathlib import Path
from classes import Student, Course
import openai
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts import Prompt
from langchain.chains import ConversationalRetrievalChain

openai.api_key = "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" #API key is used for connection with ChatGPT 
#openai.organization = "org-8CvvT3mCplTB5TmLU85AYXZx"

masterPrompt = """You are a college student advisor, you will 
use the course data and student data that are provided. First check whether
the student has taken the prerequired courses. By taking the student's GPA and major as reference, 
check whether the course is suitable for the student. Finally, state whether
is it recommended for the student to take this course. Use the following data for the student and the course:

Student {
Name: student_name, 
Level: student_level, 
Taken Courses: student_taken_courses, 
Major: student_major, 
GPA: student_gpa
}
----------------------------------
Course{
Name: course_name,
Code: course_code, 
Syllabus: course_syllabus, 
Prerequisites: course_prerequisites
}
"""

def create_prompt(student,course,prompt):
    prompt = prompt.replace('stundent_name',student.name)
    prompt = prompt.replace('student_level',student.level)
    prompt = prompt.replace('student_taken_courses'," ".join(x for x in student.taken_courses))
    prompt = prompt.replace('student_major',student.major)
    prompt = prompt.replace('student_gpa',str(student.gpa))
    prompt = prompt.replace('course_name',course.name)
    prompt = prompt.replace('course_code',course.code)
    prompt = prompt.replace('course_syllabus',course.syllabus)
    prompt = prompt.replace('course_prerequisites'," ".join( x for x in course.prerequisites))
    return prompt

def send_query(prompt, model="text-davinci-003"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

doc = textract.process("/Users/selinceydeli/Desktop/AI Research/llm_dev/CS301-Syllabus-2022-2023-Spring-v4.pdf")

with open('CS301-Syllabus-2022-2023-Spring-v4.txt', 'w') as f:
    f.write(doc.decode('utf-8'))

with open('CS301-Syllabus-2022-2023-Spring-v4.txt', 'r') as f:
    text = f.read()

textSplitter = CharacterTextSplitter(chunk_size=2000, separator="\n")

student = Student(name='Nusret',level='Junior',taken_courses=['CS300'],major='Computer Science',gpa=3.5)

course = Course(name='Algorithms',code='CS301',syllabus=text,prerequisites=['CS300'])

text_prompt = create_prompt(student,course,masterPrompt)

response = send_query(text_prompt)

print(response)
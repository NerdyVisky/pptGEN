from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pylatex import Document, Math, Command
import re
import os
import fitz
import json
import subprocess
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import display, Latex
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import convert_pydantic_to_openai_function
from utils.prompts import content

# declare a list of courses
courses = [
    "Introduction to Computer Science",
    "Introduction to Machine Learning",
    "Data Structures and Algorithms",
    "Computer Organization and Architecture",
    "Maths for Computing",
    "Pattern Recognition and Machine Learning",
    "Software Engineering",
    "Digital Design",
    "Principles of Computer Systems - I",
    "Principles of Computer Systems - II",
    "Design and Analysis of Algorithms",
    "Computer Architecture",
    "Operating Systems",
    "Principles of Programming Languages",
    "Database Systems",
    "Principles of Computer Systems - I",
    "Principles of Computer Systems - II",
    "Computer Networks",
    "Artificial Intelligence",
    "Computer Networks",
    "Optimization for Machine Learning",
    "Deep Learning",
    "Data Engineering",
    "Social Networks",
    "Data Visualization",
    "Cyber Security",
    "Artificial Intelligence - I",
    "Machine Learning - I",
    "Machine Learning - I: Supervised Learning",
    "Machine Learning - I: Unsupervised Learning and Generative Models",
    "Machine Learning - I: Computational Theory and Deep Neural Network",
    "Algorithms for Big Data",
    "Artificial Intelligence - 2",
    "Probabilistic Reasoning and Knowledge Representation",
    "Making Decisions",
    "Reinforcement Learning",
    "Machine Learning - 2",
    "Introduction to Deep Learning",
    "Representation Learning &amp; Structured Models",
    "Deep Generative Models",
    "Real Time Autonomous System",
    "Computer Architecture",
    "Multi System Architecture",
    "Multicore Processing",
    "Fundamentals of Parallel Programming",
    "Security and Applications",
    "Introduction to Information Security",
    "Software and Data Engineering",
    "Cloud Computing and Virtualization",
    "Data Management",
    "Data Intensive Processing Systems",
    "Social Network Analysis",
    "Machine Learning with Big Data",
    "Complexity Theory",
    "Graph-theoretic Algorithms",
    "Data Visualization",
    "Vehicular Adhoc Networks",
    "Digital Image Analysis",
    "Neuromorphic Computing and Design",
    "Introduction to Neuromorphic Engineering",
    "Neuromorphic Computing",
    "Neuromorphic Hardware Implementation",
    "Natural Language Processing",
    "Selected Topics in AI",
    "Computer Vision",
    "Dependable AI",
    "Bioimage Computing",
    "Social Network Analysis",
    "Graph Theory and Applications",
    "Principles of Biological Vision",
    "Advanced Biometrics",
    "Ubiquitous Computing",
    "Computer Graphics",
    "Mobile and Pervasive Computing",
    "Advanced Algorithm",
    "Cryptography",
    "Introduction to Blockchain",
    "Virtualization and Cloud Computing",
    "GPU Programming",
    "Advanced Machine Learning",
    "Artificial Intelligence",
    "Machine Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Kernels and Neural Networks",
    "Advanced Data Structure and Algorithms",
    "Data Structure and Algorithmic Techniques",
    "Introduction to Augmented Reality and Virtual Reality",
    "Advanced Artificial Intelligence",
    "Deep Learning",
    "Artificial Intelligence",
    "Machine Learning",
    "Algorithms for Big Data",
    "Natural Language Understanding",
    "Autonomous Systems",
    "Computer Network Protocols and Applications",
    "Fundamentals of Machine Learning",
    "Neural Networks",
    "Advance Computer Vision",
    "Edge and Fog Computing",
    "Parameterized Complexity",
    "Advanced Computer Graphics",
    "Bridge Course on DSA",
    "Software Testing and Quality Assurance",
    "Distributed Database Systems",
    "Medical Image Analysis",
    "Special Topics in Computer Science 1",
    "Distributed Algorithms",
    "Special Topics in Computer Science 3",
    "Independent Study",
    "Selected Topics in Artificial Intelligence - I",
    "Thesis",
    "Machine Learning with Big Data",
    "Human-Machine Interaction",
    "Digital System Lab",
    "Visual Computing Lab",
    "Data Structures and Practices",
    "ML-Ops-1",
    "DL-Ops",
    "ML-Ops"
]

structure = [
    {
        "course_ID" : "CS1001",
        "course_name" : "Introduction to Computer Science",
        "chapters" : {
            "001" : "Introduction to Computer Science",
            "002" : "Computer Science Fundamentals",
            "003" : "Computer Science Basics",
        }
    },
    {
        "course_ID" : "CS1002",
        "course_name" : "Introduction to Machine Learning",
        "chapters" : {
            "001" : "Introduction to Machine Learning",
            "002" : "Machine Learning Fundamentals",
            "003" : "Machine Learning Basics",
        }
    },
]


def save_topics_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)

def topics():
    model = ChatOpenAI(
        model_name='gpt-4-1106-preview',
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_messages(content)
    parser = JsonOutputFunctionsParser()
    chain = prompt | model | parser
    response = chain.invoke({"courses": courses, "structure": structure})
    print(response.content)
    return response.content
  

def main():
    topics_list = topics()
    jso = json.loads(topics_list)
    save_topics_to_json(topics_list, 'code/data/topics_list.json') 

if __name__ == "__main__":
    main()
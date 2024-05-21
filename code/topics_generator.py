from langchain_core.prompts import (ChatPromptTemplate)
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
import random
import json


print("Running topic generation module...")
LLM_MODEL = 'gpt-4-turbo'
TEMPERATURE = 0
SUBJECT = 'CS'
BOOK = 'Introduction to Algorithms'
AUTHOR = 'Thomas Corman'


model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant to a professor. You have access to all resources on the web."),
    ("human", """I am a {subject}  professor and I want to create lectures slides for various topics in the book : {book} by {author}.\n
Give me a list of topics from the book I provided in the form of a Python dict.\n
Also, I will use these topics to make presentations and hence augment the presentation titles if they are generic\n
For example: for titles like Introduction, Applications convert them to Introduction to Deep Learning, Applications of Deep Learning, respectively.
Do not provide any converstation.\n
Here's an example\n
     
Book Name : Understanding Deep Learning\n
Subject : CS\n
Expected Output:\n
{{
    "CS": [
        "Math for Deep Learning Basics",
        "Intro to Supervised Learning",
        "Shallow Neural Networks",
        "Activation Functions",
        "Composing Neural Networks",
        "Gradient Descent Optimization",
        "Stochastic Gradient Descent",
        "Adam Optimization Algorithm",
        "Backpropagation in Toy Model",
        "Initialization Techniques",
        "MNIST-1D Performance Analysis",
        "Bias-Variance Trade-off",
        "Double Descent Phenomenon",
        "L2 Regularization Techniques",
        "Implicit Regularization Methods",
        "Model Ensembling Techniques",
        "Bayesian Methods in ML",
        "Data Augmentation Techniques",
        "1D Convolution Basics",
        "Convolution for MNIST-1D",
        "2D Convolution Basics",
        "Downsampling & Upsampling",
        "Shattered Gradients Issue",
        "Residual Networks Introduction",
        "Batch Normalization Role",
        "Self-Attention Mechanisms",
        "Multi-Head Self-Attention",
        "Graph Encoding Techniques",
        "Graph Classification Methods",
        "Neighborhood Sampling",
        "Graph Attention Mechanisms",
        "GAN Toy Example",
        "Wasserstein Distance in GANs",
        "1D Normalizing Flows Intro",
        "Autoregressive Flows Intro",
        "Latent Variable Models Intro",
        "Reparameterization Trick",
        "Importance Sampling Methods",
        "Diffusion Encoder Basics",
        "1D Diffusion Model Basics",
        "Reparameterized Model Intro",
        "Diffusion Models Families",
        "Markov Decision Processes Intro",
        "Dynamic Programming Basics",
        "Monte Carlo Methods Intro",
        "Temporal Difference Methods",
        "Control Variates Methods",
        "Random Data Generation",
        "Full-Batch Gradient Descent",
        "Lottery Tickets Hypothesis",
        "Adversarial Attacks Techniques",
        "Bias Mitigation Strategies",
        "Explainability Techniques"
    ]
}}
""")]
)
parser = JsonOutputParser()
chain = prompt | model | parser
output = chain.invoke({"subject": SUBJECT, "book": BOOK, "author": AUTHOR})

new_output = {}

n_topics = 0
for key, topics_list in output.items():
    new_output[key] = []
    n_topics = len(topics_list)
    for item in topics_list:
        topic_obj = {
            "presentation_ID" : str(hex(random.randint(0x100000, 0xFFFFFF))[2:]),
            "topic": item,
            "book": BOOK
        }
        new_output[key].append(topic_obj)

TOPICS_PATH = 'code\\data\\topics.json'
with open(TOPICS_PATH, 'w') as json_file:
    json.dump(new_output, json_file, indent=3)
    print(f"🟢 (1/1) {n_topics} presentation topics generated based on the book {BOOK} by author {AUTHOR}\n")
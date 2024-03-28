import os
import json
from langchain_core.prompts import (
    PromptTemplate
)
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)

class SlideContentJSON(BaseModel):
    slide_number: int = Field(description="The number of the slide in the presentation")
    title: str = Field(description="Title content of the slide")
    description: str = Field(description="Body content represented as a paragraph anywhere around 5 to 30 words long")
    enumeration: list = Field(description="Body Content represented as a list of points where each point is around 2 to 5 wordws long")


class PPTContentJSON(BaseModel):
    presentation_ID : int = Field(description="Unique ID for each presentation provided in the prompt")
    slides: list[SlideContentJSON] = Field(description="A list of slide objects")



def generate_slide_content(slide_id, arg_topic, arg_level, arg_toc):
   TEMPERATURE = 0.5
   LLM_MODEL = 'gpt-4-1106-preview'
   few_shot_examples = [
       {
           "presentation_ID": 11111,
           "topic": "0/1 Knapsack Problem",
           "level": "advanced",
           "TOC": "1. Title Slide\n 2. Introduction slide\n 3. Algorithm pseudocode\n 4. Use Cases of the algorithm",
           "ppt_content":
           """
       {{
        "presentation_ID": 11237,
        "slides": [
           {{
              "slide_number": 1,
              "title": "Solving the 0/1 Knapsack Problem",
              "description": "Djikstra's Algorithm is a foundational tool in computer science for finding the shortest path between nodes in a graphExploring Dynamic Programming Approaches",
              "enumeration": []
           }},
           {{
              "slide_number": 2,
              "title": "Introduction to 0/1 Knapsack",
              "description": "Definition: A classic optimization problem in computer science and combinatorial optimization. Given a set of items, each with a weight and a value, determine the number of each item to include in a knapsack so that the total weight is less than or equal to a given limit, and the total value is maximized.",
              "enumeration": [
                  "Widely applicable in various fields such as resource allocation, finance, and logistics.",
                  "Foundation for understanding dynamic programming techniques."
              ]
           }},
           {{
              "slide_number": 3,
              "title": "0/1 Knapsack: Pseudocode",
              "description": "Dynamic Programming Algorithm for 0/1 Knapsack:",
              "enumeration": [
                  "Initialize a 2D array 'dp' of size (n+1) x (W+1)",
                  "Iterate over each item and each possible weight capacity.",
                  "At each step, determine whether including the current item would increase the total value.",
                  "Update the 'dp' table accordingly.",
                  "The final entry in 'dp[n][W]' contains the maximum achievable value."
              ]
           }},
           {{
              "slide_number": 4,
              "title": "Use Cases",
              "description": "0/1 Knapsack has a wide range of applications.",
              "enumeration": [
                 "Resource allocation in project management.",
                 "Portfolio optimization in finance.",
                 "Cargo loading in transportation logistics.",
                 "Subset selection in machine learning feature engineering."
              ]
           }}
        ]
        }}
           """
       },
       {    "presentation_ID": 11112,
            "topic": "Machine Translation",
            "level": "introductory",
            "TOC": "1. Title Slide\n 2. Introduction\n 3. Methods in MT\n 4. <Common Method in MT>",
            "ppt_content": 
            """
        {{
        "presentation_ID": 11112,
        "slides": [
           {{
              "slide_number": 1,
              "title": "Machine Translation",
              "description": "The art of translating between languages by the machines!",
              "enumeration": []
           }},
           {{
              "slide_number": 2,
              "title": "Introduction to Machine Translation",
              "description": "Machine Translation has been defined as the process that utilizes computer software to translate text from one natural language(such as English) to another (such as French).",
              "enumeration": [
                "The idea of machine translation may be traced back to the 17th century",
                "MT on the web starts with Systran offering free translation of small texts (1996)"
              ]
           }},
           {{
              "slide_number": 3,
              "title": "Techniques in Machine Translation",
              "description": "",
              "enumeration": [
                 "Example-based MT",
                 "Dictionary-based",
                 "Rule-based",
                 "Hybrid MT",
                 "Neural MT",
                 "Statistical",
                 "Interlingual",
                 "Transfer-based"
              ]
           }},
           {{
              "slide_number": 4,
              "title": "Rule-based MT",
              "description": "RBMT involves more information about the linguistics of the source and target languages ,using the syntactic rules and semantic analysis of both languages",
              "enumeration": [
                 "Direct Systems",
                 "Transfer RBMT Systems",
                 "Interlingual RBMT Systems"
              ]
           }}
        ]
     }}
     """           
       }
   ]
   
   model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
   suffix = """
       Look at the above examples and help me create the content for a presentation of the following details:
       Topic : {topic}\n
       Level : {level}\n
       Table of Contents : {TOC}\n

       The presentation ID is {presentation_ID}
       """
   prefix = f"""
        I am a university professor and I want you to help me prepare content of presentations based on a lecture topic I will provide.
        You can access to all online resources to acquire content on the provided topic\n
        I want you to provide slide-wise detailed content in a JSON format. Make sure you understand the semantic meaning of each title to generate body content for that slide. Make use of bulleted enumerations, and maintain coherence from one slide to the next. 
        \nI am sharing a few examples where "User" is my prompt and "Expected JSON Output" is the expected output.\n
   """
   template = """
       User:
       Prepare a presentation having 6 slides on {topic}, with the following table of contents:
       \n\n
       {TOC}
       \n\n
       For each slide, please ensure the following constraints while generating PPT\n
        1. Title should be between 1 to 4 words
        2. The description should be between 5 and 50 words
        3. The enumeration list should have between 1 and 5 items, with each item having 1 to 3 words.
       Consider this a {level} level course, and prepare the depth of content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n\n
       
       Expected JSON output:\n
       {ppt_content}
       """
   example_prompt = PromptTemplate(
       input_variables=["topic", "presentation_ID", "level", "TOC", "ppt_content"],
       template=template
   )

#    print(example_prompt.format(**few_shot_examples[0]))
   final_prompt = FewShotPromptTemplate(
       examples=few_shot_examples,
       prefix=prefix,
       example_prompt=example_prompt,
       suffix=suffix,
       input_variables=["topic", "presentation_ID", "level", "TOC"],
       example_separator="\n\n"
       )
   print(final_prompt.format(
       topic=arg_topic,
       presentation_ID=slide_id,
       level=arg_level,
       TOC=arg_toc
   ))
   openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
   parser = JsonOutputFunctionsParser()
   chain = ( final_prompt
             | model.bind(functions=openai_functions)
             | parser) 
   llm_output = chain.invoke({"presentation_ID": slide_id, "topic": arg_topic, "TOC": arg_toc, "level": arg_level})
#    llm_output = "<NONE>"
#    print(type(llm_output))
   return llm_output
   


def save_slide_content_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)

def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed


def main():
    SEED_PATH = "code\data\\topics.json"
    slide_seeds = fetch_seed_content(SEED_PATH)
    for slide_id, seed_items in slide_seeds.items():
        topic = seed_items["topic"]
        level = seed_items["level"]
        table_of_content = seed_items["TOC"]
        # print(topic)
        generated_content = generate_slide_content(slide_id, topic, level, table_of_content)
        if isinstance(generated_content, dict):
            file_path = f"code/buffer/{slide_id}.json"
            save_slide_content_to_json(generated_content, file_path)
            print(f"Intermediate JSON file created: {slide_id}.json")

if __name__ == "__main__":
    main()






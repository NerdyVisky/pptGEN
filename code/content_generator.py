import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)

class PPTContentJSON(BaseModel):
    presentation_ID : int = Field(description="Unique ID for each presentation provided in the prompt")
    slides: list = Field(description="A list of objects where each object has keys as slide_number, title, description, and enumeration, and the value is the respective text content for each field")



def generate_slide_content(slide_id, topic, level, toc):
   TEMPERATURE = 0.8
   LLM_MODEL = 'gpt-3.5-turbo'
   model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
   prompt = ChatPromptTemplate.from_template(
       """
       I am a university professor and I want to prepare a presentation for my students on the topic of {topic}.
       I want you to help me prepare a six-slide presentation given the following Table of Contents:
       \n\n
       {TOC}
       \n\n
       I want you to output the actual content of the presenation as a JSON object with each object having consisting of a presentation ID and a slides array where each element of the array has attributes title, descirption, and enumeration corresponding to each slide
       Given this is a {level} course, I want you to prepare the content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       """
   )
   openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
   parser = JsonOutputFunctionsParser()
   chain = ( prompt
             | model.bind(functions=openai_functions)
             | parser) 
   llm_output = chain.invoke({"presentation_ID": slide_id, "topic": topic, "TOC": toc, "level": level})
   print(type(llm_output))
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

if __name__ == "__main__":
    main()






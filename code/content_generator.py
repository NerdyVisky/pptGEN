import os
import json
from langchain_core.prompts import ChatPromptTemplate
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



def generate_slide_content(slide_id, topic, level, toc):
   TEMPERATURE = 0.5
   LLM_MODEL = 'gpt-4-1106-preview'
   model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
   prompt = ChatPromptTemplate.from_template(
       """
       I am a university professor and I want to prepare a presentation for my students on the topic of {topic}.
       I want you to help me prepare a presentation having 6 slides, with the following table of contents:
       \n\n
       {TOC}
       \n\n
       I want you to output the actual content of the presenation as a JSON object. The structure of the JSON object is provided using the OpenAI function.\n
       For each slide, please ensure the title has between 1 to 4 words, the description is between 5 and 50 words, and the enumeration list contains between 1 and 5 items, with each item having 1 to 3 words.
       Given this is a {level} level course, I want you provide the depth of content accordingly.
       Look for online resources and your knowledge base on {topic} and provide extremely detailed content for each section in the Table of Contents.\n
       Also understanding the semantic meaning of each title to generate body content for that slide. Make use of bulleted enumerations, and maintain coherence from one slide to the next.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       """
   )
   openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
   parser = JsonOutputFunctionsParser()
   chain = ( prompt
             | model.bind(functions=openai_functions)
             | parser) 
   llm_output = chain.invoke({"presentation_ID": slide_id, "topic": topic, "TOC": toc, "level": level})
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






import os
import json
import csv
import random
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function

class SlideContentJSON(BaseModel):
    slide_id: int = Field(description="The number of the slide in the presentation")
    title: str = Field(description="Title content of the slide")
    description: str = Field(description="Body content represented as a paragraph anywhere around 5 to 30 words long")
    enumeration: list = Field(description="Body Content represented as a list of points where each point is around 2 to 5 wordws long")
    image_prompt: str = Field(description="Prompt for generating image for the slide")

class PPTContentJSON(BaseModel):
    presentation_ID : int = Field(description="Unique ID for each presentation provided in the prompt")
    slides: list[SlideContentJSON] = Field(description="A list of slide objects")

def generate_slide_content(ppt_id, arg_topic):
    TEMPERATURE = 0.5
    LLM_MODEL = 'gpt-4-1106-preview'
        
    model = ChatOpenAI(
        model_name=LLM_MODEL, 
        temperature=TEMPERATURE,
        )

    prompt_content = f"""
        I am a university professor and I want you to help me prepare content of presentations based on a lecture topic I will provide.\n
        Each topic is from AI field. You can access to all online resources to acquire content on the provided topic.\n
        I want you to provide slide-wise detailed content in a JSON format. Make sure you understand the semantic meaning of each title to generate body content for that slide. Make use of bulleted enumerations, and maintain coherence from one slide to the next.\n
        Prepare a presentation having 6 slides on {arg_topic}.
        Out of 6 slides, only 1 slide should have title and an image, which will be genrated by Dall-E model.
        Ensure the following constraints:
        1. Title: 1-4 words
        2. Description: 5-50 words
        3. Enumeration: 1-5 items (1-20 words each)
        Lnly for the image slide, which can be any slide, the title and image_prompt field should be filled. The rest 5 slides should have rest fields filled, with image_prompt field empty.\n
        Consider this a graduate level course, and prepare the depth of content accordingly.
        I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {ppt_id}
        """
    
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professor's assistant for an educational course. Your role is to generate presentation slide content in JSON format based on the provided topic."),
        ("user", prompt_content.format(arg_topic=arg_topic))
    ])
    
    openai_functions = [convert_to_openai_function(PPTContentJSON)]
    parser = JsonOutputFunctionsParser()
    chain = ( final_prompt
                | model.bind(functions=openai_functions)
                | parser)   
    llm_output = chain.invoke({"prmopt": "Generate the content."})
    return llm_output
   
def save_slide_content_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)

def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed

def fetch_seed_content(csv_file_path):
    slide_seeds = {}
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            ppt_id = int(row[0])
            topic = row[1]
            slide_seeds[ppt_id] = topic
    return slide_seeds

def main():
    CSV_PATH = "code\data\\topics.csv"
    slide_seeds = fetch_seed_content(CSV_PATH)
    
    slide_seed_list = list(slide_seeds.items())
    random_selections = random.sample(slide_seed_list, 1)
    
    # for ppt_id, topic in slide_seeds.items():
    for ppt_id, topic in random_selections:
        # print(f"Topic ID: {ppt_id}, Topic: {topic}")
        generated_content = generate_slide_content(ppt_id, topic)
        if isinstance(generated_content, dict):
            file_path = f"code/buffer/{ppt_id}.json"
            save_slide_content_to_json(generated_content, file_path)
            print(f"Intermediate JSON file created: {ppt_id}.json")

if __name__ == "__main__":
    main()
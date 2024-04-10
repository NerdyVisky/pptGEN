import os
import json
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (FewShotChatMessagePromptTemplate, ChatPromptTemplate)
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from utils.data_validation import PPTContentJSON
from utils.prompts import outline_prompt, instruction_example_prompt, generation_prompt, instruction_example, instruction_prompt


def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed

def save_slide_content_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)


def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo'):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     return model

def configure_prompt(phase):
    if phase == 'outline':
        prompt = ChatPromptTemplate.from_messages(outline_prompt)
    elif phase == 'instruction':
        example_prompt = ChatPromptTemplate.from_messages(
            instruction_example_prompt
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=instruction_example,
            example_prompt=example_prompt
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', 'You are an capable and expert content creator. You can create multi-modal content such as text, images, code, etc. You also have access to all internet sources at your discretion.'),
                few_shot_prompt,
                instruction_prompt

            ]
        )
    elif phase == 'generation':
        prompt = ChatPromptTemplate.from_messages(generation_prompt)
    return prompt

def generate_slide_content(slide_id, arg_topic):
    ## Outline Phase
    model = configure_llm()
    prompt = configure_prompt("outline")
    chain = prompt | model
    output = chain.invoke({"topic": arg_topic, "format": "Nested Dictionary"})
    print(output.content)

    ## Instruction Phase
    instruct_prompt = configure_prompt("instruction")
    instruct_chain = instruct_prompt | model
    arg_elements = ['chart', 'graph', 'diagram', 'enumeration','description', 'table', 'equation', 'url']
    instruct_output = instruct_chain.invoke({"topic": arg_topic, "elements": arg_elements, "outline": output.content})
    print(instruct_output.content)

    ## Generation Phase
    gen_model = ChatOpenAI(
       model_name='gpt-4-1106-preview', 
       temperature=0,
       )
    gen_prompt = configure_prompt("generation")
    openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
    parser = JsonOutputFunctionsParser()
    gen_chain = gen_prompt | gen_model.bind(functions=openai_functions) | parser
    gen_output = gen_chain.invoke({'topic': arg_topic, 'outline': instruct_output.content, 'presentation_ID': slide_id})
    # print(gen_output)
    return gen_output
    


def main():
    load_dotenv(find_dotenv())
    SEED_PATH = "code\data\\topics.json"
    slide_seeds = fetch_seed_content(SEED_PATH)
    for slide_id, seed_items in slide_seeds.items():
        topic = seed_items["topic"]
        generated_content = generate_slide_content(slide_id, topic)
        if isinstance(generated_content, dict):
            file_path = f"code/buffer/{slide_id}.json"
            save_slide_content_to_json(generated_content, file_path)
            print(f"Intermediate JSON file created: {slide_id}.json")

if __name__ == "__main__":
    main()

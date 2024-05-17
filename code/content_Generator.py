import os
import json
import re
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (FewShotChatMessagePromptTemplate, ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from utils.data_validation import PPTContentJSON
from utils.generators_fns import generate_figure_content, generate_plot_content, generate_struct_content, generate_text_content, assemble_elements
from utils.prompts import outline_prompt, instruction_example_prompt, generation_prompt, instruction_example, instruction_prompt, construct_generation_prompts
# from test2 import text_content, instruct_content


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
                ('system', 'You are an experienced assistant. You have access to the internet and expectional teaching acumen and reasoning skills'),
                few_shot_prompt,
                instruction_prompt

            ]
        )
    elif phase == 'generation':
        prompt = ChatPromptTemplate.from_messages(generation_prompt)
    return prompt

def generate_slide_content(slide_id, arg_topic):
    ## Outline Phase
    model = configure_llm(TEMPERATURE=0, LLM_MODEL='gpt-3.5-turbo')
    prompt = configure_prompt("outline")
    chain = prompt | model
    output = chain.invoke({"topic": arg_topic})
    print(output.content)

    ## Instruction Phase
    instruct_prompt = configure_prompt("instruction")
    instruct_chain = instruct_prompt | model
    arg_elements = ['flow-chart', 'graph', 'tree', 'block-diagram', 'enumeration','description', 'url', 'table', 'equation', 'plot', 'bar-chart', 'line-chart', 'pie-chart', '3d-plot']
    instruct_output = instruct_chain.invoke({"topic": arg_topic, "elements": arg_elements, "outline": output.content})
    print(instruct_output.content)
    instruct_content = json.loads(instruct_output.content)

    # prompts, positions = construct_generation_prompts(json.loads(instruct_content), arg_topic)
    prompts, positions, captions = construct_generation_prompts(instruct_content, arg_topic)
    # Generation Phase
    gpt_4_model = configure_llm(TEMPERATURE=0, LLM_MODEL='gpt-4-turbo')
    text_content = generate_text_content(model, arg_topic, instruct_content, slide_id)
    struct_imgs = generate_struct_content(prompts[0], gpt_4_model, slide_id)
    plot_imgs = generate_plot_content(prompts[1], gpt_4_model, slide_id)
    figure_imgs = generate_figure_content(prompts[2], gpt_4_model, slide_id)
    final_content = assemble_elements(text_content, struct_imgs, plot_imgs, figure_imgs, positions, prompts, captions)
    print(final_content)

    return final_content
    


def main():
    load_dotenv(find_dotenv())
    SEED_PATH = "code\data\\topics.json"
    slide_seeds = fetch_seed_content(SEED_PATH)
    for subject, ppts in slide_seeds.items():
        for ppt in ppts: 
            topic = ppt["topic"]
            presentation_ID = ppt["presentation_ID"]
            generated_content = generate_slide_content(presentation_ID, topic)
            if isinstance(generated_content, dict):
                dir_path = f"code/temp/{subject}"
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                file_path = f"code/temp/{subject}/{presentation_ID}.json"
                save_slide_content_to_json(generated_content, file_path)
                print(f"Content Generated: {subject}/{presentation_ID}.json")

if __name__ == "__main__":
    main()
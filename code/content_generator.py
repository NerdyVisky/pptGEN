import os
import json
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (FewShotChatMessagePromptTemplate, ChatPromptTemplate)
from langchain_openai import ChatOpenAI
from utils.generators_fns import generate_outline, generate_instructions, generate_figure_content, generate_plot_content, generate_struct_content, generate_text_content, assemble_elements
from utils.prompts import outline_prompt, instruction_example_prompt, instruction_example, instruction_prompt, construct_generation_prompts
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
    return prompt


def generate_slide_content(slide_id, arg_topic, subject, book):
    ## Outline Phase
    model = configure_llm(TEMPERATURE=0, LLM_MODEL='gpt-3.5-turbo')
    gpt4_model = configure_llm(TEMPERATURE=0, LLM_MODEL='gpt-4-turbo')
    outline_prompt = configure_prompt("outline")
    outline = generate_outline(outline_prompt, gpt4_model, arg_topic, book)
    print(f"\t🟢 (1/8) Prepared outline for {slide_id}")

    ## Instruction Phase
    instruct_prompt = configure_prompt("instruction")
    arg_elements = ['flow-chart', 'graph', 'tree', 'block-diagram', 'enumeration','description', 'url', 'table', 'equation', 'plot', 'bar-chart', 'line-chart', 'pie-chart', '3d-plot']
    instruct_content = generate_instructions(instruct_prompt, model, arg_topic, arg_elements, outline)
    print(f"\t🟢 (2/8) Devised instructions for {slide_id}")

    prompts, positions, captions, num_of_vis = construct_generation_prompts(instruct_content, arg_topic)
    # num_of_vis -> [n_s, n_p, n_f]

    # Generation Phase
    text_content = generate_text_content(gpt4_model, arg_topic, instruct_content, slide_id, subject)
    print(f"\t🟢 (3/8) Generated text content for {slide_id}")

    struct_imgs = []
    plot_imgs = []
    figure_imgs = []
    if(num_of_vis[0] != 0):
        struct_imgs = generate_struct_content(prompts[0], gpt4_model, slide_id)
        print(f"\t🟢 (4/8) Generated structs for {slide_id}")
    else:
        print(f"\t🟢 (4/8) No struct content for {slide_id}")



    if(num_of_vis[1] != 0):
        plot_imgs = generate_plot_content(prompts[1], gpt4_model, slide_id)
        print(f"\t🟢 (5/8) Generated plots for {slide_id}")
    else:
        print(f"\t🟢 (5/8) No plot content for {slide_id}")

    if(num_of_vis[2] != 0):
        figure_imgs = generate_figure_content(prompts[2], gpt4_model, slide_id)
        print(f"\t🟢 (6/8) Generated figures for {slide_id}")
    else:
        print(f"\t🟢 (6/8) No figure content for {slide_id}")

    final_content = assemble_elements(text_content, struct_imgs, plot_imgs, figure_imgs, positions, prompts, captions)
    print(f"\t🟢 (7/8) Assembled content for {slide_id}")

    return final_content
    

def main():
    print("Running content generation module...")
    load_dotenv(find_dotenv())
    SEED_PATH = "code\data\\topics.json"
    slide_seeds = fetch_seed_content(SEED_PATH)
    for subject, ppts in slide_seeds.items():
        n_ppts = len(ppts)
        for i, ppt in enumerate(ppts): 
            topic = ppt["topic"]
            presentation_ID = ppt["presentation_ID"]
            book = ppt["book"]
            print(f"({i+1}/{n_ppts}): generating content for {presentation_ID}")
            try:
                generated_content = generate_slide_content(presentation_ID, topic, subject, book)
                if isinstance(generated_content, dict):
                    dir_path = f"code/temp/{subject}"
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    file_path = f"code/temp/{subject}/{presentation_ID}.json"
                    save_slide_content_to_json(generated_content, file_path)
                    print(f"\t🟢 (8/8) Content saved for {presentation_ID}")
            except:
                print(f"\t 🟠 Error in generating content for {presentation_ID}. Skipping topic.")
    print('\n')
    

if __name__ == "__main__":
    main()

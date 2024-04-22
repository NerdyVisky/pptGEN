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
from utils.prompts import outline_prompt, instruction_example_prompt, generation_prompt, instruction_example, instruction_prompt
# from test2 import instruct_content, output


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

def construct_generation_prompts(instruct_content, topic):
    prompts = [f"I am providing some instructions which are related to generating text-based content for a presentation on {topic} with presentation ID: {{presentation_ID}}.\n"
               , f"I am providing some instructions which are related to generating structural content for a presentation like tables and equations on {topic}.\n"
               , f"I am providing some instructions which are related to generating plots for a presentation on {topic}.\n"
               , f"I am providing some instructions which are related to generating diagrams and figures for a presentation on {topic}.\n"]
    # prompts -> ['text', 'structural (LaTeX)', 'plots (Matplotlib)', 'figures (DOT + GraphViz)']
    positions = [{"description": [],
                  "enumeration": [],
                  "url": []
                 },
                 {
                  "table": [],
                  "equation": []   
                 },
                 {
                  "plot": [],
                  "bar-chart": [],
                  "line-chart": [],
                  "pie-chart": [],
                  "3d-plot": []
                 },
                 {
                    "tree": [],
                    "graph": [],
                    "flow-chart": [],
                    "block-diagram": [] 
                 }]


    i = 0
    for slide, elements in instruct_content.items():
        for element in elements:
            context_line = f"For the section title '{slide}'(Slide Number {i+1})"
            element_type = element["element_type"]
            element_caption = element["element_caption"]

            if element_type in ["description", "enumeration", "url"]:
                positions[0][element_type].append(i+1)
                prompts[0] += (context_line + f" generate the actual text content of a {element_type} element given the element caption: {element_caption}\n")
            elif element_type in ["table", "equation"]:
                positions[1][element_type].append(i+1)
                prompts[1] += (context_line + f" generate LaTeX code for a simple {element_type} given the caption: {element_caption}\n")
            elif element_type in ["plot", "bar-chart", "line-chart", "pie-chart", "3d-plot"]:
                positions[2][element_type].append(i+1)
                prompts[2] += (context_line + f" generate Matplotlib code for a simple {element_type} given the caption: {element_caption}\n")
            elif element_type in ["tree", "graph", "flow-chart", "block-diagram"]:
                positions[3][element_type].append(i+1)
                prompts[3] += (context_line + f" generate DOT language code for a simple {element_type} given the caption: {element_caption}\n")
        i+=1
                
    prompts[0] += """Generate text content as a Python List of objects. The length of the list will be total number of slides. Here are the slide-wise titles:\n
{titles}\n
Each object will have slide_number, title, description, enumeration, and url as keys.
For title, description, and url content the value is a string while for an enumeration content the value is a python list of strings where each element of that list is a string. Also note that the first element in the enumeration is the heading of the enumeration.\n
    """
    prompts[1] += "Generate LaTeX code as plain text seperated by ```latex<content>``` and three line breaks. Do not add a caption to the table/equation and do not provide any conversation.\n"
    prompts[2] += "Generate python code using Matplotlib as plain text seperated by ```python<content>``` and three line breaks. Each generated plot shoule be saved to 'code/buffer/figures/<id>.png' where <id> is a numerical sequence of the plot. Do not generate a title for the plot and do not give any conversation.\n"
    prompts[3] += "Generate DOT language code as plain text seperated by ```dot<content>``` and three line breaks. Do not add a caption to the diagram/chart, etc. and do not provide any conversation.\n"
    # Return the constructed prompts
    return [prompts, positions]

def generate_slide_content(slide_id, arg_topic):
    ## Outline Phase
    model = configure_llm()
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
    prompts, positions = construct_generation_prompts(instruct_content, arg_topic)
    # Generation Phase
    gpt_4_model = ChatOpenAI(
       model_name='gpt-4-turbo-2024-04-09', 
       temperature=0,
       )
    # gen_model = ChatOpenAI(
    #    model_name='gpt-3.5-turbo', 
    #    temperature=0,
    #    )
    # text_content = generate_text_content(prompts[0], model, output, slide_id)
    text_content = generate_text_content(prompts[0], model, list(output.content), slide_id)
    struct_imgs = generate_struct_content(prompts[1], model, slide_id)
    plot_imgs = generate_plot_content(prompts[2], model, slide_id)
    figure_imgs = generate_figure_content(prompts[3], model, slide_id)
   
    final_content = assemble_elements(text_content, struct_imgs, plot_imgs, figure_imgs, positions, prompts)
    print(final_content)

    # # for ele in text_content:
    #     print(ele)
    #     print("\n")

    # print(struct_imgs[0])
    # print("\n")
    # print(plot_imgs[0])
    # print("\n")
    # print(figure_imgs[0])

    # openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
    # parser = JsonOutputFunctionsParser()
    # gen_chain = gen_prompt | gen_model.bind(functions=openai_functions) | parser
    # gen_output = gen_chain.invoke({'topic': arg_topic, 'outline': instruct_output.content, 'presentation_ID': slide_id})
    # # print(gen_output)
    return final_content
    


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

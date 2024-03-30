import os
import json
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (PromptTemplate)
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_functions_agent
from langchain import hub
from langchain.agents import AgentExecutor
from prompt_store import few_shot_examples, suffix, prefix, template




class SlideContentJSON(BaseModel):
    slide_number: int = Field(description="The number of the slide in the presentation")
    title: str = Field(description="Title content of the slide")
    description: str = Field(description="Body content represented as a paragraph anywhere around 5 to 30 words long")
    enumeration: list = Field(description="Body Content represented as a list of points where each point is around 2 to 5 wordws long")


class PPTContentJSON(BaseModel):
    presentation_ID : int = Field(description="Unique ID for each presentation provided in the prompt")
    slides: list[SlideContentJSON] = Field(description="A list of slide objects")


def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo'):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     return model
     
     
def configure_few_shots_prompt():
    example_prompt = PromptTemplate(
       input_variables=["topic", "presentation_ID", "level", "TOC", "ppt_content"],
       template=template
       )
    final_prompt = FewShotPromptTemplate(
       examples=few_shot_examples,
       prefix=prefix,
       example_prompt=example_prompt,
       suffix=suffix,
       input_variables=["topic", "presentation_ID", "level", "TOC"],
       example_separator="\n\n"
       )
    return final_prompt

def construct_chain(final_prompt, model):
    openai_functions = [convert_pydantic_to_openai_function(PPTContentJSON)]
    parser = JsonOutputFunctionsParser()
    chain = ( final_prompt
             | model.bind(functions=openai_functions)
             | parser)
    return chain
     

def generate_slide_content(slide_id, arg_topic, arg_level, arg_toc):
   model = configure_llm()
   final_prompt = configure_few_shots_prompt()
   chain = construct_chain(final_prompt, model)
   llm_output = chain.invoke({"presentation_ID": slide_id, "topic": arg_topic, "TOC": arg_toc, "level": arg_level})
   return llm_output
   


def save_slide_content_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)

def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed


def main():
    load_dotenv(find_dotenv())
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






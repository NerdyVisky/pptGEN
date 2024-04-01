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
from langchain.agents import AgentExecutor
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from prompt_store import prefix, suffix, few_shot_examples, few_shot_template, sample_context




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
     
     
def configure_prompt():
    example_prompt = PromptTemplate(
       input_variables=["topic", "presentation_ID", "context", "ppt_content"],
       template=few_shot_template
       )
    final_prompt = FewShotPromptTemplate(
       examples=few_shot_examples,
       prefix=prefix,
       example_prompt=example_prompt,
       suffix=suffix,
       input_variables=["topic", "presentation_ID", "context"],
       example_separator="\n\n"
       )
    # prompt = PromptTemplate(
    #    input_variables=["topic", "presentation_ID"],
    #    template=template
    #    )
    return final_prompt

def construct_retrieval_chain(prompt, model, retriever):
    parser = JsonOutputFunctionsParser()
    # chain = ( final_prompt
    #          | model.bind(functions=openai_functions)
    #          | parser)
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    return retrieval_chain

def construct_retriever(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
        ).split_documents(docs)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    return vector.as_retriever()



def initalize_tools(tools_list, retriever=None):
    tools = []
    for name in tools_list:
        match name:
            case 'search':
                search = TavilySearchResults()
                tools.append(search)
            case 'retrieve':
                if retriever != None:
                    retriever_tool = create_retriever_tool(
                        retriever,
                        "python_pptx_retriever",
                        "Search for information about python-pptx library. For any questions about python-pptx, you must use this tool!",
                        )
                    tools.append(retriever_tool)
                else:
                    raise Exception("Retriever not configured.")
            case _:
                raise Exception("specified tool not available")
    return tools

def configure_agent(llm, tools, prompt):
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
     
def construct_query(vars):
    query = {}
    query["input"] = """
    Create extremely detailed lecture-style presentation content on the topic: {topic}
    The presenation ID (not related to the content creation) is {presentation_ID}\n
    """.format(topic=vars["topic"], presentation_ID=vars["presentation_ID"])
    print(query)
    return query


def generate_slide_content(slide_id, arg_topic):
    model = configure_llm()
    prompt = configure_prompt()
#     print(prompt.format(
#        topic=arg_topic,
#        presentation_ID=slide_id,
#        context=sample_context
#    ))
    retriever = construct_retriever("https://brilliant.org/wiki/k-nearest-neighbors/")
    chain = construct_retrieval_chain(prompt, model, retriever)
    # tools_list = ['search', 'retrieve']
    # tools = initalize_tools(tools_list, retriever)
    # agent_executor = configure_agent(model, tools, final_prompt)
    # agent_output = agent_executor.invoke({"topic": arg_topic, "presentation_ID": slide_id, "level": arg_level, "TOC": arg_toc})
    query = construct_query({"presentation_ID": slide_id, "topic": arg_topic})
    llm_output = chain.invoke({"input": query["input"], "presentation_ID": slide_id, "topic": arg_topic})
    # print(type(json.loads(llm_output["answer"])))
    # llm_output = ""
    return json.loads(llm_output["answer"])

   


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
        # print(topic)
        generated_content = generate_slide_content(slide_id, topic)
        if isinstance(generated_content, dict):
            file_path = f"code/buffer/{slide_id}.json"
            save_slide_content_to_json(generated_content, file_path)
            print(f"Intermediate JSON file created: {slide_id}.json")

if __name__ == "__main__":
    main()






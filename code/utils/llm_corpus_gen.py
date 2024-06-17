# Generate 1000 random code samples
# Generate 1000 random URL links
import os
import re
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (ChatPromptTemplate)

TOPICS = {
"Depth First Search": "C++",
"Djisktra's Algorithm": "Java",
"Post Order Traversal": "Python"
}

def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo'):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     return model

def generate_code_snippets(ID=111111):
     model = configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-4-turbo')
     prompt = ChatPromptTemplate.from_messages([
          ("system", "You are a helpful code assistant. You have access to internet resources"),
          ("human", """I am a professor of Computer Science, I want to generate code for certain topics in CS. I am providing you a Python Dict where the keys are topics \
           I want to generate code for and the value is the programming language I want my code in. The dict is as follows:\n
           {topics}
           Generate code as plain text seperated by ```code<content>``` and three line breaks. \
           Here do not change the word code inside the side-ticks as it will be used to get individual code segments.\
           Make sure to not make any syntax errors,\
           and hence double check each output code snippet.\n
           
           Keep the following in mind:\n
           1. Do not generate additional elements unless they are part of the above request. 
           2. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests.
           3. Do not provide any input and output examples in the code or any library imports. Just the basic code function. 
           4. Do not provide more than 30 lines of code in any case.
           """)
     ])
     chain = prompt | model
     gen_code = chain.invoke({"topics": TOPICS}).content
     code_dump = f"code\\buffer\\corpus\\{ID}.txt"

     with open(code_dump, 'w') as file:
        file.write(gen_code)

     with open(code_dump, 'r') as file:
        content = file.read()
        pattern = r'```code(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        code_dir = 'code\\buffer\corpus\code_snips'
        code_snip_paths = []
        for i, match in enumerate(matches):
            code_snippet = match.strip() # Remove leading/trailing whitespace
            # print(code_snippet)
            os.makedirs(os.path.join(code_dir, ), exist_ok=True)
            code_snip_name = f'{hex(random.randint(0x100000, 0xFFFFFF))[2:]}.txt'
            code_file_path = os.path.join(code_dir, code_snip_name)
            with open(code_file_path, 'w') as file:
                file.write(code_snippet)
            code_snip_paths.append(code_file_path)
     return code_snip_paths


# code_snip_paths = generate_code_snippets()
def store_all_file_paths():
    root_dirs = ['code\\buffer\corpus\charts', 'code\\buffer\corpus\diagrams', 'code\\buffer\corpus\equations', 'code\\buffer\corpus\\tables', 'code\\buffer\corpus\code_snips']
    for dir_path in root_dirs:
        files = [f'{dir_path}/{f}' for f in os.listdir(dir_path)]
        base_name = os.path.basename(dir_path)
        match base_name:
            case 'charts':
                CHARTS = files
            case 'diagrams':
                DIAGRAMS = files
            case 'tables':
                TABLES = files
            case 'equations':
                EQUATIONS = files
            case 'code_snips':
                CODE_SNIPS = files
    with open('code\\utils\\corpus_paths.py', 'w') as file:
        file.writelines(f'CHARTS = {CHARTS}\n\n')
        file.writelines(f'DIAGRAMS = {DIAGRAMS}\n\n')
        file.writelines(f'TABLES = {TABLES}\n\n')
        file.writelines(f'EQUATIONS = {EQUATIONS}\n\n')
        file.writelines(f'CODE_SNIPS = {CODE_SNIPS}\n\n')
    return True


if(store_all_file_paths()):
    print("File paths stored")
else:
    raise Exception("ERR")




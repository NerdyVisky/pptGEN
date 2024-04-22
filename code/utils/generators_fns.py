import re
import subprocess
import os
import fitz
import graphviz
import ast
import json
from langchain_core.prompts import (FewShotChatMessagePromptTemplate, ChatPromptTemplate)
from utils.prompts import text_generation_example, text_generation_ex_prompt
from utils.data_validation import PPTContentJSON
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
# from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from langchain_core.utils.function_calling import convert_to_openai_function


def generate_content(prompt, model):
    gen_output = model.invoke(prompt)
    return gen_output

def generate_text_content(main_prompt, model, titles, presentation_ID):
    example_prompt = ChatPromptTemplate.from_messages(
            text_generation_ex_prompt
        )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=text_generation_example,
        example_prompt=example_prompt
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', 'You are an capable and expert content creator. You are supposed to help a professor prepare content for a presentation.'),
            few_shot_prompt,
            main_prompt

        ]
    )
    # print(prompt.format({"titles": titles, "presentation_ID": presentation_ID}))
    fn = convert_to_openai_function(PPTContentJSON)
    # print(fn)
    openai_functions = [fn]
    parser = JsonOutputFunctionsParser()
    chain = prompt | model.bind(functions=openai_functions) | parser
    text_output = chain.invoke({"titles": titles, "presentation_ID": presentation_ID})
    print(text_output)
    return text_output
    # return 0
    # text_output_list = ast.literal_eval(text_output)
    # urls = []
    # descriptions = []
    # enumerations = []
    # for element in text_output_list:
    #     if isinstance(element, str):
    #         if '.com' in element:
    #             urls.append(element)
    #         else:
    #             descriptions.append(element)
    #     elif isinstance(element, list):
    #         enumerations.append(element)
    # return [urls, descriptions, enumerations]
def get_full_element_name(im_par):
    match im_par:
        case "tb":
           element_name = "tables"
        case "eq":
           element_name = "equations"
        case "bc":
           element_name = "bar-chart"
        case "lc":
           element_name = "line-charts"
        case "pc":
           element_name = "pie-chart"
        case "3p":
           element_name = "3d-plot"
        case "pt":
           element_name = "plot"
        case "tr":
           element_name = "tree"
        case "gr":
           element_name = "graph"
        case "fc":
           element_name = "flow-chart"
        case "bd":
           element_name = "block-diagram"
    return element_name

def get_element_type(prompt_line):
    if "table" in prompt_line:
        element_type = "tb"
    elif "equation" in prompt_line:
        element_type = "eq"
    elif "bar-chart" in prompt_line:
        element_type = "bc"
    elif "line-chart" in prompt_line:
        element_type = "lc"
    elif "pie-chart" in prompt_line:
        element_type = "pc"
    elif "3d-plot" in prompt_line:
        element_type = "3p"
    elif "plot" in prompt_line:
        element_type = "pt"
    elif "tree" in prompt_line:
        element_type = "tr"
    elif "graph" in prompt_line:
        element_type = "gr"
    elif "flow-chart" in prompt_line:
        element_type = "fc"
    elif "block-diagram" in prompt_line:
        element_type = "bd"
    else:
        element_type = "uk"
    
    return element_type
    

def generate_struct_content(prompt, model, presentation_ID):

    struct_output = generate_content(prompt, model).content
    with open(f"code/buffer/{presentation_ID}_tex.txt", 'w') as tex_dump:
        tex_dump.write(struct_output)

    with open(f'code/buffer/{presentation_ID}_tex.txt', 'r') as file:
        content = file.read()

    pattern = r'```latex(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    struct_img_paths = []
    for i, match in enumerate(matches):
        tex_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        struct_type = get_element_type(prompt_line)
        print(struct_type)
        img_path = get_struct_img_path(tex_code, i, presentation_ID, struct_type)
        struct_img_paths.append(img_path)

    return struct_img_paths

def generate_figure_content(prompt, model, presentation_ID):
    gen_figure = generate_content(prompt, model).content
    with open(f"code/buffer/{presentation_ID}_dot.txt", 'w') as dot_dump:
        dot_dump.write(gen_figure)

    with open(f'code/buffer/{presentation_ID}_dot.txt', 'r') as file:
        content = file.read()

    pattern = r'```dot(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    fig_dir = 'code/buffer/figures'
    fig_img_paths = []
    for i, match in enumerate(matches):
        dot_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        fig_type = get_element_type(prompt_line)
        print(fig_type)
        graph = graphviz.Source(dot_code)
        graph.render(filename=os.path.join(fig_dir, fig_type, f'{i+1}_{presentation_ID}'), format='png', cleanup=True)
        img_path = os.path.join(fig_dir, fig_type, f'{i+1}_{presentation_ID}') + '.png'
        fig_img_paths.append(img_path)
    
    return fig_img_paths

def generate_plot_content(prompt, model, presentation_ID):
    gen_plot = generate_content(prompt, model).content
    with open(f"code/buffer/{presentation_ID}_py.txt", 'w') as py_dump:
        py_dump.write(gen_plot)

    with open(f'code/buffer/{presentation_ID}_py.txt', 'r') as file:
        content = file.read()

    pattern = r'```python(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    plot_img_paths = []
    for i, match in enumerate(matches):
        py_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        plt_type = get_element_type(prompt_line)
        print(plt_type)
        script_path = "code\plot_test.py"
        with open(script_path, "w") as py_plot_file:
            py_plot_file.write(py_code)
        try:
            subprocess.run(["python", script_path], check=True, capture_output=True, text=True) 
        except subprocess.CalledProcessError as e:
            print(f"Script execution failed with error code {e.returncode}")
        all_files =  os.listdir('code/buffer/figures')
        plot_paths = [file for file in all_files if file.endswith('.png')]
        for plt_path in plot_paths:
            plt_path = os.path.join('code/buffer/figures', plt_path)
            id_ = os.path.basename(plt_path).replace('.png', '')
            plt_dir = f"code/buffer/plots/{plt_type}"
            if not os.path.exists(plt_dir):
                os.mkdir(plt_dir)
            new_file_path = os.path.join(plt_dir, f"{id_}_{presentation_ID}.png")  
            os.rename(plt_path, new_file_path)
            plot_img_paths.append(new_file_path)
    
    return plot_img_paths


def assemble_elements(text_json, struct_imgs, plot_imgs, figure_imgs, positions, prompts):
    # text_json = json.loads(text_content)
    vis_eles = [struct_imgs, plot_imgs, figure_imgs]
    for slide in text_json["slides"]:
        slide["equations"] = []
        slide["tables"] = []
        slide["figures"] = []
    positions = positions[1:]
    for ind, imgs in enumerate(vis_eles):
        prompt_lines = prompts[ind + 1].split('\n')
        for i, img_path in enumerate(imgs):
            dir_name = os.path.dirname(img_path)
            im_par = os.path.basename(dir_name)
            print(im_par)
            element_name = get_full_element_name(im_par)
            file_name = os.path.basename(img_path)
            parts = file_name.split('_')
            slide_number = int(parts[0])
            presentation_id = int(parts[1].replace('.png', ''))
            caption = prompt_lines[i+1].split(':')[1].strip()
            obj = {
                'desc': caption,
                'path': img_path
            }
            if ind == 0:
                text_json["slides"][slide_number - 1][element_name].append(obj)
            else:
                obj['label'] = element_name
                text_json["slides"][slide_number - 1]["figures"].append(obj)
    
    return text_json


def get_struct_img_path(tex_code, num, presentation_ID, struct_type):
    img_dir = f'code/buffer/structs/{struct_type}/'
    img_name = f'{num + 1}_{presentation_ID}.png'
    dpi = 600
    tex_file = f'tmp.tex'
    with open(tex_file, 'w') as latexfile:
        latexfile.write('\\documentclass[preview]{standalone}\n')
        latexfile.write('\\usepackage{tikz}\n')
        latexfile.write('\\usepackage{graphicx}\n')
        latexfile.write('\\begin{document}\n')
        latexfile.write('%s\n' % tex_code)
        latexfile.write('\\end{document}\n')
    subprocess.call(['pdflatex', '-interaction=nonstopmode', tex_file], creationflags=subprocess.CREATE_NO_WINDOW)
    doc = fitz.open(f'tmp.pdf')
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    pix.save(img_name)
    img_path = os.path.join(img_dir, img_name)
    os.rename(img_name, img_path)
    return img_path



import re
import subprocess
import os
import fitz
import graphviz
import json
from langsmith import traceable
from langchain_core.prompts import (FewShotChatMessagePromptTemplate, ChatPromptTemplate)
from utils.prompts import text_generation_example, text_generation_ex_prompt
from utils.data_validation import PPTContentJSON
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function



def get_full_element_name(im_par):
    match im_par:
        case "tb":
           element_name = "table"
        case "eq":
           element_name = "equation"
        case "bc":
           element_name = "bar-chart"
        case "lc":
           element_name = "line-chart"
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
    elements = ['table', 'equation', 'bar-chart', 'line-chart', 'pie-chart', '3d-plot', 'plot', 'tree', 'graph', 'flow-chart', 'block-diagram']
    for element in elements:
        if element in prompt_line:
            if element == 'table' or element == 'equation':
                element += 's'
            element_type = element
            break
    
    return element_type


@traceable(name='Text Content')
def generate_text_content(model, topic, instruction_content, presentation_ID, subject):
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
            ('human', """I am providing you with some instructions given to generate content for a presentation on {topic} on the subject {subject}\n
The instructions have Slide Title as key and the value is a list of object describing what text/visual elements are required to explain that concept\n
I want you to focus on generating the actual content for only the text elements, i.e. description, enumeration, and url.\n
Following are the instructions:\n
{instructions}\n
While generating content keep the following in mind:\n
1. Description should be between 15 to 30 words long and be rendered as a string.\n
2. Enumeration should have short pithy points related to the slide content. It should be rendered as a list of strings where the first element of the list is the heading of the enumeration.\n
3. URL should be a weblink to a related resource in the web and it should be rendered as a string\n
""" )

        ]
    )
    # print(prompt.format({"titles": titles, "presentation_ID": presentation_ID}))
    fn = convert_to_openai_function(PPTContentJSON)
    # print(fn)
    openai_functions = [fn]
    parser = JsonOutputFunctionsParser()
    chain = prompt | model.bind(functions=openai_functions) | parser
    text_output = chain.invoke({"instructions": instruction_content , "presentation_ID": presentation_ID, "topic": topic, "subject": subject})
    return text_output
   
@traceable(name='Struct Content')
def generate_struct_content(prompt, model, presentation_ID):
    struct_output = model.invoke(prompt).content
    # struct_output = generate_content(prompt, model).content
    tex_code_dump = f"code/buffer/{presentation_ID}_tex.txt"
    with open(tex_code_dump, 'w') as tex_dump:
        tex_dump.write(struct_output)

    with open(tex_code_dump, 'r') as file:
        content = file.read()

    pattern = r'```latex(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    struct_img_paths = []
    for i, match in enumerate(matches):
        tex_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        struct_type = get_element_type(prompt_line)
        # print(struct_type)
        try:
            img_path = get_struct_img_path(tex_code, i, presentation_ID, struct_type)
            struct_img_paths.append(img_path)
        except Exception as e:
            print(f"\t 🟠 Error rendering struct: {e}. Continuing generation for other images.")
            continue
    
    dir_path = 'code/buffer/vis_dump'
    if not os.path.exists(os.path.join(dir_path, presentation_ID)):
        os.mkdir(os.path.join(dir_path, presentation_ID))
        
    os.rename(tex_code_dump, os.path.join(dir_path, presentation_ID, 'struct_code.txt'))
    return struct_img_paths


@traceable(name='Figure Content')
def generate_figure_content(prompt, model, presentation_ID):
    gen_figure = model.invoke(prompt).content
    # gen_figure = generate_content(prompt, model).content
    dot_code_dump = f"code/buffer/{presentation_ID}_dot.txt"
    with open(dot_code_dump, 'w') as dot_dump:
        dot_dump.write(gen_figure)

    with open(dot_code_dump, 'r') as file:
        content = file.read()

    pattern = r'```dot(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    fig_dir = 'code/buffer/figures'
    fig_img_paths = []
    for i, match in enumerate(matches):
        dot_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        fig_type = get_element_type(prompt_line)
        if not os.path.exists(os.path.join(fig_dir, fig_type)):
            os.mkdir(os.path.join(fig_dir, fig_type))
        # print(fig_type)
        try:
            graph = graphviz.Source(dot_code)
            graph.render(filename=os.path.join(fig_dir, fig_type, presentation_ID, f'{i+1}'), format='png', cleanup=True)
            img_path = os.path.join(fig_dir, fig_type, presentation_ID, f'{i+1}') + '.png'
            fig_img_paths.append(img_path)
        except Exception as e:
            print(f"\t 🟠 Error rendering figure: {e}. Continuing generation for other images.")
            continue
    dir_path = 'code/buffer/vis_dump'
    os.rename(dot_code_dump, os.path.join(dir_path, presentation_ID, 'figure_code.txt'))
    return fig_img_paths


@traceable(name='Outline')
def generate_outline(prompt, model, arg_topic, book):
    chain = prompt | model
    output = chain.invoke({"topic": arg_topic, "book": book})
    return output.content

@traceable(name='Instructions')
def generate_instructions(prompt, model, arg_topic, arg_elements, outline):
    chain = prompt | model
    output = chain.invoke({"topic": arg_topic, "elements": arg_elements, "outline": outline})
    # print(output.content)
    return json.loads(output.content)

@traceable(name='Plot Content')
def generate_plot_content(prompt, model, presentation_ID):
    gen_plot = model.invoke(prompt).content
    # gen_plot = generate_content(prompt, model).content
    py_code_dump = f"code/buffer/{presentation_ID}_py.txt"
    with open(py_code_dump, 'w') as py_dump:
        py_dump.write(gen_plot)

    with open(py_code_dump, 'r') as file:
        content = file.read()

    pattern = r'```python(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    plot_img_paths = []
    for i, match in enumerate(matches):
        py_code = match.strip() # Remove leading/trailing whitespace
        prompt_line = prompt.split('\n')[i+1]
        plt_type = get_element_type(prompt_line)
        # print(plt_type)
        script_path = "code\plot_test.py"
        with open(script_path, "w") as py_plot_file:
            py_plot_file.write(py_code)
        try:
            subprocess.run(["python", script_path], check=True, capture_output=True, text=True) 
        except subprocess.CalledProcessError as e:
            print(f"\t 🟠 Error generating plot: {e.returncode}. Continuing generation for other elements.")
            continue

        all_files =  os.listdir('code/buffer/figures')
        plot_paths = [file for file in all_files if file.endswith('.png')]
        for plt_path in plot_paths:
            # print(plt_path)
            plt_path = os.path.join('code/buffer/figures', plt_path)
            id_ = os.path.basename(plt_path).replace('.png', '')
            plt_dir = f"code/buffer/plots/{plt_type}"
            if not os.path.exists(plt_dir):
                os.mkdir(plt_dir)
            if not os.path.exists(os.path.join(plt_dir, presentation_ID)):
                os.mkdir(os.path.join(plt_dir, presentation_ID))
            new_file_path = os.path.join(plt_dir, presentation_ID, f"{id_}.png")  
            os.rename(plt_path, new_file_path)
            plot_img_paths.append(new_file_path)
    
    dir_path = 'code/buffer/vis_dump'
    os.rename(py_code_dump, os.path.join(dir_path, presentation_ID, 'plots_code.txt'))
    return plot_img_paths


def assemble_elements(text_json, struct_imgs, plot_imgs, figure_imgs, positions, prompts, captions):
    # text_json = json.loads(text_json)
    vis_eles = [struct_imgs, plot_imgs, figure_imgs]
    for slide in text_json["slides"]:
        slide["equations"] = []
        slide["tables"] = []
        slide["figures"] = []
    for ind, imgs in enumerate(vis_eles):
        # prompt_lines = prompts[ind].split('\n')
        for i, img_path in enumerate(imgs):
            dir_name = os.path.dirname(img_path)
            second_parent_dir = os.path.dirname(dir_name)
            element_name = os.path.basename(second_parent_dir)
            # element_name = get_full_element_name(im_par)
            file_name = os.path.basename(img_path)
            name = file_name.split('.')[0]
            if int(name) in positions[ind][element_name].keys():
                slide_number = positions[ind][element_name][int(name)]
                caption = captions[ind][element_name][int(name)]
                
            # presentation_id = int(parts[1].replace('.png', ''))
            # caption = prompt_lines[i+1].split(':')[1].strip()
            obj = {
                'desc': caption,
                'path': img_path
            }
            if ind == 0:
                if element_name == 'table':
                    element_name = 'tables'
                if element_name == 'equation':
                    element_name = 'equations'
                text_json["slides"][slide_number - 1][element_name].append(obj)
            else:
                obj['label'] = element_name
                text_json["slides"][slide_number - 1]["figures"].append(obj)
    
    return text_json


def get_struct_img_path(tex_code, num, presentation_ID, struct_type):
    img_dir = f'code/buffer/structs/{struct_type}'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    if not os.path.exists(os.path.join(img_dir, presentation_ID)):
        os.mkdir(os.path.join(img_dir, presentation_ID))
    img_name = f'{num + 1}.png'
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
    img_path = os.path.join(img_dir, presentation_ID, img_name)
    os.rename(img_name, img_path)
    return img_path



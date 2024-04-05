import os
import random
import json
from layouts import CustomLayouts
from random_generator import (generate_random_style_obj, 
                              generate_random_font, 
                              generate_random_value, 
                              pick_random, 
                              generate_random_layout, 
                              generate_n_numbers_with_sum, 
                              generate_contrasting_font_color,
                              generate_random_date,
                              pick_random_presenter)
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO 


def generate_dicts(csv_file_path):
    df = pd.read_csv(csv_file_path)
    dict = {}
    for i in range(len(df)):
        topic = df.loc[i,'Topic']
        value = df.loc[i,'Value']
        
        if topic not in dict.keys():
            dict[topic] = [value]
        else:
            dict[topic].extend([value])
    return dict


TOPICS = ['NLP', 'AI', 'Deep Learning', 'Computer Vision']
TITLES_DICT = generate_dicts("code\data\\titles.csv")
DESC_DICT = generate_dicts("code\data\\descriptions.csv")
ENUM_DICT = generate_dicts("code\data\\enumerations.csv")
PATH_DICT = generate_dicts("code\data\\figures.csv")

# print(TITLES_DICT['NLP'])

def count_body_elements(data, slide_number):
    ttl_desc = 0
    ttl_enum = 0
    ttl_eq = 0
    for k, v in data["slides"][slide_number - 1].items():
        if k == 'description' and v != "":
            ttl_desc = 1
        elif k == 'enumeration':
            ttl_enum = 1
        elif k == 'equations':
            ttl_eq = len(v)
    # print(ttl_desc)
    # print(ttl_enum)
    # print(ttl_eq)
    return [ttl_desc, ttl_enum, ttl_eq]

def get_eq_img_path(tex_code, slide_number, eq_num):
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize = (2,2))
    ax.text(0.5, 0.5, tex_code, fontsize = 14, ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')
    # plt.show()
    buffer = BytesIO()
    plt.savefig(buffer, dpi=300, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buffer.seek(0)
    img_path = f'code\\data\\equations\\eq_{slide_number}_{eq_num + 1}.png'
    with open(img_path, 'wb') as img_file:
        img_file.write(buffer.getvalue())
    
    return img_path

def generate_random_slide(slide_number, data, style_obj):
    bg_color, title_font_family, title_font_bold, title_font_attr, desc_font_family, desc_font_attr = style_obj["bg_color"], style_obj["title_font_family"], style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj["desc_font_family"], style_obj["desc_font_attr"]
    # Determining when a slide has BG as White
    THRES = 0.667
    if generate_random_value(float, 0, 1) < THRES:
        bg_color = {"r": 255, "g": 255, "b": 255}

    # # Define total number of body elements
    # if slide_number == 1:
    #     total_body_elements = 0
    # else:
    #     total_body_elements = generate_random_value(int, 1, 3)
    n_elements_list = count_body_elements(data, slide_number)
    total_body_elements = sum(n_elements_list)
    # n_elements_list = [descriptions, enumerations, figures]
    # n_elements_list = generate_n_numbers_with_sum(total_body_elements, 3)
    # Distribute the total count among the three categories


    # Generate random slide layout
    layout_id = generate_random_layout(total_body_elements)
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(layout_id)

    ## Skeleton Slide object with Slide-level metadata
    slide = {
        "pg_no": slide_number,
        "bg_color": bg_color,
        "slide_layout": layout_id,
        "elements": {}
    }

    # Title Generation
    ## Generate Font-level random values for Title
    font_color = generate_contrasting_font_color(bg_color)

    ## Fetch Random content
    title_content = data["slides"][slide_number - 1]["title"]
    # print(title_content)

    ## Putting it together for the title object
    slide['elements']['title'] = [{
            "label": "text",
            "value": title_content,
            "xmin": all_dims['title']['left'],
            "ymin": all_dims['title']['top'],
            "width": all_dims['title']['width'],
            "height": all_dims['title']['height'],
            "style": {
                "font_name": title_font_family,
                "font_size": title_font_attr["font_size"],
                "font_color": font_color,
                "bold": title_font_bold,
                "italics": False,
                "underlined": False
            }
        }]    
       
    if total_body_elements != 0:
        # Body Generation
        ## Randomly shuffle the bounding box dimensions of the body elements
        random.shuffle(all_dims['body'])
        element_index = 0

        ## Generate Descriptions
        slide['elements']['description'] = []
        for _ in range(n_elements_list[0]):
            font_obj = generate_random_font("description")
            desc = data["slides"][slide_number - 1]["description"]
            desc_instance = {
            "label": "text",
            "value": desc,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": False,
                "italics": False,
                "underlined": False
               }
            } 
            slide['elements']['description'].append(desc_instance)
            element_index += 1

        ## Generate Enumerations
        for _ in range(n_elements_list[1]):
            font_obj = generate_random_font("description")
            enum = data["slides"][slide_number - 1]["enumeration"]
            enum_instance = {
            "label": "enumeration",
            "value": enum,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": max(all_dims['body'][element_index]['height'], 0.5*len(enum)),
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": font_obj["bold"],
                "italics": font_obj["italics"],
                "underlined": font_obj["underline"]
               }
            } 
            slide['elements']['description'].append(enum_instance)
            element_index += 1
        
        # Render Equations
        slide['elements']['equations'] = []
        for i in range(n_elements_list[2]):
            fig_instance = {
            "label": "equation",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "desc": data["slides"][slide_number - 1]["equations"][i]["eq_desc"],
            "path": get_eq_img_path(data["slides"][slide_number - 1]["equations"][i]['tex_code'], slide_number, i)
            }
            slide['elements']['equations'].append(fig_instance)
            element_index += 1

        # ## Generate figures
        # slide['elements']['figure'] = []
        # for _ in range(n_elements_list[2]):
        #     fig_instance = {
        #     "label": "image",
        #     "xmin": all_dims['body'][element_index]['left'],
        #     "ymin": all_dims['body'][element_index]['top'],
        #     "width": all_dims['body'][element_index]['width'],
        #     "height": all_dims['body'][element_index]['height'],
        #     "path": 'code\\assets\\frog_img.png'
        #     }
        #     slide['elements']['figure'].append(fig_instance)
        #     element_index += 1
    
    return slide

    

if __name__ == "__main__":
    # num_files = 3
    buffer_dir = 'code/buffer'
    json_files = [f for f in os.listdir(buffer_dir) if f.endswith('.json')]

    for json_file in json_files: 
        style_obj = generate_random_style_obj()
        # print(style_obj)
        slide_id, _ = os.path.splitext(json_file)
        file_path = os.path.join(buffer_dir, json_file)
        with open(file_path, 'r') as file:
            data = json.load(file)
        n_slides = len(data["slides"])
        slides = [generate_random_slide(i+1, data, style_obj) for i in range(n_slides)]
    
        new_data = {
            "slide_id": slide_id,
            "n_slides": len(slides),
            "topic" : data["topic"],
            "presenter": pick_random_presenter(),
            "date": generate_random_date(),
            "slides": slides
        }
        with open(f"code\\buffer\\full\\{slide_id}.json", 'w') as json_file:
            json.dump(new_data, json_file, indent=3)
        print(f"{slide_id} JSON file created successfully")
    
    # #Delete content JSON files
    # for json_file in json_files:
    #     os.remove(os.path.join(buffer_dir, json_file))
    


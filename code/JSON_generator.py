import os
import random
import json
from layouts import CustomLayouts
from random_generator import generate_random_style_obj, generate_random_font, generate_random_value, pick_random, generate_random_layout, generate_n_numbers_with_sum, generate_contrasting_font_color
import pandas as pd


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



def generate_random_slide(slide_number, data, style_obj):
    bg_color, title_font_family, title_font_attr, desc_font_family, desc_font_attr = style_obj["bg_color"], style_obj["title_font_family"], style_obj["title_font_attr"], style_obj["desc_font_family"], style_obj["desc_font_attr"]
    # Determining when a slide has BG as White
    THRES = 0.667
    if generate_random_value(float, 0, 1) < THRES:
        bg_color = {"r": 255, "g": 255, "b": 255}

    # # Define total number of body elements
    # if slide_number == 1:
    #     total_body_elements = 0
    # else:
    #     total_body_elements = generate_random_value(int, 1, 3)
    total_body_elements = 2
    # n_elements_list = [descriptions, enumerations, figures]
    n_elements_list = [1, 1, 0]
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
                "bold": random.random() < 0.33,
                "italics": random.random() < 0.1,
                "underlined": random.random() < 0.1
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
                "italics": random.random() < 0.1,
                "underlined": random.random() < 0.1
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

        ## Generate figures
        slide['elements']['figure'] = []
        for _ in range(n_elements_list[2]):
            fig_instance = {
            "label": "image",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "path": 'code\\assets\\frog_img.png'
            }
            slide['elements']['figure'].append(fig_instance)
            element_index += 1
    
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
        print(data)
        n_slides = 4
        slides = [generate_random_slide(i+1, data, style_obj) for i in range(n_slides)]
    
        data = {
            "slide_id": slide_id,
            "n_slides": len(slides),
            "slides": slides
        }
        with open(f"code\\buffer\\full\\{slide_id}.json", 'w') as json_file:
            json.dump(data, json_file, indent=3)
        print(f"{slide_id} JSON file created successfully")
    
    # #Delete content JSON files
    # for json_file in json_files:
    #     os.remove(os.path.join(buffer_dir, json_file))
    


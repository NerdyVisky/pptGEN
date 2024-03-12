import random
import json
from layouts import CustomLayouts
from random_generator import generate_random_color, generate_random_font, generate_random_value, pick_random, generate_random_layout, generate_n_numbers_with_sum, generate_contrasting_font_color
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
FONT_STYLES = ['Arial', 'Times New Roman', 'Georgia', 'Calibiri']
TITLES_DICT = generate_dicts("code\data\\titles.csv")
DESC_DICT = generate_dicts("code\data\\descriptions.csv")
ENUM_DICT = generate_dicts("code\data\\enumerations.csv")
PATH_DICT = generate_dicts("code\data\\figures.csv")

# print(TITLES_DICT['NLP'])



def generate_random_slide(slide_number, topic, bg_color, title_font_family, title_font_attr, desc_font):
    
    # Determining when a slide has BG as White
    THRES = 0.667
    if generate_random_value(float, 0, 1) < THRES:
        bg_color = {"r": 255, "g": 255, "b": 255}

    # Define total number of body elements
    total_body_elements = generate_random_value(int, 0, 2)
    # n_elements_list = [descriptions, enumerations, figures]
    n_elements_list = generate_n_numbers_with_sum(total_body_elements, 3)
    # Distribute the total count among the three categories


    # Generate random slide layout
    layout_id = generate_random_layout(total_body_elements)
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(layout_id)
    # print(all_dims)

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
    title_content = pick_random(TITLES_DICT[topic])
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
                "bold": title_font_attr["bold"],
                "italics": title_font_attr["italics"],
                "underlined": title_font_attr["underline"]
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
            desc = pick_random(DESC_DICT[topic])
            desc_instance = {
            "label": "text",
            "value": desc,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "style": {
                "font_name": desc_font,
                "font_size": font_obj["font_size"],
                "font_color": font_color,
                "bold": font_obj["bold"],
                "italics": font_obj["italics"],
                "underlined": font_obj["underline"]
               }
            } 
            slide['elements']['description'].append(desc_instance)
            element_index += 1

        ## Generate Enumerations
        for _ in range(n_elements_list[1]):
            font_obj = generate_random_font("description")
            enum_raw = pick_random(ENUM_DICT[topic])
            enum = enum_raw.split('<pt>')
            enum_instance = {
            "label": "enumeration",
            "value": enum,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": max(all_dims['body'][element_index]['height'], 0.5*len(enum)),
            "style": {
                "font_name": desc_font,
                "font_size": font_obj["font_size"],
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
            "path": pick_random(PATH_DICT[topic])
            }
            slide['elements']['figure'].append(fig_instance)
            element_index += 1
    
    return slide

    

if __name__ == "__main__":
    num_files = 3
    for i in range(num_files): 
        topic = pick_random(TOPICS)
        n_slides = generate_random_value(int, 3, 7)
        bg_color = generate_random_color()
        title_font_family = pick_random(FONT_STYLES)
        title_font_attr = generate_random_font("title")
        desc_font = pick_random(FONT_STYLES)
        slides = [generate_random_slide(i+1, topic, bg_color, title_font_family, title_font_attr, desc_font) for i in range(n_slides)]
    
        data = {
            "topic": topic,
            "n_slides": n_slides,
            "slides": slides
        }
        with open(f"code\\buffer\\{topic}_{i}.json", 'w') as json_file:
            json.dump(data, json_file, indent=3)
        print(f"{topic}_{i} JSON file created successfully")

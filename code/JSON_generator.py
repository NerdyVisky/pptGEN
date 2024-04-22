import os
import random
import json
from layouts import CustomLayouts
from random_generator import (generate_random_style_obj, 
                              generate_random_font, 
                              generate_random_value, 
                              pick_random, 
                              generate_footer_obj,
                              generate_random_layout, 
                              generate_n_numbers_with_sum, 
                              generate_contrasting_font_color,
                              generate_random_date,
                              pick_random_presenter)
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO 
import subprocess
import fitz



def count_footer_elements(date, showFN, showSN):
    footer_elements = []
    if date != None:
        footer_elements.append("date")
    if showSN == True:
        footer_elements.append("slideNr")
    if showFN == True:
        footer_elements.append("footnote")
    return footer_elements

def count_body_elements(data, slide_number):
    ttl_desc = 0
    ttl_enum = 0
    ttl_url = 0
    ttl_eq = 0
    ttl_tb = 0
    ttl_fig = 0
    for k, v in data["slides"][slide_number - 1].items():
        if k == 'description' and v != "":
            ttl_desc = 1
        elif k == 'enumeration' and v:
            ttl_enum = 1
        elif k == 'url' and v != "":
            ttl_url = 1
        elif k == 'equations' and v:
            ttl_eq = len(v)
        elif k == 'tables' and v:
            ttl_tb = len(v)
        elif k == 'figures' and v:
            ttl_fig = len(v)
    return [ttl_desc, ttl_enum, ttl_url, ttl_eq, ttl_tb, ttl_fig]

def resize_image(input_image_path, slide_number, i, output_image_dir, box_width, box_height, dpi=96):
    box_width_pixels = int(box_width * dpi)
    box_height_pixels = int(box_height * dpi)
    with Image.open(input_image_path) as img:
        img_width, img_height = img.size
        img_aspect_ratio = img_width / img_height
        box_aspect_ratio = box_width_pixels / box_height_pixels
        if img_aspect_ratio > box_aspect_ratio:
            new_width = box_width_pixels
            new_height = int(box_width_pixels / img_aspect_ratio)
        else:
            new_height = box_height_pixels
            new_width = int(box_height_pixels * img_aspect_ratio)
        resized_img = img.resize((new_width, new_height))
        new_img_path = os.path.join(output_image_dir, f'{slide_number}_{i}.png')
        resized_img.save(new_img_path)
        new_width_inches = new_width / dpi
        new_height_inches = new_height / dpi
        return new_img_path, new_width_inches, new_height_inches

def remove_tmp_files():
    tmp_files = ['tmp.tex', 'tmp.aux', 'tmp.log', 'tmp.pdf']
    for f in tmp_files:
        if os.path.exists(f):
            os.remove(f)
    # os.remove(f'tmp.tex')
    # os.remove(f'tmp.aux')
    # os.remove(f'tmp.log')
    # os.remove(f'tmp.pdf')
    # tmp_eqs = 'code\\buffer\\equations'
    # for filename in os.listdir(tmp_eqs):
    #         file_path = os.path.join(tmp_eqs, filename)
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)
                
    # tmp_tabs = 'code\\buffer\\tables'
    # for filename in os.listdir(tmp_tabs):
    #         file_path = os.path.join(tmp_tabs, filename)
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)
            
    # tmp_figs = 'code\\buffer\\figures'
    # for filename in os.listdir(tmp_figs):
    #         file_path = os.path.join(tmp_figs, filename)
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)


def generate_random_slide(slide_number, data, style_obj, footer_obj, presentation_ID):
    bg_color, title_font_family, title_font_bold, title_font_attr, desc_font_family, desc_font_attr = style_obj["bg_color"], style_obj["title_font_family"], style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj["desc_font_family"], style_obj["desc_font_attr"]
    date = style_obj["date"]
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
            font_obj = generate_random_font("enumeration")
            enum = data["slides"][slide_number - 1]["enumeration"]
            enum_instance = {
            "label": "enumeration",
            "heading": {
                "value": enum[0],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'],
                "width": all_dims['body'][element_index]['width'],
                "height": 0.5,
            },
            "value": enum[1:],
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'] + 0.5,
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


        #Render URLs
        slide['elements']['url'] = []
        for _ in range(n_elements_list[2]):
            font_obj = generate_random_font("url")
            desc = data["slides"][slide_number - 1]["url"]
            desc_instance = {
            "value": desc,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": {"r": 0, "g": 0, "b": 238},
                "bold": False,
                "italics": True,
                "underlined": True
               }
            } 
            slide['elements']['url'].append(desc_instance)
            element_index += 1


        # Render Equations
        resized_path = f'code\\buffer\\structs\\eq\\{presentation_ID}'
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)

        slide['elements']['equations'] = []
        for i in range(n_elements_list[3]):
            img_path = data["slides"][slide_number - 1]["equations"][i]["path"]
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            eq_instance = {
            "label": "equation",
            "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
            "ymin": all_dims['body'][element_index]['top'] - (n_h - all_dims['body'][element_index]['height'])/2,
            "width": n_w,
            "height": n_h,
            "desc": data["slides"][slide_number - 1]["equations"][i]["desc"],
            "path": resized_img_path
            }
            slide['elements']['equations'].append(eq_instance)
            element_index += 1
            remove_tmp_files()

        # Render Tables
        resized_path = f'code\\buffer\\structs\\tb\\{presentation_ID}'
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)

        slide['elements']['tables'] = []
        for i in range(n_elements_list[4]):
            img_path = data["slides"][slide_number - 1]["tables"][i]['path']
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            tab_instance = {
            "label": "table",
            "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
            "ymin": all_dims['body'][element_index]['top'] - (n_h - all_dims['body'][element_index]['height'])/2,
            "width": n_w,
            "height": n_h,
            "desc": data["slides"][slide_number - 1]["tables"][i]["desc"],
            "path": resized_img_path    
            }
            slide['elements']['tables'].append(tab_instance)
            element_index += 1
            remove_tmp_files()

        # Render Figures
        

        slide['elements']['figures'] = []
        for i in range(n_elements_list[5]):
            font_obj = generate_random_font("enumeration")
            # if data["slides"][slide_number - 1]["figures"][i]["label"] == "diagram":    
            #     img_path = get_fig_img_path_matplot(data["slides"][slide_number - 1]["figures"][i]['fig_code'], slide_number, i)
            # else:
            img_path = data["slides"][slide_number - 1]["figures"][i]['path']
            label = data["slides"][slide_number - 1]["figures"][i]['label'] 
            if label == 'tree' or label == 'chart' or label == 'flow-chart' or label == 'block-diagram':
                resized_path = f'code\\buffer\\figures\\{label}\\{presentation_ID}'
            else:
                resized_path = f'code\\buffer\\plots\\{label}\\{presentation_ID}'

            if not os.path.exists(resized_path):
                os.makedirs(resized_path)
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            fig_instance = {
            "label": label,
            "caption": {
                "value": data["slides"][slide_number - 1]["figures"][i]["desc"],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'] + (n_h - 0.35),
                "width": all_dims['body'][element_index]['width'],
                "height": 0.35,
                "style": {
                    "font_name": desc_font_family,
                    "font_size": 14,
                    "font_color": font_color,
                    "bold": font_obj["bold"],
                    "italics": True,
                    "underlined": font_obj["underline"]
               }
            },
            "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
            "ymin": all_dims['body'][element_index]['top'] - (n_h - all_dims['body'][element_index]['height'])/2,
            "width": n_w,
            "height": n_h,
            "desc": data["slides"][slide_number - 1]["figures"][i]["desc"],
            "path": resized_img_path
            }
            slide['elements']['figures'].append(fig_instance)
            element_index += 1
            remove_tmp_files()
        

    ##Footer generation
    slide['elements']['footer'] = []
    for i, obj in enumerate(footer_obj):
        footer_type = ''
        if 'slideNr' in obj.keys():
            footer_type = 'slideNr'
            value = str(slide_number)
        if 'footnote' in obj.keys():
            footer_type = 'footnote'
            value = "This is a footnote"
        if 'date' in obj.keys():
            footer_type = 'date'
            value = date         
        footer_dim = all_dims['footer'][obj[footer_type]]
        foot_instance = {
                "label": footer_type,
                "location": footer_dim["type"],
                "value": value,
                "xmin": footer_dim['left'],
                "ymin": footer_dim['top'],
                "width": footer_dim['width'],
                "height": footer_dim['height'],
                "style": {
                    "font_name": desc_font_family,
                    "font_size": desc_font_attr["font_size"],
                    "font_color": font_color,
                    "bold": False,
                    "italics": False,
                    "underlined": False
                }
            }
        slide['elements']['footer'].append(foot_instance)
    
    return slide

    

if __name__ == "__main__":
    # num_files = 3
    buffer_dir = 'code/buffer'
    json_files = [f for f in os.listdir(buffer_dir) if f.endswith('.json')]

    for json_file in json_files: 
        style_obj = generate_random_style_obj()
        footer_obj = generate_footer_obj()
        print(footer_obj)
        # print(style_obj)
        slide_id, _ = os.path.splitext(json_file)
        file_path = os.path.join(buffer_dir, json_file)
        with open(file_path, 'r') as file:
            data = json.load(file)
        n_slides = len(data["slides"])
        slides = [generate_random_slide(i+1, data, style_obj, footer_obj, slide_id) for i in range(n_slides)]
    
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
    


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
    ttl_cd = 0
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
        elif k == 'code' and v:
            ttl_cd = len(v)
    return [ttl_desc, ttl_enum, ttl_url, ttl_eq, ttl_tb, ttl_fig, ttl_cd]

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
    bg_color, title_font_family, title_font_bold, title_font_attr, title_align,\
          desc_font_family, desc_font_attr, date, tmp_list = style_obj["bg_color"], style_obj["title_font_family"],\
              style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj['title_align'], style_obj["desc_font_family"],\
                  style_obj["desc_font_attr"], style_obj["date"], style_obj["template"]
    tmp_path, isDark = tmp_list
    n_elements_list = count_body_elements(data, slide_number)
    total_body_elements = sum(n_elements_list)
    topic = data["topic"]
    title_dark, title_light = style_obj['title_font_dark'], style_obj['title_font_light']
    # Title Generation
    ## Generate Font-level random values for Title
    if(tmp_path != ''):
        if isDark == 0:
            title_font = title_dark
            font_color = {"r": 0, "g": 0, "b": 0}
        elif isDark == 1:
            title_font = title_light
            font_color = {"r": 255, "g": 255, "b": 255}
        else:
            raise Exception('Invalid template list')
    else:
        title_font, font_color = generate_contrasting_font_color(bg_color, title_dark, title_light)
    ## Fetch Random content
    title_content = data["slides"][slide_number - 1]["title"]
    if(total_body_elements > 3):
        slide = {
             "pg_no": slide_number,
             "bg_color": bg_color,
             "slide_layout": 0,
             "elements": {}
        }
        slide['elements']['title'] = [{
            "label": "title",
            "value": title_content,
            "xmin": 0.5,
            "ymin": 2,
            "width": 9*1.33,
            "height": 1.25,
            "style": {
                "font_name": title_font_family,
                "font_size": title_font_attr["font_size"],
                "font_color": title_font,
                "bold": title_font_bold,
                "italics": False,
                "underlined": False,
                "h_align": title_align
            }
        }]
        return slide

    # Generate random slide layout
    layout_id = generate_random_layout(total_body_elements)
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(layout_id)

    ## Skeleton Slide object with Slide-level metadata
    slide = {
        "pg_no": slide_number,
        "slide_layout": layout_id,
        "elements": {}
    }
    if tmp_path != '':
        slide["template"] = tmp_path
    else:
        slide["bg_color"] = bg_color

    ## Putting it together for the title object
    slide['elements']['title'] = [{
            "label": "title",
            "value": title_content,
            "xmin": all_dims['title']['left'],
            "ymin": all_dims['title']['top'],
            "width": all_dims['title']['width'],
            "height": all_dims['title']['height'],
            "style": {
                "font_name": title_font_family,
                "font_size": title_font_attr["font_size"],
                "font_color": title_font,
                "bold": title_font_bold,
                "italics": False,
                "underlined": False,
                "h_align": title_align
            }
        }]    
       
    if total_body_elements != 0:
        # Body Generation
        ## Randomly shuffle the bounding box dimensions of the body elements
        random.shuffle(all_dims['body'])
        element_index = 0
        h_desc_align, v_desc_align = pick_random("alignments")
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
                "underlined": False,
                "h_align": h_desc_align,
                "v_align": v_desc_align
               }
            } 
            slide['elements']['description'].append(desc_instance)
            element_index += 1

        ## Generate Enumerations
        P_H = 1
        h_enum_align, v_enum_align = pick_random("alignments")
        for _ in range(n_elements_list[1]):
            font_obj = generate_random_font("enumeration")
            enum = data["slides"][slide_number - 1]["enumeration"]
            enum_instance = {
            "label": "enumeration",
            "value": enum[1:],
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'] + 0.5,
            "width": all_dims['body'][element_index]['width'],
            "height": max(all_dims['body'][element_index]['height'], 0.5*len(enum)) - 0.5,
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": font_obj["bold"],
                "italics": font_obj["italics"],
                "underlined": font_obj["underline"],
                "h_align": 'left',
                "v_align": 'top'
               }
            }
            if (P_H > random.random()):
                enum_instance['heading'] = {
                "label": 'heading',
                "value": enum[0],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'],
                "width": all_dims['body'][element_index]['width'],
                "height": 0.5,
                }
            
            slide['elements']['description'].append(enum_instance)
            element_index += 1


        #Render URLs
        h_url_align, v_url_align = ['left', 'center']
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
                "font_size": font_obj['font_size'],
                "font_color": {"r": 0, "g": 0, "b": 238},
                "bold": False,
                "italics": True,
                "underlined": True,
                "h_align": h_url_align,
                "v_align": v_url_align
               }
            } 
            slide['elements']['url'].append(desc_instance)
            element_index += 1
       
        # Render Equations
       

        P_E = 1
        slide['elements']['equations'] = []
        for i in range(n_elements_list[3]):
            ele_ymin = all_dims['body'][element_index]['top']
            ele_height = all_dims['body'][element_index]['height']
            eq_instance = {}
            if (P_E > random.random()):
                ele_height =all_dims['body'][element_index]['height'] - 0.35 
                if random.random() > 0.5:
                # Caption below the visual element
                    cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.35 
                else:
                    # Caption above the visual element
                    ele_ymin = all_dims['body'][element_index]['top'] + 0.35
                    cap_ymin = all_dims['body'][element_index]['top']
                eq_instance["caption"] = {
                    "label": "equation_caption",
                    "value": data["slides"][slide_number - 1]["equations"][i]["desc"],
                    "xmin": all_dims['body'][element_index]['left'],
                    "ymin": cap_ymin,
                    "width": all_dims['body'][element_index]['width'],
                    "height": 0.35,
                    "style": {
                        "font_name": desc_font_family,
                        "font_size": 14,
                        "font_color": font_color,
                        "bold": random.random() > 0.5,
                        "italics": random.random() > 0.25,
                        "underlined": random.random() > 0.75
                }
                }
            img_path = data["slides"][slide_number - 1]["equations"][i]["path"]
            eq_instance = {**eq_instance, **{
            "label": "equation",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": ele_height,
            "width": all_dims['body'][element_index]['width'],
            "height": ele_height,
            "desc": data["slides"][slide_number - 1]["equations"][i]["desc"],
            "path": img_path
            }}
            slide['elements']['equations'].append(eq_instance)
            element_index += 1
            remove_tmp_files()

        # Render Table

        P_T = 1
        slide['elements']['tables'] = []
        for i in range(n_elements_list[4]):
            ele_ymin = all_dims['body'][element_index]['top']
            ele_height = all_dims['body'][element_index]['height']
            tab_instance = {}
            if (P_T > random.random()):
                ele_height =all_dims['body'][element_index]['height'] - 0.35 
                if random.random() > 0.5:
                # Caption below the visual element
                    cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.35 
                else:
                    # Caption above the visual element
                    ele_ymin = all_dims['body'][element_index]['top'] + 0.35
                    cap_ymin = all_dims['body'][element_index]['top']
                tab_instance["caption"] = {
                    "label": "table_caption",
                    "value": data["slides"][slide_number - 1]["tables"][i]["desc"],
                    "xmin": all_dims['body'][element_index]['left'],
                    "ymin": cap_ymin,
                    "width": all_dims['body'][element_index]['width'],
                    "height": 0.35,
                    "style": {
                        "font_name": desc_font_family,
                        "font_size": 14,
                        "font_color": font_color,
                        "bold": random.random() > 0.5,
                        "italics": random.random() > 0.25,
                        "underlined": random.random() > 0.75
                }
                }
            
                
            img_path = data["slides"][slide_number - 1]["tables"][i]['path']
            tab_instance = {**tab_instance, **{
            "label": "table",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": ele_ymin,
            "width": all_dims['body'][element_index]['width'],
            "height": ele_height,
            "desc": data["slides"][slide_number - 1]["tables"][i]["desc"],
            "path": img_path    
            }}
            
            slide['elements']['tables'].append(tab_instance)
            element_index += 1
            remove_tmp_files()

        # Render Figures
        P_F = 1
        slide['elements']['figures'] = []
        for i in range(n_elements_list[5]):
            font_obj = generate_random_font("enumeration")
            # if data["slides"][slide_number - 1]["figures"][i]["label"] == "diagram":    
            #     img_path = get_fig_img_path_matplot(data["slides"][slide_number - 1]["figures"][i]['fig_code'], slide_number, i)
            # else:
            fig_instance = {}
            img_path = data["slides"][slide_number - 1]["figures"][i]['path']
            label = data["slides"][slide_number - 1]["figures"][i]['label']
            ele_ymin = all_dims['body'][element_index]['top']
            ele_height =  all_dims['body'][element_index]['height']
            if (P_F > random.random()):
                ele_height =  all_dims['body'][element_index]['height'] - 0.35
                if random.random() > 0.5:
                # Caption below the visual element
                    cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.35 
                else:
                    # Caption above the visual element
                    ele_ymin = all_dims['body'][element_index]['top'] + 0.35
                    cap_ymin = all_dims['body'][element_index]['top']
                fig_instance["caption"] = {
                    "label": "figure_caption",
                    "value": data["slides"][slide_number - 1]["figures"][i]["desc"],
                    "xmin": all_dims['body'][element_index]['left'],
                    "ymin": cap_ymin,
                    "width": all_dims['body'][element_index]['width'],
                    "height": 0.35,
                    "style": {
                        "font_name": desc_font_family,
                        "font_size": 14,
                        "font_color": font_color,
                        "bold": random.random() > 0.5,
                        "italics": random.random() > 0.25,
                        "underlined": random.random() > 0.75
                }
                }
            
            # if label == 'graph' or label == 'tree' or label == 'flow-chart' or label == 'block-diagram':
            #     superlabel = 'diagram'
            # else:
            #     superlabel = 'graph'
            fig_instance = {**fig_instance, **{
            "label": label,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": ele_ymin,
            "width": all_dims['body'][element_index]['width'],
            "height": ele_height,
            "desc": data["slides"][slide_number - 1]["figures"][i]["desc"],
            "path": img_path
            }}

            slide['elements']['figures'].append(fig_instance)
            element_index += 1
            remove_tmp_files()
    
        slide['elements']['code'] = []
        for i in range(n_elements_list[6]):
            font_obj = generate_random_font("url")
            value = data["slides"][slide_number - 1]["code"][i]['value']
            caption = data["slides"][slide_number - 1]["code"][i]['desc']
            code_instance = {
            "label": "code",
            "desc": caption,
            "value": value,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "style": {
                "font_name": 'Courier New',
                "font_size": font_obj['font_size'],
                "font_color": font_color,
                "bold": False,
                "italics": False,
                "underlined": False,
                "h_align": 'left',
                "v_align": 'top'
               }
            } 
            slide['elements']['code'].append(code_instance)
            element_index += 1
        

    ##Footer generation
    slide['elements']['footer'] = []
    for i, obj in enumerate(footer_obj):
        footer_type = ''
        if 'slideNr' in obj.keys():
            footer_type = 'slideNr'
            value = str(slide_number)
        if 'footnote' in obj.keys():
            footer_type = 'footnote'
            value = topic
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
    # get the list of json files from all subdirectories of folder dataset/json/
    created_files = []
    for subject in os.listdir("dataset/json/"):
        for topic in os.listdir(f"dataset/json/{subject}"):
            created_files.append(topic)
    print("Running layout discriminator module...")
    temp_dir = f"code/temp"
    entries = os.listdir(temp_dir)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(temp_dir, entry))]
    DUP_FAC = 2
    for directory in directories:
        json_files = [f for f in os.listdir(os.path.join(temp_dir,directory)) if f.endswith('.json')]
        json_files = [f for f in json_files if f.split('.')[0] not in created_files]
        n_json_files = len(json_files)
        for i, json_file in enumerate(json_files): 
            presentation_ID, _ = os.path.splitext(json_file)
            file_path = os.path.join(temp_dir, directory, json_file)
            with open(file_path, 'r') as file:
                data = json.load(file)
            n_slides = len(data["slides"])
            subject = data["subject"]
            for ver in range(DUP_FAC):
                style_obj = generate_random_style_obj()
                footer_obj = generate_footer_obj()
                
                slides = [generate_random_slide(i+1, data, style_obj, footer_obj, presentation_ID) for i in range(n_slides)]
                new_data = {
                    "slide_id": presentation_ID,
                    "n_slides": len(slides),
                    "topic" : data["topic"],
                    "subject": subject,
                    "presenter": pick_random_presenter(),
                    "date": generate_random_date(),
                    "slides": slides
                }
                if not os.path.exists(f"code/buffer/full/{directory}"):
                    os.mkdir(f"code/buffer/full/{directory}")
                if not os.path.exists(f"code/buffer/full/{directory}/{presentation_ID}"):
                    os.mkdir(f"code/buffer/full/{directory}/{presentation_ID}")

                with open(f"code/buffer/full/{directory}/{presentation_ID}/{ver + 1}.json", 'w') as json_file:
                    json.dump(new_data, json_file, indent=3)

            print(f"🟢 ({i+1}/{n_json_files}): generated {DUP_FAC} layouts for {presentation_ID}")
    print('\n')


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
                              pick_random_presenter,
                              pick_random_logo,
                              generate_title_slide_obj,
                              generate_random_phrases,
                              modify_url_prefix,
                              random_logo_pos
                              )


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
        # elif k == 'url' and v != "":
        #     ttl_url = 1
        elif k == 'equations' and v:
            ttl_eq = len(v)
        elif k == 'tables' and v:
            ttl_tb = len(v)
        elif k == 'figures' and v:
            ttl_fig = len(v)
        elif k == 'code' and v:
            ttl_cd = len(v)
    # return [ttl_desc, ttl_enum, ttl_url, ttl_eq, ttl_tb, ttl_fig, ttl_cd]
    return [ttl_desc, ttl_enum, 0, ttl_eq, ttl_tb, ttl_fig, ttl_cd]

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

def insert_title_slide(data, style_obj, course_code):
    slide = {
        "pg_no": 0,
        "slide_layout": 0,
        "elements": {}
    }
    title_obj = generate_title_slide_obj()
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(0)
    path, _, _ = pick_random_logo(0.5)
    slide['elements']['footer'] = []
    for i, obj in enumerate(title_obj):
        if 'PT' in obj.keys():
            slide['elements']['title'] = [{
                "label": 'presentation_title',
                "value": data["topic"],
                "xmin": all_dims['topic_slide'][obj['PT']]['left'],
                "ymin": all_dims['topic_slide'][obj['PT']]['top'],
                "width": all_dims['topic_slide'][obj['PT']]['width'],
                "height": all_dims['topic_slide'][obj['PT']]['height'],
                "style": {
                    "font_name": style_obj['title_font_family'],
                    "font_size": style_obj['title_font_attr']["font_size"],
                    "font_color": style_obj['title_font_dark'],
                    "bold": style_obj["title_font_bold"],
                    "italics": random.random() > 0.8,
                    "underlined": random.random() > 0.1
                }
            }]
        if 'DT' in obj.keys():
            footer_instance = {
                "label": 'date',
                "location": 2,
                "value": style_obj['date'],
                "xmin": all_dims['topic_slide'][obj['DT']]['left'],
                "ymin": all_dims['topic_slide'][obj['DT']]['top'],
                "width": all_dims['topic_slide'][obj['DT']]['width'],
                "height": all_dims['topic_slide'][obj['DT']]['height'],
                "style": {
                    "font_name": style_obj['desc_font_family'],
                    "font_size": style_obj['desc_font_attr']["font_size"],
                    "font_color": style_obj['title_font_dark'],
                    "bold": False,
                    "italics": False,
                    "underlined": False
                }
            }
            slide['elements']['footer'].append(footer_instance)


        if 'CC' in obj.keys():
            footer_instance = {
                "label": 'course_code',
                "location": 2,
                "value": course_code,
                "xmin": all_dims['topic_slide'][obj['CC']]['left'],
                "ymin": all_dims['topic_slide'][obj['CC']]['top'],
                "width": all_dims['topic_slide'][obj['CC']]['width'],
                "height": all_dims['topic_slide'][obj['CC']]['height'],
                "style": {
                    "font_name": style_obj['desc_font_family'],
                    "font_size": style_obj['desc_font_attr']["font_size"],
                    "font_color": style_obj['title_font_dark'],
                    "bold": False,
                    "italics": False,
                    "underlined": False
                }
            }
            slide['elements']['footer'].append(footer_instance)

        if 'Lg' in obj.keys():
            slide['elements']['graphic'] = [{
                "label": 'logo',
                "value": path,
                "xmin": all_dims['topic_slide'][obj['Lg']]['left'],
                "ymin": all_dims['topic_slide'][obj['Lg']]['top'],
                "width": all_dims['topic_slide'][obj['Lg']]['width'],
                "height": all_dims['topic_slide'][obj['Lg']]['height']
            }]
        if 'Is' in obj.keys():
            footer_instance = {
                "label": 'instructor',
                "location": 2,
                "value": style_obj['instructor'],
                "xmin": all_dims['topic_slide'][obj['Is']]['left'],
                "ymin": all_dims['topic_slide'][obj['Is']]['top'],
                "width": all_dims['topic_slide'][obj['Is']]['width'],
                "height": all_dims['topic_slide'][obj['Is']]['height'],
                "style": {
                    "font_name": style_obj['desc_font_family'],
                    "font_size": style_obj['desc_font_attr']["font_size"],
                    "font_color": style_obj['title_font_dark'],
                    "bold": False,
                    "italics": False,
                    "underlined": False
                }
            }
            slide['elements']['footer'].append(footer_instance)
    return slide       
    


def generate_random_slide(slide_number, data, style_obj, footer_obj, course_code, presentation_ID):
    bg_color, title_font_family, title_font_bold, title_font_attr, title_align,\
          desc_font_family, desc_font_attr, date, tmp_list = style_obj["bg_color"], style_obj["title_font_family"],\
              style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj['title_align'], style_obj["desc_font_family"],\
                  style_obj["desc_font_attr"], style_obj["date"], style_obj["template"]
    tmp_path, isDark = tmp_list
    logo_path, logo_width, logo_height= style_obj['logo']
    url_font_color = style_obj['url_font_color']
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
                "h_align": title_align,
                "v_align": random.choice(['top', 'middle', 'bottom'])
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
    
    if logo_path != '':
        bbox_logo = random_logo_pos(footer_obj)
        slide["elements"]["graphic"] = [{
            "label": "logo",
            "value": logo_path,
            "xmin": bbox_logo['left'],
            "ymin": bbox_logo['top'],
            "width": logo_width,
            "height": min(logo_height, 7.5 - bbox_logo['top']),
        }]

    ## Putting it together for the title object
    if random.random() > 0.20:
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
                    "italics": random.random() > 0.75,
                    "underlined": random.random() > 0.75,
                    "h_align": title_align,
                    "v_align": random.choice(['top', 'middle', 'bottom'])
                }
            }]    
       
    if total_body_elements != 0:
        # Body Generation
        ## Randomly shuffle the bounding box dimensions of the body elements
        random.shuffle(all_dims['body'])
        element_index = 0
        h_desc_align, v_desc_align = pick_random("alignments")
        ## Generate Descriptions
        slide['elements']['text'] = []
        for _ in range(n_elements_list[0]):
            font_obj = generate_random_font("description")
            desc = data["slides"][slide_number - 1]["description"]
            styled_phrases = generate_random_phrases(desc)
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
                "v_align": v_desc_align,
                "phrases": styled_phrases
               }
            } 
            slide['elements']['text'].append(desc_instance)
            element_index += 1

        ## Generate Enumerations
        P_H = 0.25
        hasHeading = P_H > random.random()
        h_enum_align, v_enum_align = pick_random("alignments")
        for i in range(n_elements_list[1]):
            font_obj = generate_random_font("enumeration")
            enum = data["slides"][slide_number - 1]["enumeration"][i]
            enum_phrases = []
            for pt in enum[1:]:
                styled_phrases = generate_random_phrases(pt)
                enum_phrases.append(styled_phrases)
            
            if len(enum) > 6:
                enum = enum[:6]

            enum_instance = {
            "label": "enumeration",
            "value": enum[1:] if hasHeading else enum,
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
                "v_align": 'top',
                "phrases": enum_phrases
               }
            }
            if (hasHeading):
                enum_instance['heading'] = {
                "label": 'heading',
                "value": enum[0],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'],
                "width": all_dims['body'][element_index]['width'],
                "height": 0.5,
                "style": {
                    "font_name": desc_font_family,
                    "font_size": desc_font_attr["font_size"] + random.randint(0, 2),
                    "font_color": font_color,
                    "bold": random.random() > 0.5,
                    "italics": font_obj["italics"],
                    "underlined": random.random() > 0.5
                }
                }
            
            slide['elements']['text'].append(enum_instance)
            element_index += 1


        #Render URLs
        h_url_align, v_url_align = ['left', 'center']
        slide['elements']['refs'] = []
        for _ in range(1):
            font_obj = generate_random_font("url")
            desc = data["slides"][slide_number - 1]["url"]
            prefix = ""
            if desc != "" and random.random() > 0.5:
                prefix = modify_url_prefix(desc)
            desc_instance = {
            "label": "url",
            "value": prefix + desc,
            "xmin": 0.5 if random.random() > 0.5 else 5*1.333,
            "ymin": 6.5 if random.random() > 0.5 else 1.5,
            "width": 4.5*1.333,
            "height": 0.5,
            "style": {
                "font_name": desc_font_family,
                "font_size": font_obj['font_size'],
                "font_color": {"r": 0, "g": 0, "b": 238} if random.random() > 0.75 else url_font_color,
                "bold": False,
                "italics": True,
                "underlined": True,
                "h_align": h_url_align,
                "v_align": v_url_align
               }
            } 
            slide['elements']['refs'].append(desc_instance)
       
        # Render Equations
        P_E = 0.25
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
        P_T = 0.5
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
            
            tab_instance = {**tab_instance, **{
            "label": "table",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": ele_ymin,
            "width": all_dims['body'][element_index]['width'],
            "height": ele_height,
            "desc": data["slides"][slide_number - 1]["tables"][i]["desc"]
            }}
            
            if 'path' in data["slides"][slide_number - 1]["tables"][i].keys():
                tab_instance['path'] = data["slides"][slide_number - 1]["tables"][i]['path']
            elif 'content' in data["slides"][slide_number - 1]['tables'][i]:
                tab_instance['content'] = data["slides"][slide_number - 1]['tables'][i]['content']
                   
          
            
            slide['elements']['tables'].append(tab_instance)
            element_index += 1
            remove_tmp_files()

        # Render Figures
        P_F = 0.5
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
                # check if caption is long
                caption_value = data["slides"][slide_number - 1]["figures"][i]["desc"]
                long_caption = len(caption_value) > 8
                
                ele_height =  all_dims['body'][element_index]['height'] - 0.35
                if random.random() > 0.5:
                # Caption below the visual element
                    cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.35 
                else:
                    # Caption above the visual element
                    # if caption is long, add more space
                    if long_caption:
                        ele_ymin = all_dims['body'][element_index]['top'] + 0.55
                        cap_ymin = all_dims['body'][element_index]['top']
                    else:
                        ele_ymin = all_dims['body'][element_index]['top'] + 0.35
                        cap_ymin = all_dims['body'][element_index]['top']
                
                
                fig_instance["caption"] = {
                    "label": "figure_caption",
                    "value": caption_value,
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
                "font_color": font_color if random.random() > 0.25 else url_font_color ,
                "bold": random.random() > 0.5,
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
        if 'affiliation' in obj.keys():
            footer_type = 'affiliation'
            value = style_obj["instructor"]
        if 'course_code' in obj.keys():
            footer_type = 'course_code'
            value = course_code
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
                    "font_size": random.randint(12, 22),
                    "font_color": font_color if random.random() > 0.5 else url_font_color,
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
            course_code = f'{subject} {random.randint(100, 300)}'
            for ver in range(DUP_FAC):
                style_obj = generate_random_style_obj()
                footer_obj = generate_footer_obj()
                all_slide = [insert_title_slide(data, style_obj, course_code)]
                slides = [generate_random_slide(i+1, data, style_obj, footer_obj, course_code, presentation_ID) for i in range(n_slides)]
                all_slide.extend(slides)
                new_data = {
                    "slide_id": presentation_ID,
                    "n_slides": len(slides),
                    "topic" : data["topic"],
                    "subject": subject,
                    "presenter": style_obj['instructor'],
                    "date": style_obj['date'],
                    "slides": all_slide
                }
                if not os.path.exists(f"code/buffer/full/{directory}"):
                    os.mkdir(f"code/buffer/full/{directory}")
                if not os.path.exists(f"code/buffer/full/{directory}/{presentation_ID}"):
                    os.mkdir(f"code/buffer/full/{directory}/{presentation_ID}")

                with open(f"code/buffer/full/{directory}/{presentation_ID}/{ver + 1}.json", 'w') as json_file:
                    json.dump(new_data, json_file, indent=3)

            print(f"🟢 ({i+1}/{n_json_files}): generated {DUP_FAC} layouts for {presentation_ID}")
    print('\n')

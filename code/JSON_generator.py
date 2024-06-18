import os
import random
import json
from layouts import CustomLayouts
import pandas as pd
import math
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
from utils.os_helpers import count_body_elements, count_footer_elements, remove_tmp_files, resize_image, get_line_height
from utils.corpus_paths import DIAGRAMS, CHARTS, TABLES, EQUATIONS, CODE_SNIPS

def insert_title_slide(data, style_obj, course_code):
    slide = {
        "pg_no": 0,
        "slide_layout": 0,
        "elements": {}
    }
    title_obj = generate_title_slide_obj()
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(0)
    path, logo_w, logo_h = pick_random_logo(1, 2, 2)
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
                "width": logo_w,
                "height": logo_h
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
    


def generate_random_slide(slide_number, data, style_obj, footer_obj, course_code, presentation_ID, url_df):
    n_slides = len(data["slides"])
    bg_color, title_font_family, title_font_bold, title_font_attr, title_align,\
          desc_font_family, desc_font_attr, date, tmp_list = style_obj["bg_color"], style_obj["title_font_family"],\
              style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj['title_align'], style_obj["desc_font_family"],\
                  style_obj["desc_font_attr"], style_obj["date"], style_obj["template"]
    tmp_path, isDark = tmp_list
    logo_path, logo_width, logo_height= style_obj['logo']
    url_font_color = style_obj['url_font_color']
    title_dark, title_light = style_obj['title_font_dark'], style_obj['title_font_light']
    if isDark == 1:
        title_font = title_light
        font_color = {"r": 255, "g": 255, "b": 254}
    else:
        title_font = title_dark
        font_color = {"r": 0, "g": 0, "b": 1}

    topic = data["topic"]
    if slide_number > n_slides:
        slide = {
             "pg_no": slide_number,
             "bg_color": bg_color,
             "slide_layout": 0,
             "elements": {}
        }
        slide['elements']["tables"] = []
        slide['elements']["equations"] = []
        slide['elements']["figures"] = []
        slide['elements']["code"] = []
        slide['elements']["text"] = []
        layout_id = 1 if random.random() > 0.75 else 2
        layouts = CustomLayouts()
        all_dims = layouts.get_layout_dimensions(layout_id)
        if layout_id % 2 == 0:
            title_value = data["slides"][random.randint(1, 15) - 1]["title"]
            slide['elements']['title'] = [{
                    "label": "title",
                    "value": title_value,
                    "xmin": all_dims['title']['left'],
                    "ymin": all_dims['title']['top'],
                    "width": all_dims['title']['width'],
                    "height": all_dims['title']['height'],
                    "style": {
                        "font_name": title_font_family,
                        "font_size": title_font_attr["font_size"],
                        "font_color": title_dark,
                        "bold": title_font_bold,
                        "italics": random.random() > 0.85,
                        "underlined": random.random() > 0.75,
                        "h_align": title_align,
                        "v_align": random.choice(['top', 'middle', 'bottom'])
                    }
                }]
        rand_element = pick_random(['code', 'chart', 'diagram', 'table', 'equation', 'enumeration'])
        # rand_element = pick_random(['enumeration'])
        pos = 0
        if rand_element == 'enumeration':
            for slide_obj in data["slides"]:
                if slide_obj["enumeration"] != [] and slide_obj["slide_number"] > pos:
                    pts = slide_obj["enumeration"][0]
                    pos = slide_obj["slide_number"]
                    break
            brk_ind = random.randint(0, len(pts) - 2) if len(pts) > 2 else 0
            font_obj = generate_random_font("description")
            for i, pt in enumerate(pts):
                 pts[i] = ' '.join(pts[i].split()[:5])
            enum_instance = {
            "label": "enumeration",
            "value": pts,
            "xmin": all_dims['body'][0]['left'],
            "ymin": all_dims['body'][0]['top'],
            "width": all_dims['body'][0]['width'],
            "height": max(all_dims['body'][0]['height'], 0.5*len(pts)),
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": font_obj["bold"],
                "italics": font_obj["italics"],
                "underlined": font_obj["underline"],
                "h_align": 'left',
                "v_align": 'top',
               }
            }
            slide['elements']['text'].append(enum_instance) 
            # rand_element = pick_random(['code'])
            rand_element = pick_random(['code', 'chart', 'diagram', 'equation', 'table'])

        file_path = ""
        img_path = ""
        if rand_element == 'code':
            file_path = pick_random(CODE_SNIPS)

        elif rand_element == 'chart':
            img_path = pick_random(CHARTS)
            
        elif rand_element == 'diagram':
            img_path = pick_random(DIAGRAMS)

        elif rand_element == 'equation':
            img_path = pick_random(EQUATIONS)

        elif rand_element == 'table':
            img_path = pick_random(TABLES)

        img_instance = {}
        code_instance = {}
                        
        if(len(slide["elements"]["text"]) > 0):
            enum_font = slide['elements']['text'][0]["style"]
            l_h = get_line_height(enum_font["font_name"], enum_font["font_size"])
            img_top = all_dims['body'][0]['top'] + (0.0139*(1 + brk_ind)*l_h)
            if img_path != "":
                if rand_element == 'equation':
                    m_w = 5
                    m_h = 1.5
                else:
                    m_w = 5
                    m_h = 3
                resized_img_path, n_w, n_h = resize_image(img_path, m_w, m_h)
                num_of_brks = math.ceil((n_h*72)/l_h)
                pts[brk_ind] = pts[brk_ind] + '\n'*num_of_brks
                img_instance = {
                    "label": rand_element,
                    "xmin": random.randint(1, 4) - (n_w - 6)/2,
                    "ymin": img_top,
                    "width": n_w,
                    "height": n_h,
                    "path": resized_img_path
                    }
            elif file_path != "":
                with open(file_path, 'r') as f:
                    content = f.read()
                code_lines = content.split('\n')
                code_lines = code_lines[:5]
                cl_h = get_line_height('Courier New', 14)
                num_of_brks = math.ceil((cl_h*5)/l_h)
                pts[brk_ind] = pts[brk_ind] + '\n'*num_of_brks
                slide["elements"]["code"] = [{
                    "label": "code",
                    "value": code_lines,
                    "xmin": random.randint(1, 2),
                    "ymin": img_top,
                    "width": 5,
                    "height": 0.0139*cl_h*5 + 0.1,
                    "style": {
                     "font_name": "Courier New",
                     "font_size": 14,
                     "font_color": {
                        "r": 0,
                        "g": 0,
                        "b": 1
                     },
                     "bold": False,
                     "italics": False,
                     "underlined": False,
                     "h_align": "left",
                     "v_align": "top"
                  }
                }]
        else:
            if img_path != "":
                resized_img_path, n_w, n_h = resize_image(img_path, all_dims['body'][0]['width'], all_dims['body'][0]['height'])
                img_instance = {
                    "label": rand_element,
                    "xmin": all_dims['body'][0]['left'] - (n_w - all_dims['body'][0]['width'])/2,
                    "ymin": all_dims['body'][0]['top'] - (n_h - all_dims['body'][0]['height'])/2,
                    "width": n_w,
                    "height": n_h,
                    "path": resized_img_path
                }
            elif file_path != "":
                with open(file_path, 'r') as f:
                    code_snip = f.read()
                code_lines = code_snip.split('\n')
                code_lines = code_lines[:15]
                slide["elements"]["code"] = [{
                    "label": "code",
                    "value": code_lines,
                    "xmin": all_dims['body'][0]['left'],
                    "ymin": all_dims['body'][0]['top'],
                    "width": all_dims['body'][0]['width'],
                    "height": all_dims['body'][0]['height'],
                    "style": {
                     "font_name": "Courier New",
                     "font_size": 14,
                     "font_color": {
                        "r": 0,
                        "g": 0,
                        "b": 1
                     },
                     "bold": False,
                     "italics": False,
                     "underlined": False,
                     "h_align": "left",
                     "v_align": "top"
                  }
                }]
        if img_instance != {}:
            if rand_element == 'chart' or rand_element == 'diagram':
                ele_type = 'figures'
            elif rand_element == 'table':
                ele_type = 'tables'
            elif rand_element == 'equation':
                ele_type = 'equations'
            slide['elements'][ele_type].append(img_instance)
    else:
        n_elements_list = count_body_elements(data, slide_number)
        total_body_elements = sum(n_elements_list)
        # Title Generation
        ## Generate Font-level random values for Title
        if(tmp_path != ''):
            if isDark == 0:
                title_font = title_dark
                font_color = {"r": 0, "g": 0, "b": 1}
            elif isDark == 1:
                title_font = title_light
                font_color = {"r": 255, "g": 255, "b": 254}
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
        
        if logo_path != '' and layout_id % 2 == 0:
            # if title_align is left, then the logo should not be on the top left side, i.e. left = 0.25 and top = 0.25
            # if title_align is right, then the logo should not be on the top right side, i.e. left = 12.083 and top = 0.25
            # any other alignment, the logo can be anywhere
            while True:
                bbox_logo = random_logo_pos(footer_obj)
                if bbox_logo["top"] == 0.25:
                    if bbox_logo["left"] == 0.25 and title_align == 'left':
                        continue
                    if bbox_logo["left"] == 12.083 and title_align == 'right':
                        continue
                break
            
            slide["elements"]["graphic"] = [{
                "label": "logo",
                "value": logo_path,
                "xmin": bbox_logo['left'],
                "ymin": bbox_logo['top'],
                "width": logo_width,
                "height": logo_height,
            }]

        ## Putting it together for the title object
        if len(all_dims['title']) != 0:
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
                        "italics": random.random() > 0.85,
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
                n_words = len(desc.split())
                if n_words < 15 and random.random() > 0:
                    desc = desc + ' ' + desc
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
                    "font_color": {"r": 0, "g": 0, "b": 1},
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
            P_H = 0.33
            hasHeading = P_H > random.random()
            h_enum_align, v_enum_align = pick_random("alignments")
            for i in range(n_elements_list[1]):
                font_obj = generate_random_font("enumeration")
                enum = data["slides"][slide_number - 1]["enumeration"][i]
                enum_phrases = []
                for pt in enum[1:]:
                    styled_phrases = generate_random_phrases(pt)
                    enum_phrases.append(styled_phrases)

                enum_instance = {}       
                # code for row oriented enumeration is left
                if (hasHeading):
                    # Limit the heading to 3 words if column oriented
                    heading_words = enum[0].split()
                    if len(heading_words) > 3:
                        heading_content = ' '.join(heading_words[:3])
                    else:
                        heading_content = ' '.join(heading_words)
                        
                    enum_instance['heading'] = {
                    "label": 'heading',
                    "value": heading_content,
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
                
                # below works for column oriented enumeration,
                # for row oriented enumeration, size and no of points should be reduced
                enum = enum[1:]
                if len(enum) > 4:
                    enum = enum[:4]
                    # count the number of words in the first 5 elements
                    n_words = sum([len(e.split()) for e in enum])
                    # if the number of words is greater than 12, then remove the last element
                    if n_words > 12:
                        enum = enum[:-1]
                if len(enum) > 3:
                    if desc_font_attr["font_size"] >= 24:
                        enum = enum[:3]


                if len(enum) > 2:
                    if all_dims['body'][element_index]['type'] == 4 or all_dims['body'][element_index]['type'] == 2:
                        enum = enum[:2]
        
                        
                enum_instance = {**enum_instance, **{
                "label": "enumeration",
                "value": enum,
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
                }}
                
                slide['elements']['text'].append(enum_instance)
                element_index += 1


            #Render URLs
            h_url_align, v_url_align = ['left', 'center']
            slide['elements']['refs'] = []
            for _ in range(1):
                font_obj = generate_random_font("url")
                desc = data["slides"][slide_number - 1]["url"]
                prefix = ""
                if desc != "":
                    # prefix = modify_url_prefix(desc)
                    # url_value = prefix + desc
                    random_url_inst = url_df.sample(n=1)
                    url_value = random_url_inst['URL'].values[0]
                    url_value = url_value[:60]
                    if url_value == "":
                        break
                    desc_instance = {
                    "label": "url",
                    "value": url_value,
                    "xmin": 0.5 if random.random() > 0.5 else 5*1.333,
                    "ymin": 1.5,
                    "width": 4.5*1.333,
                    "height": 0.75,
                    "style": {
                        "font_name": desc_font_family,
                        "font_size": font_obj['font_size'],
                        "font_color": {"r": 0, "g": 0, "b": 225}, # if random.random() > 0.75 else url_font_color,
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
                # img_path = data["slides"][slide_number - 1]["equations"][i]["path"]
                img_path = pick_random(EQUATIONS)
                resized_img_path, n_w, n_h = resize_image(img_path, all_dims['body'][element_index]['width'], ele_height)
                if (P_E > random.random()):
                    # take only the first 6 words of the description
                    caption_value = data["slides"][slide_number - 1]["equations"][i]["desc"]
                    # take only the first 6 words of the description
                    caption_value = ' '.join(caption_value.split()[:7])
                    ele_height =all_dims['body'][element_index]['height'] - 0.45 
                    if random.random() > 0.5:
                    # Caption below the visual element
                        cap_ymin = all_dims['body'][element_index]['top'] + ele_height - 0.35 + (n_h - ele_height)/2
                        ele_ymin = all_dims['body'][element_index]['top']
                    else:
                        # Caption above the visual element
                        ele_ymin = all_dims['body'][element_index]['top'] + 0.45
                        cap_ymin = all_dims['body'][element_index]['top'] - (n_h - ele_height)/2
                    eq_instance["caption"] = {
                        "label": "equation_caption",
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
                
                eq_instance = {**eq_instance, **{
                "label": "equation",
                "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
                "ymin": ele_ymin - (n_h - ele_height)/2,
                "width": n_w,
                "height": n_h,
                "desc": data["slides"][slide_number - 1]["equations"][i]["desc"],
                "path": resized_img_path
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
                n_w = all_dims['body'][element_index]['width']
                n_h = ele_height

                if 'path' in data["slides"][slide_number - 1]["tables"][i].keys():
                    # img_path = data["slides"][slide_number - 1]["tables"][i]['path']
                    img_path = pick_random(TABLES)
                    resized_img_path, n_w, n_h = resize_image(img_path, all_dims['body'][element_index]['width'], ele_height)
                    tab_instance['path'] = resized_img_path
                elif 'content' in data["slides"][slide_number - 1]['tables'][i]:
                    tab_instance['content'] = data["slides"][slide_number - 1]['tables'][i]['content']
                if (P_T > random.random()):
                    # take only the first 6 words of the description
                    caption_value = data["slides"][slide_number - 1]["tables"][i]["desc"]
                    # take only the first 6 words of the description
                    caption_value = ' '.join(caption_value.split()[1:7])
                    ele_height = all_dims['body'][element_index]['height'] - 0.45 
                    if random.random() > 0.5:
                    # Caption below the visual element
                        cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.45 + (n_h - ele_height)/2
                        ele_ymin = all_dims['body'][element_index]['top']
                    else:
                        # Caption above the visual element
                        ele_ymin = all_dims['body'][element_index]['top'] + 0.45
                        cap_ymin = all_dims['body'][element_index]['top'] - (n_h - ele_height)/2
                    tab_instance["caption"] = {
                        "label": "table_caption",
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

                
                
                tab_instance = {**tab_instance, **{
                "label": "table",
                "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
                "ymin": ele_ymin - (n_h - ele_height)/2,
                "width": n_w,
                "height": n_h,
                "desc": data["slides"][slide_number - 1]["tables"][i]["desc"]
                }}
                
                
                
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
                # img_path = data["slides"][slide_number - 1]["figures"][i]['path']
                label = data["slides"][slide_number - 1]["figures"][i]['label']
                if(label == 'pie-chart' or label == 'line-chart' or label == 'bar-chart' or label == 'plot' or label == '3d-plot'):
                    img_path = pick_random(CHARTS)
                else:
                    img_path = pick_random(DIAGRAMS)
                ele_ymin = all_dims['body'][element_index]['top']
                ele_height =  all_dims['body'][element_index]['height']
                resized_img_path, n_w, n_h = resize_image(img_path, all_dims['body'][element_index]['width'], ele_height)
                if (P_F > random.random()):
                    # take only the first 6 words of the description
                    caption_value = data["slides"][slide_number - 1]["figures"][i]["desc"]
                    # take only the first 6 words of the description
                    caption_value = ' '.join(caption_value.split()[:7])
                    ele_height =  all_dims['body'][element_index]['height'] - 0.45
                    if random.random() > 0.5:
                    # Caption below the visual element
                        cap_ymin = all_dims['body'][element_index]['top'] + all_dims['body'][element_index]['height'] - 0.35 + (n_h - ele_height)/2
                        ele_ymin = all_dims['body'][element_index]['top']
                    else:
                        ele_ymin = all_dims['body'][element_index]['top'] + 0.45
                        cap_ymin = all_dims['body'][element_index]['top'] - (n_h - ele_height)/2
                    
                    
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
                fig_instance = {**fig_instance, **{
                "label": label,
                "xmin": all_dims['body'][element_index]['left'] - (n_w - all_dims['body'][element_index]['width'])/2,
                "ymin": ele_ymin - (n_h - ele_height)/2,
                "width": n_w,
                "height": n_h,
                "desc": data["slides"][slide_number - 1]["figures"][i]["desc"],
                "path": resized_img_path
                }}

                slide['elements']['figures'].append(fig_instance)
                element_index += 1
                remove_tmp_files()
        
            slide['elements']['code'] = []
            for i in range(n_elements_list[6]):
                font_obj = generate_random_font("url")
                # value = data["slides"][slide_number - 1]["code"][i]['value']
                random_code_snip = pick_random(CODE_SNIPS)
                with open(random_code_snip, 'r') as file:
                    value = file.read()
                codelines = value.split('\n')
                if all_dims['body'][element_index]['type'] == 1:
                    codelines = codelines[:15]
                elif all_dims['body'][element_index]['type'] == 3:
                    codelines = codelines[:10]
                elif all_dims['body'][element_index]['type'] == 2:
                    codelines = codelines[:7]
                else:
                    codelines = codelines[:4]

                caption = data["slides"][slide_number - 1]["code"][i]['desc']
                code_instance = {
                "label": "code",
                "desc": caption,
                "value": codelines,
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
    url_df = pd.read_csv('code\\buffer\\corpus\\urls.csv')
    entries = os.listdir(temp_dir)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(temp_dir, entry))]

    DUP_FAC = 2
    for directory in directories:
        json_files = [f for f in os.listdir(os.path.join(temp_dir,directory)) if f.endswith('.json')][:25]
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
                slides = [generate_random_slide(i+1, data, style_obj, footer_obj, course_code, presentation_ID, url_df) for i in range(n_slides + 5)]
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

            print(f"🟢 ({i+1}/{n_json_files}): generated {DUP_FAC} layouts for {subject}/{presentation_ID}")
    print('\n')

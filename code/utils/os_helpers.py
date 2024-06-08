from PIL import Image
import os
import random 

def resize_image(input_image_path, box_width, box_height):
        dpi = 96
        box_width_pixels = int(box_width) * dpi
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
            # img_name = os.path.basename(input_image_path)
            img_dir = os.path.dirname(input_image_path)
            new_img_dir = os.path.join('code/buffer', 'temp')
            if not os.path.exists(new_img_dir):
                 os.mkdir(new_img_dir)            
            new_img_path = os.path.join(new_img_dir, f'{hex(random.randint(0x100000, 0xFFFFFF))[2:]}.png')
            resized_img.save(new_img_path)
            # os.remove(input_image_path)
            new_width_inches = new_width / dpi
            new_height_inches = new_height / dpi
            return new_img_path, new_width_inches, new_height_inches
        

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
    ttl_img = 0
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
        elif k =='images' and v:
            ttl_img = len(v)
    # return [ttl_desc, ttl_enum, ttl_url, ttl_eq, ttl_tb, ttl_fig, ttl_cd]
    return [ttl_desc, ttl_enum, 0, ttl_eq, ttl_tb, ttl_fig, ttl_cd, ttl_img]

def remove_tmp_files():
    tmp_files = ['tmp.tex', 'tmp.aux', 'tmp.log', 'tmp.pdf']
    for f in tmp_files:
        if os.path.exists(f):
            os.remove(f)
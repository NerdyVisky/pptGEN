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
            new_img_dir = f"code/buffer/temp"
            if not os.path.exists(new_img_dir):
                 os.mkdir(new_img_dir)            
            new_img_path = f"{new_img_dir}/{hex(random.randint(0x100000, 0xFFFFFF))[2:]}.png"
            resized_img.save(new_img_path)
            # os.remove(input_image_path)
            new_width_inches = new_width / dpi
            new_height_inches = new_height / dpi
            return new_img_path, new_width_inches, new_height_inches
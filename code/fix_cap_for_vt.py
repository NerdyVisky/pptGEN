import cv2
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches 

def correct_element_annotations(annotations, image, bg_color):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = annotations["xmin"] + annotations["width"]
    ymax = annotations["ymin"] + annotations["height"]
    
    # Convert bg_color to numpy array for comparison
    bg_color = np.array([bg_color['b'], bg_color['g'], bg_color['r']])

    # Ensure the coordinates are within the image boundaries
    image_height, image_width = image.shape[:2]

    while ymin < ymax and np.all(image[ymin, xmin:xmax] == bg_color):
        ymin += 1
    while ymax > ymin and np.all(image[ymax - 1, xmin:xmax] == bg_color):
        ymax -= 1
    while xmin < xmax and np.all(image[ymin:ymax, xmin] == bg_color):
        xmin += 1
    while xmax > xmin and np.all(image[ymin:ymax, xmax - 1] == bg_color):
        xmax -= 1

    new_annotations = {
        "label": annotations["label"],
        "xmin": xmin,
        "ymin": ymin,
        "width": xmax - xmin,
        "height": ymax - ymin
    }
    if xmin == xmax or ymin == ymax:
      return annotations
    return new_annotations

def correction():
    a = 0
    json_path = f"dataset/json/"
    for subject in os.listdir(json_path):
        for topic in os.listdir(json_path + subject):
            for json_file in os.listdir(f"{json_path}{subject}/{topic}"):
                if json_file.endswith(".json"):
                    folder_name = f"dataset/images/{subject}/{topic}/{json_file.split(".")[0]}"
                    with open(f"code/json/final/{subject}/{topic}/{json_file}") as f:
                        data = json.load(f)
                        i = 1
                        for slide in data["slides"]:
                            # print(slide["pg_no"])
                            img_path = f"{folder_name}/slide{i}.png"
                            image = cv2.imread(img_path)
                            i += 1
                            # print(img_path)
                            
                            elements = slide["elements"]
                            bg_color = slide["bg_color"]
                            
                            for element_type, element_list in elements.items():
                                for items in element_list:
                                    if element_type == 'figures' and items["caption"]["height"] == 0:
                                        avg_width = 491
                                        avg_height = 27
                                        new_annotations["xmin"] = int(items["xmin"] + ( items["width"] / 2 ) - ( avg_width / 2 ))
                                        new_annotations["ymin"] = items["ymin"] + items["height"] - avg_height
                                        new_annotations["width"] = avg_width
                                        new_annotations["height"] = avg_height
                                        new_annotations = correct_element_annotations(new_annotations, image, bg_color)
                                        items["caption"]["xmin"] = new_annotations["xmin"]
                                        items["caption"]["ymin"] = new_annotations["ymin"]
                                        items["caption"]["width"] = new_annotations["width"]
                                        items["caption"]["height"] = new_annotations["height"]
                                        items["caption"]["label"] = "caption"
                            
                            
                                if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
                                    os.makedirs(f"dataset/json/{subject}/{topic}/")
                                with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
                                    json.dump(data, f, indent=3)
                a += 1
    print(f"🟢 (3/5) Annotations corrected for {a} presentations.")

if __name__ == "__main__":
  correction()
import cv2
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches 

def get_element_annotations(element):
    slide_width = 13.333
    slide_height = 7.50
    
    label = element["label"]
    xmin = element.get("xmin", 0)
    ymin = element.get("ymin", 0)
    width = element.get("width", 0)
    height = element.get("height", 0)
    
    normalized_bbox = {
        "label": label,
        "xmin": int(xmin / slide_width * 1280),
        "ymin": int(ymin / slide_height * 720),
        "width": int(width / slide_width * 1280),
        "height": int(height / slide_height * 720)
    }
    return normalized_bbox

def correct_element_annotations(annotations, image, bg_color):
  xmin = annotations["xmin"]
  ymin = annotations["ymin"]
  xmax = annotations["xmin"] + annotations["width"]
  ymax = annotations["ymin"] + annotations["height"]

  bg_color = np.array([bg_color['b'], bg_color['g'], bg_color['r']])
  
  while True:
    if not np.all(image[ymin, xmin:xmax] == bg_color):
      break
    ymin += 1
  while True:
    if not np.all(image[ymax - 1, xmin:xmax] == bg_color):
      break
    ymax -= 1
  while True:
    if not np.all(image[ymin:ymax, xmin] == bg_color):
      break
    xmin += 1
  while True:
    if not np.all(image[ymin:ymax, xmax - 1] == bg_color):
      break
    xmax -= 1
  new_annotations = {
    "label": annotations["label"],
    "xmin": xmin,
    "ymin": ymin,
    "width": xmax - xmin,
    "height": ymax - ymin
  }
  return new_annotations

def correction():
  json_path = "dataset/json/"
  for json_file in os.listdir(json_path):
    if json_file.endswith(".json"):
      folder_name = json_file.split(".")[0]
      with open(f"dataset/json/{json_file}") as f:
        data = json.load(f)
  
        i = 1
        for slide in data["slides"][1:]:
          print(slide["pg_no"])
          img_path = f"dataset/images/{folder_name}/slide{i}.png"
          image = cv2.imread(img_path)
          
          elements = ['title', 'textural' 'figures','footer']
          bg_color = slide["bg_color"]
          
          for element_type in elements:
            if element_type in slide["elements"]:
              elements = slide["elements"][element_type]
              for item in elements:
                annotations = get_element_annotations(item)
                updated_annotations = correct_element_annotations(annotations, image, bg_color)
                print(annotations)
                print(updated_annotations)
                item["xmin"] = updated_annotations["xmin"]
                item["ymin"] = updated_annotations["ymin"]
                item["width"] = updated_annotations["width"]
                item["height"] = updated_annotations["height"]
                with open(f"dataset/json/updated/{json_file}", "w") as f:
                  json.dump(data, f, indent=3)
        i += 1

def show_annotations(filename):
    with open(f"dataset/json/{filename}.json", "r") as f:
        data = json.load(f)
    images = []
    i = 2
    for slide in data["slides"][1:]:
        img_path = f"dataset/images/{filename}/slide{i}.png"
        image = cv2.imread(img_path)
        bg_color = slide["bg_color"]
        i += 1

        for element_type in ['title', 'description', 'url', 'equations','tables','figures','footer']:
          if element_type == 'description' and "description" in slide["elements"]:
            desc = slide["elements"][element_type]
            for item in desc:
              annotations = get_element_annotations(item)
              new_annotations = correct_element_annotations(annotations, image, bg_color)          
              cv2.rectangle(image, (new_annotations["xmin"], new_annotations["ymin"]), (new_annotations["xmin"] + new_annotations["width"], new_annotations["ymin"] + new_annotations["height"]), (0, 255, 0), 2)
          elif element_type == 'figures' and "figures" in slide["elements"]:
            figs = slide["elements"][element_type]
            for item in figs:
              annotations = get_element_annotations(item) 
              new_annotations = correct_element_annotations(annotations, image, bg_color)
              cv2.rectangle(image, (new_annotations["xmin"], new_annotations["ymin"]), (new_annotations["xmin"] + new_annotations["width"], new_annotations["ymin"] + new_annotations["height"]), (255, 0, 0), 2)
              annotations = get_element_annotations(item["caption"]) 
              new_annotations = correct_element_annotations(annotations, image, bg_color)
              cv2.rectangle(image, (new_annotations["xmin"], new_annotations["ymin"]), (new_annotations["xmin"] + new_annotations["width"], new_annotations["ymin"] + new_annotations["height"]), (0, 0, 255), 2)
          elif element_type in slide["elements"]:
            elements = slide["elements"][element_type]
            for item in elements:
              annotations = get_element_annotations(item) 
              new_annotations = correct_element_annotations(annotations, image, bg_color)
              cv2.rectangle(image, (new_annotations["xmin"], new_annotations["ymin"]), (new_annotations["xmin"] + new_annotations["width"], new_annotations["ymin"] + new_annotations["height"]), (0, 0, 0), 2)
        
        # image.save(f"dataset/images/annotations/{filename}/slide{i - 1}_bbox.png")

        images.append(image)
    
    num_images = len(images)
    num_batches = (num_images + 3) // 4

    for batch in range(num_batches):
        start_index = batch * 4
        end_index = min(start_index + 4, num_images)
        rows, cols = (2, min(2, end_index - start_index))
        fig, axes = plt.subplots(rows, cols, figsize=(8, 8))

        for i in range(start_index, end_index):
            image = images[i]
            h, w, _ = image.shape
            border_rect = patches.Rectangle(xy=(0, 0),
                                            width=w, height=h,
                                            color='black',
                                            linewidth=2,
                                            fill=False)
            axes.flat[i - start_index].add_patch(border_rect)
            axes.flat[i - start_index].imshow(image)
            axes.flat[i - start_index].axis('off')

        plt.tight_layout()
        plt.show()

def main():
  correction()
  # show_annotations("15001")

if __name__ == "__main__":
  main()
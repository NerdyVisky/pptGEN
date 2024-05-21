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

    xmin = element.get("xmin", 0)
    ymin = element.get("ymin", 0)
    width = element.get("width", 0)
    height = element.get("height", 0)
    
    normalized_bbox = {
        "label": element.get("label"),
        "xmin": int(xmin / slide_width * 1280),
        "ymin": int(ymin / slide_height * 720),
        "width": int(width / slide_width * 1280),
        "height": int(height / slide_height * 720)
    }
    return normalized_bbox

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
    
    return new_annotations

def correction():
  json_path = "code/json/final/"
  for subject in os.listdir(json_path):
    for topic in os.listdir(json_path + subject):
      for json_file in os.listdir(json_path + subject + '/' + topic):
        if json_file.endswith(".json"):
          folder_name = 'dataset/images/' + subject + '/' + topic + '/' + json_file.split(".")[0]
          with open(f"code/json/final/{subject}/{topic}/{json_file}") as f:
            data = json.load(f)

            i = 1
            for slide in data["slides"]:
              img_path = f"{folder_name}/slide{i}.png"
              image = cv2.imread(img_path)
              i += 1              
              elements = slide["elements"]
              bg_color = slide["bg_color"]

              for element_type, element_list in elements.items():
                for items in element_list:
                  if element_type == 'description':
                    if items["label"] == 'text':
                      annotations = get_element_annotations(items)
                      new_annotations = correct_element_annotations(annotations, image, bg_color)
                      items["xmin"] = new_annotations["xmin"]
                      items["ymin"] = new_annotations["ymin"]
                      items["width"] = new_annotations["width"]
                      items["height"] = new_annotations["height"]
                      items["label"] = new_annotations["label"]
                    else:
                      annotations["xmin"] = items["heading"]["xmin"]
                      annotations["ymin"] = items["heading"]["ymin"]
                      annotations["width"] = items["heading"]["width"]
                      annotations["height"] = items["heading"]["height"] + items["height"]
                      annotations["label"] = items["label"]
                      annotations1 = get_element_annotations(annotations)
                      new_annotations = correct_element_annotations(annotations1, image, bg_color)
                      items["xmin"] = new_annotations["xmin"]
                      items["ymin"] = new_annotations["ymin"]
                      items["width"] = new_annotations["width"]
                      items["height"] = new_annotations["height"]
                      items["label"] = new_annotations["label"]
                  elif element_type == 'figures':
                    annotations = get_element_annotations(items["caption"])
                    new_annotations = correct_element_annotations(annotations, image, bg_color)
                    items["caption"]["xmin"] = new_annotations["xmin"]
                    items["caption"]["ymin"] = new_annotations["ymin"]
                    items["caption"]["width"] = new_annotations["width"]
                    items["caption"]["height"] = new_annotations["height"]
                    items["caption"]["label"] = "caption"
                    annotations = get_element_annotations(items)
                    new_annotations = correct_element_annotations(annotations, image, bg_color)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    items["label"] = new_annotations["label"]
                  else:
                    annotations = get_element_annotations(items)
                    new_annotations = correct_element_annotations(annotations, image, bg_color)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    items["label"] = new_annotations["label"]
              
              # for element_type, element_list in elements.items():
              #   for items in element_list:
              #     if element_type == 'title' or element_type == 'equations' or element_type == 'tables' or element_type == 'footer':
              #       annotations = get_element_annotations(items)
              #       new_annotations = correct_element_annotations(annotations, image, bg_color)
              #       items["xmin"] = new_annotations["xmin"]
              #       items["ymin"] = new_annotations["ymin"]
              #       items["width"] = new_annotations["width"]
              #       items["height"] = new_annotations["height"]
              #       items["label"] = new_annotations["label"]
              #     if element_type == 'description':
              #       if items["label"] == 'text':
              #         annotations = get_element_annotations(items)
              #         new_annotations = correct_element_annotations(annotations, image, bg_color)
              #         items["xmin"] = new_annotations["xmin"]
              #         items["ymin"] = new_annotations["ymin"]
              #         items["width"] = new_annotations["width"]
              #         items["height"] = new_annotations["height"]
              #         items["label"] = new_annotations["label"]
              #       else:
              #         annotations["xmin"] = items["heading"]["xmin"]
              #         annotations["ymin"] = items["heading"]["ymin"]
              #         annotations["width"] = items["heading"]["width"]
              #         annotations["height"] = items["heading"]["height"] + items["height"]
              #         annotations["label"] = items["label"]
              #         annotations1 = get_element_annotations(annotations)
              #         new_annotations = correct_element_annotations(annotations1, image, bg_color)
              #         items["xmin"] = new_annotations["xmin"]
              #         items["ymin"] = new_annotations["ymin"]
              #         items["width"] = new_annotations["width"]
              #         items["height"] = new_annotations["height"]
              #         items["label"] = new_annotations["label"]
              #     if element_type == 'url':
              #       annotations = get_element_annotations(items)
              #       new_annotations = correct_element_annotations(annotations, image, bg_color)
              #       items["xmin"] = new_annotations["xmin"]
              #       items["ymin"] = new_annotations["ymin"]
              #       items["width"] = new_annotations["width"]
              #       items["height"] = new_annotations["height"]
              #       items["label"] = "url"
              #     if element_type == 'figures':
              #       annotations = get_element_annotations(items["caption"])
              #       new_annotations = correct_element_annotations(annotations, image, bg_color)
              #       items["caption"]["xmin"] = new_annotations["xmin"]
              #       items["caption"]["ymin"] = new_annotations["ymin"]
              #       items["caption"]["width"] = new_annotations["width"]
              #       items["caption"]["height"] = new_annotations["height"]
              #       items["caption"]["label"] = "caption"
              #       annotations = get_element_annotations(items)
              #       new_annotations = correct_element_annotations(annotations, image, bg_color)
              #       items["xmin"] = new_annotations["xmin"]
              #       items["ymin"] = new_annotations["ymin"]
              #       items["width"] = new_annotations["width"]
              #       items["height"] = new_annotations["height"]
              #       items["label"] = new_annotations["label"]
                    
                if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
                  os.makedirs(f"dataset/json/{subject}/{topic}/")
                with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
                  json.dump(data, f, indent=3)
              

def show_annotations(filename):
    with open(f"dataset/json/{filename}.json", "r") as f:
      data = json.load(f)
    images = []
    i = 1
    for slide in data["slides"]:
        img_path = f"dataset/images/{filename}/slide{i}.png"
        image = cv2.imread(img_path)
        i += 1
        elements = slide["elements"]
        
        for element_type, element_list in elements.items():
          for items in element_list:
            if element_type == 'figures':
              cv2.rectangle(image, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (0, 255, 0), 2)
            cv2.rectangle(image, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (0, 255, 0), 2)
        
        # save the annotated image
        # image.save(f"dataset/images/{filename}/slide{i}_bbox.png")
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
  # to correct Annotations
  correction()
  print(f"🟢 (4/5) JSON Annotations corrected and saved")
  # to show Annotations
  # for subject in os.listdir("dataset/json"):
  #   for topic in os.listdir(f"dataset/json/{subject}"):
  #     for json_file in os.listdir(f"dataset/json/{subject}/{topic}"):
  #       if json_file.endswith(".json"):
  #         show_annotations(f"{subject}/{topic}/{json_file.split('.')[0]}")
  #       break
  #     break

if __name__ == "__main__":
  main()
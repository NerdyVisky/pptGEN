import cv2
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches 

def get_pixel_values(element):
    slide_width = 13.333
    slide_height = 7.50

    # Get the bounding box coordinates
    xmin = element.get("xmin", 0)
    ymin = element.get("ymin", 0)
    width = element.get("width", 0)
    height = element.get("height", 0)
    
    # Get the label
    label = element.get("label")
    
    # Handle the case where the bounding box is outside the slide
    if xmin + width > slide_width:
        width = slide_width - xmin
    if ymin + height > slide_height:
        height = slide_height - ymin
    
    normalized_bbox = {
        "label": label,
        "xmin": int(xmin / slide_width * 1280),
        "ymin": int(ymin / slide_height * 720),
        "width": int(width / slide_width * 1280),
        "height": int(height / slide_height * 720),
    }    
    return normalized_bbox

def alter_bounding_box(image, xmin, ymin, xmax, ymax, font_color):
    image_width = image.shape[1]
    image_height = image.shape[0]

    # Clip coordinates to image boundaries
    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    print(xmin, ymin, xmax, ymax)
    
    found_top, found_bottom, found_left, found_right = False, False, False, False
    for x in range(xmin, xmax):
      if not found_top and np.any(image[ymin, x] == font_color):
        found_top = True
      if not found_bottom and np.any(image[ymax, x] == font_color):
        found_bottom = True
    for y in range(ymin, ymax):
      if not found_left and np.any(image[y, xmin] == font_color):
        found_left = True
      if not found_right and np.any(image[y, xmax] == font_color):
        found_right = True
        
    print(found_top, found_bottom, found_left, found_right)
    
    # Top
    new_ymin = ymin
    while not found_top and new_ymin > 0:
      new_ymin -= 1
      found_top = np.any(image[new_ymin, xmin:xmax] == font_color)
    # Bottom
    new_ymax = ymax
    while not found_bottom and new_ymax < image_height - 1:
      new_ymax += 1
      found_bottom = np.any(image[new_ymax, xmin:xmax] == font_color)
    # Left
    new_xmin = xmin
    while not found_left and new_xmin > 0:
      new_xmin -= 1
      found_left = np.any(image[ymin:ymax, new_xmin] == font_color)
    # Right
    new_xmax = xmax
    while not found_right and new_xmax < image_width - 1:
      new_xmax += 1
      found_right = np.any(image[ymin:ymax, new_xmax] == font_color)
    
    new_ymin = max(0, min(new_ymin, image_height - 1))
    new_ymax = max(0, min(new_ymax, image_height - 1))
    new_xmin = max(0, min(new_xmin, image_width - 1))
    new_xmax = max(0, min(new_xmax, image_width - 1))
    
    print(new_xmin, new_ymin, new_xmax, new_ymax) 
    
    return new_xmin, new_ymin, new_xmax, new_ymax


def correct_element_annotations_for_text(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = annotations["xmin"] + annotations["width"]
    ymax = annotations["ymin"] + annotations["height"]
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])
    
    # Alter the bounding box
    xmin_n, ymin_n, xmax_n, ymax_n = alter_bounding_box(image, xmin, ymin, xmax, ymax, target_color)
  
    if xmin_n == xmin and ymin_n == ymin and xmax_n == xmax and ymax_n == ymax:
        return annotations
  
    new_annotations = {
        "xmin": xmin_n,
        "ymin": ymin_n,
        "width": xmax_n - xmin_n,
        "height": ymax_n - ymin_n
    }
    print(annotations["label"], annotations["xmin"], annotations["ymin"], annotations["width"], annotations["height"])
    print(new_annotations)
    return new_annotations

def correction():
  a = 0
  json_path = f"dataset/json/"
  for subject in os.listdir(json_path):
    for topic in os.listdir(json_path + subject):
      for json_file in os.listdir(f"{json_path}{subject}/{topic}"):
        if json_file.endswith(".json"):
          file_name, _ = json_file.split(".")
          folder_name = f"dataset/images/{subject}/{topic}/{file_name}"
          print(folder_name)
          with open(f"{json_path}{subject}/{topic}/{json_file}") as f:
            data = json.load(f)
            print(data["slide_id"])

            i = 0
            for slide in data["slides"]:
              print(slide["pg_no"])
              if slide["pg_no"] <= 9:
                img_path = f"{folder_name}/0{i}{file_name}{topic}.png"
              else:
                img_path = f"{folder_name}/{i}{file_name}{topic}.png"
              print(img_path)
              image = cv2.imread(img_path)
              a += 1
              i += 1
              
              elements = slide["elements"]
              # correction needed for text:
              # title, footer, text enumeration, e_heading, refs, figure_caption, table_caption, equation_caption, 
              for element_type, element_list in elements.items():
                for items in element_list:
                  if element_type == 'footer' or element_type == 'refs' or element_type == 'title':
                    new_annotations = correct_element_annotations_for_text(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                  if element_type == 'text':
                    new_annotations = correct_element_annotations_for_text(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    if items["label"] == 'enumeration':
                      if 'heading' in items.keys():
                        new_annotations = correct_element_annotations_for_text(items["heading"], image)
                        items["heading"]["xmin"] = new_annotations["xmin"]
                        items["heading"]["ymin"] = new_annotations["ymin"]
                        items["heading"]["width"] = new_annotations["width"]
                        items["heading"]["height"] = new_annotations["height"]
                  if element_type == 'figures' or element_type == 'equations' or element_type == 'tables':  
                    if 'caption' in items.keys():
                      new_annotations = correct_element_annotations_for_text(items["caption"], image)
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                
                if element_type == 'figures' or element_type == 'tables' or element_type == 'equations':
                  if 'caption' in items.keys():
                    cv2.rectangle(image, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 2)
                if element_type == 'description' and items["label"] == 'enumeration':
                  if 'heading' in items.keys():  
                    cv2.rectangle(image, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 2)
                cv2.rectangle(image, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 2)
                
                # show the image
                cv2.imshow("image", image)
                
                if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
                  os.makedirs(f"dataset/json/{subject}/{topic}/")
                with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
                  json.dump(data, f, indent=3)
              # if a == 16:
              #   return
  print(f"🟢 (4/5) Annotations corrected for {a} images.")
              

def move_files():
  a = 0
  created_files = []
  for subject in os.listdir("dataset/json/"):
      for topic in os.listdir(f"dataset/json/{subject}"):
          created_files.append(topic)
  json_path = f"code/json/final/"
  for subject in os.listdir(json_path):
    for topic in os.listdir(json_path + subject):
      if topic in created_files:
        continue
      for json_file in os.listdir(f"{json_path}{subject}/{topic}"):
        if json_file.endswith(".json"):
          file_name, _ = json_file.split(".")
          folder_name = f"dataset/images/{subject}/{topic}/{file_name}"
          with open(f"{json_path}{subject}/{topic}/{json_file}") as f:
            data = json.load(f)
            print(data["slide_id"])

            i = 0
            for slide in data["slides"]:
              print(slide["pg_no"])
              # if slide["pg_no"] <= 9:
              #   img_path = f"{folder_name}/0{i}{file_name}{topic}.png"
              # else:
              #   img_path = f"{folder_name}/{i}{file_name}{topic}.png"
              # print(img_path)
              # image = cv2.imread(img_path)
              a += 1
              i += 1
              
              elements = slide["elements"]
              
              for element_type, element_list in elements.items():
                for items in element_list:
                  new_annotations = get_pixel_values(items)
                  items["xmin"] = new_annotations["xmin"]
                  items["ymin"] = new_annotations["ymin"]
                  items["width"] = new_annotations["width"]
                  items["height"] = new_annotations["height"]
                  items["label"] = new_annotations["label"]
                  if element_type == 'figures' or element_type == 'equations' or element_type == 'tables':
                    if 'caption' in items.keys():
                      new_annotations = get_pixel_values(items["caption"])
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                      items["caption"]["label"] = new_annotations["label"]
                  if element_type == 'text' and items["label"] == 'enumeration':
                    if 'heading' in items.keys():
                      new_annotations = get_pixel_values(items["heading"])
                      items["heading"]["xmin"] = new_annotations["xmin"]
                      items["heading"]["ymin"] = new_annotations["ymin"]
                      items["heading"]["width"] = new_annotations["width"]
                      items["heading"]["height"] = new_annotations["height"]
                      items["heading"]["label"] = new_annotations["label"]
                    
                if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
                  os.makedirs(f"dataset/json/{subject}/{topic}/")
                with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
                  json.dump(data, f, indent=3)
  print(f"🟢 (4/5) Annotations corrected for {a} images.")

def show_annotations(filename):
    with open(f"dataset/json/{filename}.json", "r") as f:
      data = json.load(f)
    images = []
    print(filename)
    subject, topic, version = filename.split("/")
    for slide in data["slides"]:
        i = slide["pg_no"]
        if i <= 9:
          img_path = f"dataset/images/{subject}/{topic}/{version}/0{i}{version}{topic}.png"
        else:
          img_path = f"dataset/images/{subject}/{topic}/{version}/{i}{version}{topic}.png"
        image = cv2.imread(img_path)
        print(img_path)

        elements = slide["elements"]
        
        for element_type, element_list in elements.items():
          for items in element_list:
            if element_type == 'figures' or element_type == 'tables' or element_type == 'equations':
              if 'caption' in items.keys():
                cv2.rectangle(image, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 2)
            if element_type == 'description' and items["label"] == 'enumeration':
              if 'heading' in items.keys():  
                cv2.rectangle(image, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 2)
            cv2.rectangle(image, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 2)
        
        # save the annotated image
        # cv2.imwrite(f"dataset/images/{filename}/slide{i-1}_bbox.png", image)
        
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

if __name__ == "__main__":
    # move_files()
    # correction()
    for subject in os.listdir("dataset/json"):
        for topic in os.listdir(f"dataset/json/{subject}"):
            json_files = os.listdir(f"dataset/json/{subject}/{topic}")
            # randomly shuffle the json files list
            np.random.shuffle(json_files)
            for json_file in json_files:
                if json_file.endswith(".json"):
                    show_annotations(f"{subject}/{topic}/{json_file.split('.')[0]}")
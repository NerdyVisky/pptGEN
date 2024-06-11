import cv2
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches 

# Convert Inches to Pixels
def get_pixel_values(element):
    slide_width = 13.333
    slide_height = 7.50

    # Get the bounding box coordinates
    xmin = element.get("xmin", 0)
    ymin = element.get("ymin", 0)
    width = element.get("width", 0)
    height = element.get("height", 0)
    
    # Handle the case where the bounding box is outside the slide
    if xmin + width > slide_width:
        width = slide_width - xmin
    if ymin + height > slide_height:
        height = slide_height - ymin
    
    normalized_bbox = {
        "xmin": int(xmin / slide_width * 1280),
        "ymin": int(ymin / slide_height * 720),
        "width": int(width / slide_width * 1280),
        "height": int(height / slide_height * 720),
    }    
    return normalized_bbox

# Move from code/json to dataset/json while converting inches to pixels
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
          with open(f"{json_path}{subject}/{topic}/{json_file}", 'r') as f:
            data = json.load(f)
            # print(data)
            for slide in data["slides"]:
              a += 1
              elements = slide["elements"]
              
              for element_type, element_list in elements.items():
                for items in element_list:
                  new_annotations = get_pixel_values(items)
                  items["xmin"] = new_annotations["xmin"]
                  items["ymin"] = new_annotations["ymin"]
                  items["width"] = new_annotations["width"]
                  items["height"] = new_annotations["height"]
                  if element_type == 'figures' or element_type == 'equations' or element_type == 'tables':
                    if 'caption' in items.keys():
                      new_annotations = get_pixel_values(items["caption"])
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                  if element_type == 'text' and items["label"] == 'enumeration':
                    if 'heading' in items.keys():
                      new_annotations = get_pixel_values(items["heading"])
                      items["heading"]["xmin"] = new_annotations["xmin"]
                      items["heading"]["ymin"] = new_annotations["ymin"]
                      items["heading"]["width"] = new_annotations["width"]
                      items["heading"]["height"] = new_annotations["height"]
                    
            if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
              os.makedirs(f"dataset/json/{subject}/{topic}/")
            try:
              with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
                json.dump(data, f, indent=3)
            except:
              print(f"{json_file} already exists.")
  print(f"🟢 (4/5) Annotations corrected for {a} images.")

# Random Display of annnotations
def show_annotations():
  json_path = f"dataset/json/"
  for subject in os.listdir(json_path):
    for topic in os.listdir(json_path + subject):
      json_files = os.listdir(f"{json_path}{subject}/{topic}")
      np.random.shuffle(json_files)
      for json_file in json_files:
        if json_file.endswith(".json"):
          file_name, _ = json_file.split(".")
          folder_name = f"dataset/images/{subject}/{topic}/{file_name}"
          print(folder_name)
          with open(f"{json_path}{subject}/{topic}/{json_file}") as f:
            data = json.load(f)
            print(data["slide_id"])
            for slide in data["slides"]:
              i = slide["pg_no"]
              if slide["pg_no"] <= 9:
                img_path = f"{folder_name}/0{i}{file_name}{topic}.png"
              else:
                img_path = f"{folder_name}/{i}{file_name}{topic}.png"
              print(img_path)
              image = cv2.imread(img_path)
              
              elements = slide["elements"]
              
              for element_type, element_list in elements.items():
                for items in element_list:
                  if element_type == 'figures' or element_type == 'tables' or element_type == 'equations':
                    if 'caption' in items.keys():
                      cv2.rectangle(image, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 1)
                  if element_type == 'description' and items["label"] == 'enumeration':
                    if 'heading' in items.keys():
                      cv2.rectangle(image, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 1)
                  cv2.rectangle(image, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                
                # show the image
              cv2.imshow("image", image)
              cv2.waitKey(0)
              cv2.destroyAllWindows()

# Expand or Shrink for title
def correction_title(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])
    image_height, image_width, _ = image.shape
  
    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    if np.any(image[ymin, xmin:xmax] == target_color):
        while ymin > 0 and np.any(image[ymin, xmin:xmax] == target_color):
            ymin -= 1
    else:
        while ymin < image_height - 1 and not np.any(image[ymin, xmin:xmax] == target_color):
            ymin += 1
            
    if np.any(image[ymax, xmin:xmax] == target_color):
        while ymax < image_height - 1 and np.any(image[ymax, xmin:xmax] == target_color):
            ymax += 1
    else:
        while ymax > 0 and not np.any(image[ymax, xmin:xmax] == target_color):
            ymax -= 1
            
    if np.any(image[ymin:ymax, xmin] == target_color):
        while xmin > 0 and np.any(image[ymin:ymax, xmin] == target_color):
            xmin -= 1
    else:
        while xmin < image_width - 1 and not np.any(image[ymin:ymax, xmin] == target_color):
            xmin += 1
    
    if np.any(image[ymin:ymax, xmax] == target_color):
        while xmax < image_width - 1 and np.any(image[ymin:ymax, xmax] == target_color):
            xmax += 1
    else:
        while xmax > 0 and not np.any(image[ymin:ymax, xmax] == target_color):
            xmax -= 1
          
    new_annotations = {
      "xmin": int(xmin),
      "ymin": int(ymin),
      "width": int(xmax - xmin),
      "height": int(ymax - ymin)
    }
    return new_annotations
  
# Shrink till target color is found
def correction_shrink(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])

    image_height, image_width, _ = image.shape
  
    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    while ymin < ymax and not np.any(image[ymin, xmin:xmax] == target_color):
        ymin += 1
    while ymax > ymin and not np.any(image[ymax, xmin:xmax] == target_color):
        ymax -= 1
    while xmin < xmax and not np.any(image[ymin:ymax, xmin] == target_color):
        xmin += 1
    while xmax > xmin and not np.any(image[ymin:ymax, xmax] == target_color):
        xmax -= 1
      
    new_annotations = {
        "xmin": int(xmin),
        "ymin": int(ymin),
        "width": int(xmax - xmin),
        "height": int(ymax - ymin)
    }
    return new_annotations

# Mask black color and find the bounding box
def correction_unimask(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    # image1 = image.copy()
    image1 = image[ymin:ymax, xmin:xmax]
    
    target_color_1 = np.array([0, 0, 0])
    target_color_2 = np.array([100, 100, 100])
  
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, target_color_1, target_color_2)
    
    kernel = np.ones((5, 5), np.uint8)
    
    gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
    
    where_white = np.where(gradient == 255)
    if where_white[0].size > 0:
      x1 = min(where_white[1])
      y1 = min(where_white[0])
      x2 = max(where_white[1])
      y2 = max(where_white[0])
    
      xmin_n = xmin + x1
      ymin_n = ymin + y1
      xmax_n = xmin + x2
      ymax_n = ymin + y2
    
      new_annotations = {
          "xmin": int(xmin_n),
          "ymin": int(ymin_n),
          "width": int(xmax_n - xmin_n),
          "height": int(ymax_n - ymin_n)
      }
      return new_annotations
    return annotations

# Simple Maths to correct the bounding box
def correction_calc(annotations, image):
  path = annotations["path"]
  
  og_img = cv2.imread(path)
  
  apect_ratio = og_img.shape[1] / og_img.shape[0]
  
  xmin = annotations["xmin"]
  ymin = annotations["ymin"]
  height = annotations["height"]
  width = annotations["width"]
  
  new_height = height
  new_width = height * apect_ratio
  
  if new_width > width: 
    return correction_unimask(annotations, image)
  else:
    new_annotations = {
      "xmin": int(xmin + (width - new_width) / 2),
      "ymin": ymin,
      "width": int(new_width),
      "height": new_height
      }
    return new_annotations

# Mask any color except white and find the bounding box
def correction_mask(annotations, image):
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    image_height, image_width, _ = image.shape

    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    # image1 = image.copy()
    image1 = image[ymin:ymax, xmin:xmax]
  
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
   
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([50, 50, 50]))

    kernel = np.ones((3, 3), np.uint8)
    
    gradient1 = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)

    where_white = np.where(gradient1 == 255)
    if where_white[0].size > 0:
      x1 = min(where_white[1])
      y1 = min(where_white[0])
      x2 = max(where_white[1])
      y2 = max(where_white[0])
    
      xmin_n = xmin + x1
      ymin_n = ymin + y1
      xmax_n = xmin + x2
      ymax_n = ymin + y2
    
      new_annotations = {
          "xmin": int(xmin_n),
          "ymin": int(ymin_n),
          "width": int(xmax_n - xmin_n),
          "height": int(ymax_n - ymin_n)
      }
      return new_annotations
    return annotations




    

def correction():
  a = 0
  json_path = f"dataset/json/"
  for subject in os.listdir(json_path):
    topics = os.listdir(json_path + subject)
    # np.random.shuffle(topics)
    for topic in topics:
      for json_file in os.listdir(f"{json_path}{subject}/{topic}"):
        if json_file.endswith(".json"):
          folder_name = f"dataset/images/{subject}/{topic}/{json_file.split('.')[0]}"
          print(folder_name)
          with open(f"{json_path}{subject}/{topic}/{json_file}", 'r') as f:
            data = json.load(f)
            
            for slide in data["slides"]:
              i = slide["pg_no"]
              if slide["pg_no"] <= 9:
                img_path = f"{folder_name}/0{i}{json_file.split('.')[0]}{topic}.png"
              else:
                img_path = f"{folder_name}/{i}{json_file.split('.')[0]}{topic}.png"
              print(img_path)
              image = cv2.imread(img_path)
              image1 = cv2.imread(img_path)
              a += 1
              
              elements = slide["elements"]
              
              for element_type, element_list in elements.items():
                for items in element_list:
                  print(items["label"])
                              
                  # Title - corrected (expand)      
                  if element_type == 'title':
                    new_annotations = correction_title(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                  
                  # Footer, Refs, Code - corrected (shrink)
                  if element_type == 'footer' or element_type == 'refs' or element_type == 'code':
                    new_annotations = correction_shrink(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                  
                  # Enum Heading - corrected (shrink)  
                  if 'heading' in items.keys():
                    new_annotations = correction_shrink(items["heading"], image)
                    items["heading"]["xmin"] = new_annotations["xmin"]
                    items["heading"]["ymin"] = new_annotations["ymin"]
                    items["heading"]["width"] = new_annotations["width"]
                    items["heading"]["height"] = new_annotations["height"]
                  
                  # Captions - corrected (shrink)
                  if 'caption' in items.keys():
                    new_annotations = correction_shrink(items["caption"], image)
                    items["caption"]["xmin"] = new_annotations["xmin"]
                    items["caption"]["ymin"] = new_annotations["ymin"]
                    items["caption"]["width"] = new_annotations["width"]
                    items["caption"]["height"] = new_annotations["height"]
                      
                  # Equations - corrected (unimask)
                  if element_type == 'equations':
                    new_annotations = correction_unimask(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    
                  # Diagrams and Plots - corrected (calc)
                  if element_type == 'figures':
                    new_annotations = correction_calc(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                                       
                  # Text Content: Enumeration - corrected
                  if element_type == 'text' and items["label"] == 'enumeration':
                    new_annotations = correction_mask(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    if items["label"] == 'enumeration':
                      
                        
                  # Text Content: Description - corrected
                  if element_type == 'text' and items["label"] == 'text':
                    new_annotations = correction_mask(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                  
                  
                    
              cv2.imshow("image", image1)
              cv2.waitKey(0)
              cv2.destroyAllWindows()     
            
            # print(data)   
            # if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
            #   os.makedirs(f"dataset/json/{subject}/{topic}/")
            # with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
            #   json.dump(data, f, indent=3)
            # if a == 5:
            #   return
              
  print(f"🟢 (4/5) Annotations corrected for {a} images.")

if __name__ == "__main__":
    # move_files()
    correction()
    # show_annotations()

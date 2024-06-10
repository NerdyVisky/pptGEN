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

def modify(image, xmin, ymin, xmax, ymax, target_color):
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

  return xmin, ymin, xmax, ymax

def correction_text(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])

    xmin, ymin, xmax, ymax = modify(image, xmin, ymin, xmax, ymax, target_color)    
      
    new_annotations = {
        "xmin": int(xmin),
        "ymin": int(ymin),
        "width": int(xmax - xmin),
        "height": int(ymax - ymin)
    }
    return new_annotations

def correction_title(annotations, image, is_logo=0):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])

    # print(xmin, ymin, xmax, ymax, target_color)

    xmin, ymin, xmax, ymax = modify(image, xmin, ymin, xmax, ymax, target_color)    
    
    # print(xmin, ymin, xmax, ymax)
    # if annotations["label"] == 'title':  
    #   if is_logo == 1: # Logo on left
    #     if xmin >= 24 and xmin <= 120: # Xmin is lying on logo
    #       xmin = 121  # push xmin out of logo and correct again
    #       xmin, ymin, xmax, ymax = modify(image, xmin, ymin, xmax, ymax, target_color)
    #   if is_logo == 2:
    #     if xmax >= 1159 and xmax <= 1255: # Xmax is lying on logo
    #       xmax = 1158 # push xmax out of logo and correct again
    #       xmin, ymin, xmax, ymax = modify(image, xmin, ymin, xmax, ymax, target_color)
          
    new_annotations = {
      "xmin": int(xmin),
      "ymin": int(ymin),
      "width": int(xmax - xmin),
      "height": int(ymax - ymin)
    }
    return new_annotations

def correction_enum(annotations, image):
    # Initializing coordinates
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    image_height, image_width, _ = image.shape

    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color_1 = np.array([font_color["b"], font_color["g"], font_color["r"]])
    
    if target_color_1[2] == 0:
      target_color_2 = np.array([169, 169, 169]) # Black
    else:
      target_color_2 = np.array([211, 211, 211]) # White

    while ymin < ymax and not ( np.any(image[ymin, xmin:xmax] == target_color_1) or np.any(image[ymin, xmin:xmax] == target_color_2) ):
        ymin += 1
    while ymax > ymin and not ( np.any(image[ymax, xmin:xmax] == target_color_1) or np.any(image[ymax, xmin:xmax] == target_color_2) ):
        ymax -= 1
    while xmin < xmax and not ( np.any(image[ymin:ymax, xmin] == target_color_1) or np.any(image[ymin:ymax, xmin] == target_color_2) ):
        xmin += 1
    while xmax > xmin and not ( np.any(image[ymin:ymax, xmax] == target_color_1) or np.any(image[ymin:ymax, xmax] == target_color_2) ):
        xmax -= 1
        
    new_annotations = {
        "xmin": int(xmin),
        "ymin": int(ymin),
        "width": int(xmax - xmin),
        "height": int(ymax - ymin)
    }
    return new_annotations

def bgr_to_hsv_range(bgr_color):
    hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    return hsv_color

def create_color_mask(hsv_image, hsv_color, tolerance=10):
    lower_bound = np.array([max(hsv_color[0] - tolerance, 0), 50, 50])
    upper_bound = np.array([min(hsv_color[0] + tolerance, 179), 255, 255])
    return cv2.inRange(hsv_image, lower_bound, upper_bound)

def correction_desc(annotations, image):
    TITLE_COLORS_DARK = [ # in BGR format
      [60, 20, 220], # Crimson
      [0, 128, 0], # Emerald Green
    ]
    
    TITLE_COLORS_LIGHT = [ # in BGR format
      [0, 69, 255], # Orange-Red
      [225, 105, 65], # Royal Blue
    ]
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    image_height, image_width, _ = image.shape

    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    style = annotations["style"]
    font_color = style["font_color"]
    target_color = np.array([font_color["b"], font_color["g"], font_color["r"]])
    
    if target_color[2] == 0:
      C2 = bgr_to_hsv_range(TITLE_COLORS_DARK[0])
      C3 = bgr_to_hsv_range(TITLE_COLORS_DARK[1])
      
    else:
      C2 = bgr_to_hsv_range(TITLE_COLORS_LIGHT[0])
      C3 = bgr_to_hsv_range(TITLE_COLORS_LIGHT[1])
    
    # image1 = image.copy()
    image1 = image[ymin:ymax, xmin:xmax]
  
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    
    
    mask1 = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([50, 50, 50]))
    mask2 = create_color_mask(hsv, C2, 10)
    mask3 = create_color_mask(hsv, C3, 10)
    
    kernel = np.ones((5, 5), np.uint8)
    
    gradient1 = cv2.morphologyEx(mask1, cv2.MORPH_GRADIENT, kernel) + cv2.morphologyEx(mask2, cv2.MORPH_GRADIENT, kernel) + cv2.morphologyEx(mask3, cv2.MORPH_GRADIENT, kernel)

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

def correction_diagram(annotations, image):
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
    return correction_eqn(annotations, image)
  else:
    new_annotations = {
      "xmin": int(xmin + (width - new_width) / 2),
      "ymin": ymin,
      "width": int(new_width),
      "height": new_height
      }
    return new_annotations

def correction_eqn(annotations, image):
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
              # image1 = cv2.imread(img_path)
              a += 1
              
              elements = slide["elements"]
              
              for element_type, element_list in elements.items():
                for items in element_list:
                  print(items["label"])
                                    
                  # Tables - corrected
                  if element_type == 'tables':
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                    if 'caption' in items.keys():
                      new_annotations = correction_text(items["caption"], image)
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                      # cv2.rectangle(image1, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 1)
                  
                  # Equations - corrected
                  if element_type == 'equations':
                    new_annotations = correction_eqn(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                    if 'caption' in items.keys():
                      new_annotations = correction_text(items["caption"], image)
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                      # cv2.rectangle(image1, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 1)
                  
                  # Diagrams and Plots - corrected
                  if element_type == 'figures':
                    new_annotations = correction_diagram(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                    if 'caption' in items.keys():
                      new_annotations = correction_text(items["caption"], image)
                      items["caption"]["xmin"] = new_annotations["xmin"]
                      items["caption"]["ymin"] = new_annotations["ymin"]
                      items["caption"]["width"] = new_annotations["width"]
                      items["caption"]["height"] = new_annotations["height"]
                      # cv2.rectangle(image1, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 1)
                      
                  # Graphics: Logo - corrected
                  # if element_type == 'graphic':
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                      
                  # Text Cotent: Title, Footer, Refs, Code, Text - corrected
                  if element_type == 'footer' or element_type == 'refs' or element_type == 'code' or element_type == 'title':
                    new_annotations = correction_text(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                    
                  # Text Content: Enumeration - corrected
                  if element_type == 'text' and items["label"] == 'enumeration':
                    new_annotations = correction_enum(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                    if items["label"] == 'enumeration':
                      if 'heading' in items.keys():
                        new_annotations = correction_text(items["heading"], image)
                        items["heading"]["xmin"] = new_annotations["xmin"]
                        items["heading"]["ymin"] = new_annotations["ymin"]
                        items["heading"]["width"] = new_annotations["width"]
                        items["heading"]["height"] = new_annotations["height"]
                        # cv2.rectangle(image1, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 1)
                    
                  # Text Content: Description - corrected
                  if element_type == 'text' and items["label"] == 'text':
                    new_annotations = correction_desc(items, image)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    # cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                 
            # print(data)   
            if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
              os.makedirs(f"dataset/json/{subject}/{topic}/")
            with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
              json.dump(data, f, indent=3)
            # if a == 5:
            #   return
              
  print(f"🟢 (4/5) Annotations corrected for {a} images.")

if __name__ == "__main__":
    # move_files()
    # correction()
    show_annotations()

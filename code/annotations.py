import cv2
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches 
import time
from tqdm import tqdm

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
                  if element_type == 'text' and items["label"] == 'enumeration':
                    if 'heading' in items.keys():
                      cv2.rectangle(image, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 1)
                  cv2.rectangle(image, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
                
                # show the image
              cv2.imshow("image", image)
              cv2.waitKey(0)
              cv2.destroyAllWindows()

# Cover the images on SLide
def cover_images(annotations, image):
  for item in annotations:
      xmin = item["xmin"] - 3
      ymin = item["ymin"] - 3
      xmax = xmin + item["width"] + 6
      ymax = ymin + item["height"] + 6
      image[ymin:ymax, xmin:xmax] = 255
  return image

def correction_calc(annotations, image):
  if 'path' in annotations.keys():
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
      new_width = width
      new_height = width / apect_ratio
      new_annotations = {
        "label": "figures",
        "xmin": xmin,
        "ymin": int(ymin + (height - new_height) / 2),
        "width": new_width,
        "height": int(new_height)
      }
      newer_annotations = correction_mask(new_annotations, image)
      return newer_annotations
    else:
      new_annotations = {
        "label": "figures",
        "xmin": int(xmin + (width - new_width) / 2),
        "ymin": ymin,
        "width": int(new_width),
        "height": new_height
        }
      newer_annotations = correction_mask(new_annotations, image)
      return newer_annotations
  return annotations

# Mask any color except white and find the bounding box
def correction_mask(annotations, image):
    label = annotations.get("label", "")
    xmin = annotations["xmin"]
    ymin = annotations["ymin"]
    xmax = xmin + annotations["width"]
    ymax = ymin + annotations["height"]
    
    image_height, image_width, _ = image.shape

    xmin = max(0, min(xmin, image_width - 1))
    ymin = max(0, min(ymin, image_height - 1))
    xmax = max(0, min(xmax, image_width - 1))
    ymax = max(0, min(ymax, image_height - 1))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if label == 'title' and np.any(gray[ymax, xmin:xmax] != 255):
      xmin = 0
      ymin = 0
      xmax = 1189
      ymax = 198
      
    # if label == 'url':
    #   image1 = image[ymin:ymax, xmin:xmax]
    #   for i in range(image1.shape[0]):
    #     for j in range(image1.shape[1]):
    #       if (image1[i, j] == [255, 0, 0]).all():
    #         image1[i, j] = [0, 0, 0]
    # else:
    image1 = gray[ymin:ymax, xmin:xmax]
    threshold = cv2.threshold(image1, 254, 255, cv2.THRESH_BINARY)[1]
    
    # cv2.imshow("image", threshold)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    where_black = np.where(threshold == 0)      
    if where_black[0].size > 0:
      x1 = min(where_black[1])
      y1 = min(where_black[0])
      x2 = max(where_black[1])
      y2 = max(where_black[0])
    
      xmin_n = xmin + x1
      ymin_n = ymin + y1
      xmax_n = xmin + x2
      ymax_n = ymin + y2
  
      new_annotations = {
          "label": label,
          "xmin": int(xmin_n),
          "ymin": int(ymin_n),
          "width": int(xmax_n - xmin_n),
          "height": int(ymax_n - ymin_n)
      }
      # print(new_annotations)
      return new_annotations
    return annotations

def correction():
  a = 0
  json_path = f"dataset/json/"
  for subject in os.listdir(json_path):
    topics = os.listdir(json_path + subject)
    np.random.shuffle(topics)
    for topic in topics:
      for json_file in os.listdir(f"{json_path}{subject}/{topic}"):
        if json_file.endswith(".json"):
          folder_name = f"dataset/images_white/{subject}/{topic}/{json_file.split('.')[0]}"
          print(folder_name)
          with open(f"{json_path}{subject}/{topic}/{json_file}", 'r') as f:
            data = json.load(f)
            
            for slide in data["slides"]:
              i = slide["pg_no"]
              if slide["pg_no"] <= 9:
                img_path = f"{folder_name}/0{i}{json_file.split('.')[0]}{topic}.png"
              else:
                img_path = f"{folder_name}/{i}{json_file.split('.')[0]}{topic}.png"
              # print(img_path)
              image = cv2.imread(img_path)
              a += 1
              
              elements = slide["elements"]
              
              image1 = image.copy()
              cover_coordinates_images = []
              
              if 'graphic' in elements.keys():
                for items in elements["graphic"]:
                  cover_coordinates_images.append(items)
              
              # Cover Images, and URLs to annotate Text
              image_for_images = cover_images(cover_coordinates_images, image)
              for element_type, element_list in elements.items():
                for items in element_list:
                  if element_type == 'equations':
                    new_annotations = correction_mask(items, image_for_images)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    cover_coordinates_images.append(new_annotations)
                    
                  if element_type == 'figures' or element_type == 'tables':
                    new_annotations = correction_mask(items, image_for_images)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    cover_coordinates_images.append(new_annotations)
                  
                  if element_type == 'refs':
                    new_annotations = correction_mask(items, image_for_images)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                    cover_coordinates_images.append(new_annotations)
                  
                  # Captions
                  if 'caption' in items.keys():
                    if items["caption"]["width"] > 0.7 * 1280:
                      items["caption"]["width"] = int( 0.7 * 1280)
                      items["caption"]["xmin"] = int( items["caption"]["xmin"] + 0.15 * items["caption"]["width"])
                    new_annotations = correction_mask(items["caption"], image_for_images)
                    items["caption"]["xmin"] = new_annotations["xmin"]
                    items["caption"]["ymin"] = new_annotations["ymin"]
                    items["caption"]["width"] = new_annotations["width"]
                    items["caption"]["height"] = new_annotations["height"]
                    cover_coordinates_images.append(new_annotations)
                  
              image_for_text = cover_images(cover_coordinates_images, image)              
              for element_type, element_list in elements.items():
                for items in element_list:
                  
                  # Title, Footer, Refs, Code - corrected
                  if element_type == 'footer' or element_type == 'title' or element_type == 'code' or element_type == 'text':
                    new_annotations = correction_mask(items, image_for_text)
                    items["xmin"] = new_annotations["xmin"]
                    items["ymin"] = new_annotations["ymin"]
                    items["width"] = new_annotations["width"]
                    items["height"] = new_annotations["height"]
                  
                  # Enum Heading
                  if 'heading' in items.keys():
                    new_annotations = correction_mask(items["heading"], image_for_text)
                    items["heading"]["xmin"] = new_annotations["xmin"]
                    items["heading"]["ymin"] = new_annotations["ymin"]
                    items["heading"]["width"] = new_annotations["width"]
                    items["heading"]["height"] = new_annotations["height"]
                  
                  

              # for element_type, element_list in elements.items():
              #   for items in element_list:
              #     # draw bounding box
              #     cv2.rectangle(image1, (items.get("xmin", 0), items.get("ymin", 0)), (items.get("xmin", 0) + items.get("width", 0), items.get("ymin", 0) + items.get("height", 0)), (255, 0, 0), 1)
              #     cv2.putText(image1, items.get("label", ""), (items.get("xmin", 0), items.get("ymin", 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                  
              #     if 'caption' in items.keys():                   
              #       cv2.rectangle(image1, (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), (items["caption"].get("xmin", 0) + items["caption"].get("width", 0), items["caption"].get("ymin", 0) + items["caption"].get("height", 0)), (255, 0, 0), 1)
              #       cv2.putText(image1, items["caption"].get("label", ""), (items["caption"].get("xmin", 0), items["caption"].get("ymin", 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
              #     if 'heading' in items.keys():
              #       cv2.rectangle(image1, (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), (items["heading"].get("xmin", 0) + items["heading"].get("width", 0), items["heading"].get("ymin", 0) + items["heading"].get("height", 0)), (255, 0, 0), 1)
              #       cv2.putText(image1, items["heading"].get("label", ""), (items["heading"].get("xmin", 0), items["heading"].get("ymin", 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                  
              # cv2.imshow("image", image1)
              # cv2.waitKey(0)
              # cv2.destroyAllWindows()     
            
            # print(data)   
            if not os.path.exists(f"dataset/json/{subject}/{topic}/"):
              os.makedirs(f"dataset/json/{subject}/{topic}/")
            with open(f"dataset/json/{subject}/{topic}/{json_file}", "w") as f:
              json.dump(data, f, indent=3)
            # if a == 5:
            #   return
              
  print(f"🟢 (4/5) Annotations corrected for {a} images.")

def rename_files():
  folder_path = "dataset/images/"
  for subject in os.listdir(folder_path):
    # print(subject)
    for topic in os.listdir(folder_path + subject):
      # print(topic)
      for slide in os.listdir(folder_path + subject + '/' + topic):
        # print(slide)
        for image in os.listdir(folder_path + subject + '/' + topic + '/' + slide):
          if image.endswith(".png"):
            image_id = image.split('.')[0]
            # print(image_id)
            if len(image_id) == 6:
              new_image_id = '0' + image_id[-1] + slide + topic
            else:
              new_image_id = image_id[-2:] + slide + topic
            # print(new_image_id)
            os.rename(folder_path + subject + '/' + topic + '/' + slide + '/' + image, folder_path + subject + '/' + topic + '/' + slide + '/' + new_image_id + '.png')
            # return

if __name__ == "__main__":
    start_time = time.time()
    # move_files()
    # correction()
    show_annotations()
    # rename_files()
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time} seconds")
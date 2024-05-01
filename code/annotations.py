from PIL import Image, ImageDraw
import json

def get_normalized_bbox(t_xmin, t_ymin, t_width, t_height):
  slide_width = 13.333
  slide_height = 7.50
  return {
      "xmin": int(t_xmin / slide_width * 800),
      "ymin": int(t_ymin / slide_height * 450),
      "width": int(t_width / slide_width * 800),
      "height": int(t_height / slide_height * 450),
  }

def get_element_annotations(element):
  legend = {
      'title': 'red',
      'url': 'lightgray',
      'text': 'blue',
      'enumeration': 'green',
      'equations': 'orange',
      'tables': 'yellow',
      'footer': 'darkgray',
      'graph': 'purple',
      'block-diagram': 'purple',
      'tree': 'purple',
      'flow-chart': 'purple',
      'pie-chart': 'purple',
      'bar-chart': 'purple',
      'line-chart': 'purple',
      'caption': 'cyan'
    }
  annotations = []
  for slide in slide["slides"]:
    for element in slide["elements"]:
      element_label = element.get("label", "")
      if element_label in legend:
        xmin = element.get("xmin", 0)
        ymin = element.get("ymin", 0)
        width = element.get("width", 0)
        height = element.get("height", 0)
        color = legend[element_label]
        annotations.append({
            "label": element_label,
            "xmin": xmin,
            "ymin": ymin,
            "width": width,
            "height": height,
            "color": color
        })
  return annotations

def main():
  with open("code/json/11256.json", "r") as f:
    data = json.load(f)
    
  i = 0
  for slide in data["slides"]:
    print(slide["pg_no"])
    img_path = f"images/11256/page{i}.png"
    image = Image.open(img_path)
    resized_image = image.resize((800, 450))
    draw = ImageDraw.Draw(resized_image)
    i += 1
    elements = slide["elements"]
    for element in elements:
      annotations = get_element_annotations(element)
      
    # bbox = get_element_annotations(slide)
    # xmin = bbox["xmin"]
    # ymin = bbox["ymin"]
    # xmax = bbox["xmin"] + bbox["width"]
    # ymax = bbox["ymin"] + bbox["height"]
    
    # draw.rectangle((xmin, ymin, xmax, ymax), outline=bbox["color"], width=2) 
    # resized_image.show()
    # resized_image.save(f"images/annotations/11256/page{i - 1}_bbox.png")
  
if __name__ == "__main__":
  main()
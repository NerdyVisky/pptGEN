import json
import os
from dotenv import load_dotenv, find_dotenv
from random_generator import get_random_image

load_dotenv(find_dotenv())

base = 'code/temp/'

for subject in os.listdir(base):
    for topic in os.listdir(base + subject):
        with open(base + subject + '/' + topic, 'r') as f:
            content = json.load(f)
            
            dumb_id = content['presentation_ID']
            real_id = topic.split('.')[0]
            
            # print(f"{real_id}")
            
            slides = content['slides']
            for slide in slides:
                i = slide["slide_number"]
                if 'images' in slide:
                    images = slide['images']
                    for image in images:
                        if 'path' in image.keys():
                            print(real_id)
                            path = image['path']
                            if path.startswith('code\\buffer\\graphics\\12452\\'):
                                print(i, '-')
                                new_path = get_random_image(real_id, i)
                                image["path"] = new_path
                            else:
                                print(i, '+')
            with open(base + subject + '/' + topic, 'w') as f:
                json.dump(content, f, indent=4)
                            

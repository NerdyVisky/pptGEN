import os
import json
import numpy as np

def get_average_caption_dims(SOURCE_FOLDER):
    parent_dirs = os.listdir(SOURCE_FOLDER)
    avg_dims = []
    for parent_dir in parent_dirs:
        for item in os.listdir(os.path.join(SOURCE_FOLDER, parent_dir)):
            json_folder = os.path.join(SOURCE_FOLDER, parent_dir, item)
            if os.path.isdir(json_folder):
                ttl_width = 0
                ttl_height = 0
                valid_count = 0
                vers_json = os.listdir(json_folder)
                for ver_json in vers_json:
                    json_path = os.path.join(SOURCE_FOLDER, parent_dir, item, ver_json)
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        for slide_obj in data["slides"]:
                            if 'figures' in slide_obj['elements'].keys():
                                for figure_obj in slide_obj["elements"]["figures"]:
                                    if figure_obj["caption"]["width"] != 0:
                                        ttl_width += figure_obj["caption"]["width"]
                                        ttl_height += figure_obj["caption"]["height"]
                                        valid_count += 1
                avg_dims.append([(ttl_width/valid_count), (ttl_height/valid_count)])
    return avg_dims


def correct_caption_dims(SOURCE_FOLDER, averages):
    parent_dirs = os.listdir(SOURCE_FOLDER)
    for parent_dir in parent_dirs:
        for item in os.listdir(os.path.join(SOURCE_FOLDER, parent_dir)):
            json_folder = os.path.join(SOURCE_FOLDER, parent_dir, item)
            if os.path.isdir(json_folder):
                vers_json = os.listdir(json_folder)
                for ver_json in vers_json:
                    json_path = os.path.join(SOURCE_FOLDER, parent_dir, item, ver_json)
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        for slide_obj in data["slides"]:
                            if 'figures' in slide_obj['elements'].keys():
                                for figure_obj in slide_obj["elements"]["figures"]:
                                    if figure_obj["caption"]["width"] == 0 or figure_obj["caption"]["height"] == 0:
                                        figure_obj["caption"]["width"] = averages[0]
                                        figure_obj["caption"]["height"] = averages[1]
                    
                    with open(json_path, 'w') as f:
                        json.dump(data, f, indent=3)
    return



avg_dims = get_average_caption_dims('dataset/json')
np_arr = np.array(avg_dims)
averages = np.mean(np_arr, axis=0)
print(averages)

correct_caption_dims('dataset/json', averages)
    
                
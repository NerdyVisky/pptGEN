import json
import os
from collections import Counter

json_path = 'dataset/json/'

def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed

def calculate_ppt_data(data):
    frequency_counter = Counter()
    for slide in data["slides"]:
        frequency_counter["slide"] += 1
        for element_type in ['title', 'description', 'equations','tables','figures','footer']:
            if element_type == 'description' and "description" in slide["elements"]:
                desc = slide["elements"][element_type]
                for item in desc:
                    frequency_counter[item["label"]] += 1
            elif element_type == 'figures' and "figures" in slide["elements"]:
                figures = slide["elements"][element_type]
                for figure in figures:
                    frequency_counter[figure["label"]] += 1
            elif element_type == 'footer' and "footer" in slide["elements"]:
                footer = slide["elements"][element_type]
                for item in footer:
                    frequency_counter[item["label"]] += 1
            elif element_type in slide["elements"] and slide["elements"][element_type]:
                frequency_counter[element_type] += 1
                
    return frequency_counter

def main(): 
    total_stats = Counter()
    for file in os.listdir(json_path):
        if file.endswith('.json'):
            data = fetch_seed_content(json_path + file)
            stats = calculate_ppt_data(data)
            total_stats["PPTs"] += 1
            total_stats += stats
    print(total_stats)
    
    # Save the stats to a file
    with open('code/data/stats.json', 'w') as file:
        json.dump(total_stats, file, indent=4)
    
if __name__ == '__main__':
    main()
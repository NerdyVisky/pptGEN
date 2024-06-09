import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# path to your dataset folder containing the images, json....
DATASET_PATH = 'dataset/'

# Set to True to display plots, False to save them to disk
show_plots = False

# Aspect ratio and Area of Images - working on that

def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed

def calculate_ppt_data(data):
    frequency_counter = Counter()
    for slide in data["slides"]:
        frequency_counter["slides"] += 1
        a = 0
        for element_type in ['title', 'description', 'equations','tables','figures','footer']:
            if element_type == 'description' and "description" in slide["elements"]:
                desc = slide["elements"][element_type]
                for item in desc:
                    frequency_counter[item["label"]] += 1
                    a += 1
                    if "heading" in item and item["heading"]:
                        frequency_counter["heading"] += 1
                        a += 1
            elif element_type == 'figures' and "figures" in slide["elements"]:
                figures = slide["elements"][element_type]
                for figure in figures:
                    frequency_counter[figure["label"]] += 1
                    a += 1
                    if "caption" in item and item["caption"]:
                        frequency_counter["caption"] += 1
                        a += 1
            elif element_type == 'footer' and "footer" in slide["elements"]:
                footer = slide["elements"][element_type]
                for item in footer:
                    frequency_counter[item["label"]] += 1
                    a += 1
            elif element_type in slide["elements"] and slide["elements"][element_type]:
                a += 1
                frequency_counter[element_type] += 1
        frequency_counter[f"{a}_elements"] += 1
        frequency_counter["elements"] += a
    return frequency_counter

def get_raw_stats(): 
    element_counter = Counter()
    file_counter = Counter()
    json_path = DATASET_PATH + 'json/'
    for subject in os.listdir(json_path):
        file_counter["subjects"] += 1
        file_counter["total_PPTs"] += len(os.listdir(json_path + subject))
        file_counter[f"{subject}"] = {"topics": 0, "PPTs": 0, "images": 0}
        for topic in os.listdir(json_path + subject):
            file_counter[f"{subject}"]["topics"] += 1
            for file in os.listdir(json_path + subject + '/' + topic):
                file_counter[f"{subject}"]["PPTs"] += 1
                filename = os.path.join(json_path, subject, topic, file)
                if filename.endswith('.json'):
                    # print(json_path + subject + '/' + topic + '/' + file)
                    data = fetch_seed_content(filename)
                    file_counter[f"{subject}"]["images"] += len(data["slides"])
                    stats = calculate_ppt_data(data)
                    element_counter += stats
    # print(file_counter)
    # print(element_counter)
    
    # Save the stats to a file
    if not os.path.exists(DATASET_PATH + 'stats'):
        os.makedirs(DATASET_PATH + 'stats')
    with open(DATASET_PATH + 'stats/raw_stats.json', 'w') as outfile:
        data = {
            "file_counts": dict(file_counter),
            "element_counts": dict(element_counter)
            }
        json.dump(data, outfile, indent=4)
    


def make_triple_pie(sizes_inner, sizes_middle, sizes_outer, colors_inner, colors_middle, colors_outer, labels, radius=1):
    col_inner = [[int(i)/255 for i in c] for c in colors_inner]
    col_middle = [[int(i)/255 for i in c] for c in colors_middle]
    col_outer = [[int(i)/255 for i in c] for c in colors_outer]

    plt.axis('equal')
    width = 0.3  # Adjusted to fit three pie charts

    kwargs_inner = dict(colors=col_inner, startangle=180, autopct="%1.1f%%", wedgeprops=dict(width=width, edgecolor='white'))
    kwargs_middle = dict(colors=col_middle, startangle=180, autopct="%1.1f%%", wedgeprops=dict(width=width, edgecolor='white'))
    kwargs_outer = dict(colors=col_outer, startangle=180, autopct="%1.1f%%", wedgeprops=dict(width=width, edgecolor='white'))

    # Plotting the inner pie
    outside_inner, _, _ = plt.pie(sizes_inner, radius=radius-width, pctdistance=0.72, **kwargs_inner)

    # Plotting the middle pie
    outside_middle, _, _ = plt.pie(sizes_middle, radius=radius, pctdistance=0.82, **kwargs_middle)

    # Plotting the outer pie
    outside_outer, _, _ = plt.pie(sizes_outer, radius=radius+width, pctdistance=0.9, labels=labels, **kwargs_outer)

    if show_plots:
        plt.tight_layout()
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(f"{DATASET_PATH}stats/03_subjects_distribution.png")
        plt.close()

    
def main():
    get_raw_stats()
    with open(DATASET_PATH + 'stats/raw_stats.json', 'r') as file:
        data = json.load(file)
    
    topics_generated = 0
    for file in os.listdir(DATASET_PATH + 'topics'):
        if file.endswith('.json'):
            with open(DATASET_PATH + 'topics/' + file, 'r') as f:
                content = json.load(f)
                topics = next(iter(content.values()))
                topics_generated += len(topics)
    print(f"Total Topics Generated: {topics_generated}")
    
    elements_data = data["element_counts"]
    subject_data = data["file_counts"]
    
    total_slides = elements_data["slides"]
    total_elements = elements_data["elements"]
    total_PPTs = subject_data["total_PPTs"]
    
    print(f"Total PPTs Generated: {total_PPTs}")
    print(f"Total Slide Images: {total_slides}")
    print(f"Total Elements: {total_elements}")
    print(f"Average Elements per Slide: {total_elements/total_slides:.2f}")
    elements_count = {
        key: value for key, value in elements_data.items() if "_elements" in key}
    for key in elements_count.keys():
        if key in elements_data:
            del elements_data[key]
    elements_per_slide = dict(sorted(elements_count.items(), key=lambda item: int(item[0].split("_")[0])))
    
    
    del elements_data["slides"]
    del elements_data["elements"]
    del subject_data["subjects"]
    del subject_data["total_PPTs"]
    


    # Elements Distribution Bar Chart
    plt.figure(figsize=(8, 6))
    bars = plt.bar(elements_data.keys(), elements_data.values())
    plt.xlabel("Element Type")
    plt.ylabel("Frequency")
    plt.title("Elements Distribution in Dataset")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
    if show_plots:
        plt.tight_layout()
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(f"{DATASET_PATH}stats/01_elements_distribution.png")
        plt.close()

    # Subject Distribution Pie Chart
    subject_labels = list(subject_data.keys())
    subject_values = [sum(subject_data[subject].values()) for subject in subject_data]  # Total PPTs + images per subject
    plt.figure(figsize=(8, 6))
    plt.pie(subject_values, labels=subject_labels, autopct="%1.1f%%")  # Show percentage labels
    plt.title("Subject Distribution in Dataset")
    if show_plots:
        plt.tight_layout()
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(f"{DATASET_PATH}stats/02_subject_distribution.png")
        plt.close()

    subject_labels = list(subject_data.keys())
    topic_counts = [subject_data[subject]["topics"] for subject in subject_data]
    ppts_counts = [subject_data[subject]["PPTs"] for subject in subject_data]
    image_counts = [subject_data[subject]["images"] for subject in subject_data]
    subject_colors = [
        (0, 128, 64),  # Teal (Base 1)
        (255, 128, 0),  # Orange (Base 2)
        (128, 0, 128),  # Purple (Base 3)
        (0, 174, 239)]  # Blue (Base 4)
    topic_colors = [
        (102, 204, 102),  # Light Teal (Tint 1)
        (255, 192, 128),  # Light Orange (Tint 2)
        (192, 128, 192),  # Light Purple (Tint 3)
        (102, 179, 255)]  # Sky Blue (Tint 4)
    ppt_colors = [
        (0, 102, 51),  # Dark Teal (Shade 1)
        (204, 102, 0),  # Dark Orange (Shade 2)
        (102, 0, 102),  # Dark Purple (Shade 3)
        (0, 102, 153)]  # Dark Blue (Shade 4)

    make_triple_pie(topic_counts, ppts_counts, image_counts, topic_colors, ppt_colors, subject_colors, subject_labels)
    
    # Histogram of Elements counts per slide
    plt.figure(figsize=(8, 6))
    plt.title("Distribution of Elements per Slide")
    plt.xlabel("Number of Elements")
    plt.ylabel("Frequency")
    bars = plt.bar(elements_per_slide.keys(), elements_per_slide.values())
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    if show_plots:
        plt.tight_layout()
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(f"{DATASET_PATH}stats/04_elements_frequency.png")
        plt.close()

if __name__ == '__main__':
    main()
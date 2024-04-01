import json
import os
from openai import OpenAI
import random
from dotenv import load_dotenv, find_dotenv
import base64
from IPython.display import Image
import requests
from PIL import Image
from io import BytesIO

def fetch_slide_summaries(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        slide_summaries = json.load(file)
    return slide_summaries

# def generate_image(ppt_id, summary):
def generate_image():
    load_dotenv(find_dotenv())
    print(os.environ['OPENAI_API_KEY'])
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    text_response = client.completions.create(
        model="text-davinci-003",
        prompt="A graph to explain BFS search algorithm. It has 7 nodes.",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    # prompt = f"""A textbook illustration of Natural Language Processing (NLP) steps, from raw text to a machine learning model.
    #     Each step should be label."""
    # prompt = f"""A page from any textbook that explains the concept of Natural Language Processing (NLP) in a simple and easy-to-understand manner."""
    prompt = f""" A graph to explain BFS search algorithm. It has 7 nodes."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(image_url)
    
    # response = client.images.create_variation(
    #     image=open("code/assets/nlp_4.png", "rb"),
    #     n=2,
    #     size="1024x1024"
    # )
    # image_url = response.data[0].url
    # print(image_url)
    

def main():
    # slide_summaries = fetch_slide_summaries("code\data\slide_summary_sample.json")
    
    # for ppt_id, summary_data in slide_summaries.items():
    #     summary = summary_data["glensOcr"]    
    #     generate_image(ppt_id, summary)
    generate_image()

if __name__ == "__main__":
    main()
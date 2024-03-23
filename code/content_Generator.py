import json
import os
from openai import OpenAI
import random
from dotenv import load_dotenv, find_dotenv

def fetch_slide_summaries(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        slide_summaries = json.load(file)
    return slide_summaries

def generate_slide_content(ppt_id, summary):
    load_dotenv(find_dotenv())
    print(os.environ['OPENAI_API_KEY'])
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    MAX_TITLE_WORDS = 3
    MAX_DESCRIPTION_WORDS = 20
    MAX_ENUM_POINTS = 8
    # prompt = f"""Given the summary: '{summary}', generate a JSON object for a slide with the following structure:
    # \n\n{{\n    \"slide_id\": \"{slide_id}\",\n    \"title\": \"<content of the title>\",\n    \"description\": \"<content of the description>\",\n    \"enumeration\": [\"<content of pt 1>\", \"<content of pt 2>\", ...]\n}}
    # \n\nFollow these instructions while generating the content:
    # \n1. For every slide there should be only one title and it be between 1 to {MAX_TITLE_WORDS} words long.
    # \n2. For every slide there should be only one description and it has to be between 5 to {MAX_DESCRIPTION_WORDS} words long.
    # \n3. For every slide there should be only one enumeration. The content in the enumeration should be generated in form of points such that there are between 3 to {MAX_ENUM_POINTS} points for the enumeration. Each point in the enumeration should have between 1 to 3 words.
    # \n\nPlease provide the content for each element described by the <> brackets and do not provide any other output other than the JSON file"
    # """
    
    # make a prompt in similar format as above for 5 slides
    prompt = f"""First slide content : {summary}. JSON object structure:
    \n\n{{
        \"{ppt_id}\" : [
        {{  \"slide_id\": \"001\", 
            \"content\": {{ \"title\": \"<content of the title>\", \"description\": \"<content of the description>\", \"enumeration\": [\"<content of pt 1>\", \"<content of pt 2>\", ...]}}
        }},
        {{  \"slide_id\": \"002\", 
            \"content\": {{ \"title\": \"<content of the title>\", \"description\": \"<content of the description>\", \"enumeration\": [\"<content of pt 1>\", \"<content of pt 2>\", ...]}}
        }},
        ...
        ]
    }}
    Provided the content for first slide, generate the content for slide_01, slide_02, slide_03, slide_04 and slide_05 in the JSON object structure provided.
    Slide 1 will contain the content provided by user, generate the content for 2 to 5th slide."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professor's assistant for an educational course. Your role is to generate presentation slide content given the summary of a slide. You should generate meaningful content that can be used in a classroom slide"},
            {"role": "user", "content": prompt}
            ])
    return response.choices[0].message.content

def parse_generated_content(content):
    try:
        slide_content = json.loads(content)
        return slide_content
    except json.JSONDecodeError:
        print("Error: The generated content could not be parsed as JSON.")
        return None

def save_slide_content_to_json(ppt_id, slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)
    

def main():
    slide_summaries = fetch_slide_summaries("code\data\slide_summary_sample.json")
    
    # run the loop for any 5 random data items from the seed content json file
    for ppt_id, summary_data in slide_summaries.items():
        summary = summary_data["glensOcr"]
    # for i in range(5):
        # ppt_id = random.choice(list(slide_summaries.keys()))
        # summary = slide_summary[ppt_id]["glensOcr"]
        
        generated_content = generate_slide_content(ppt_id, summary)
        slide_content = parse_generated_content(generated_content)
        if slide_content:
            file_path = f"code/buffer/{ppt_id}.json"
            save_slide_content_to_json(ppt_id, slide_content, file_path)

if __name__ == "__main__":
    main()
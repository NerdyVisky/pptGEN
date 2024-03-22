# import json
# import os
# from openai import OpenAI
# import random

# client = OpenAI(
#     api_key="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",
# )

# def read_json_data(filename):
#   with open(filename, 'r', encoding='utf-8') as f:
#     return json.load(f)

# data = read_json_data("data/seed_Content.json")

# def pptGEN():
#   for i in range(5):
#     # pick any random key from the seed content json file
#     target_id = random.choice(list(data.keys()))
#     ocr_value = data[str(target_id)].get("glensOcr")
#     prompt_data = ocr_value

#     prompt = f"""You are an assistant for educational content generation.

#     The user will provide the content for first slide. You have to generate the content for 5 slides based on the given content.

#     First slide content : {prompt_data}

#     Desired hierarchy of JSON is given:
#         {target_id}:[
#             slide_01: [
#                 slide_title: ,
#                 text:
#             ],
#             slide_02: [
#                 slide_title: ,
#                 text:
#             ]
#         ]
#     I have provided outline, you have to fill the content for slide_01, slide_02, slide_03, slide_04 and slide_05. Each key value pair and target_id should be in double quotes.
#     Here, {target_id} is ID of ppt, and slide_no is the slide number. slide_title is the title of the slide and text is the content of the slide. Slide 1 will be the content I provided, generate the content for 2 to 5th slide.
#     """

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#           {"role": "user", "content":prompt}
#         ],
#     )

#     generated_text = response.choices[0].message.content
#     print(generated_text)
#     jso = json.loads(generated_text)
#     print(jso)
    
#     if os.path.exists("data/generated_content.json") and os.path.getsize("data/generated_content.json") > 0:
#       with open("data/generated_content.json", 'r') as json_file:
#         existing_data = json.load(json_file)
#     else:
#       existing_data = []
#     existing_data.append(jso)
#     with open('data/generated_content.json', 'w') as f:
#       json.dump(existing_data, f, indent=4)
      
# pptGEN()



import json
import os
from openai import OpenAI
import random
from dotenv import load_dotenv, find_dotenv

# OpenAI API key
# load_dotenv(find_dotenv())  
# api_key = os.environ.get("OPENAI_API_KEY")


def fetch_slide_summaries(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_summaries = json.load(file)
    return slide_summaries

def generate_slide_content(slide_id, summary):
    load_dotenv(find_dotenv())
    # Load the .env file
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
    prompt = f"""Given the summary: '{summary}', generate a JSON object for a slide with the following structure:
    \n\n{{\n    \"slide_id\": \"{slide_id}\",\n    \"title\": \"<content of the title>\",\n    \"description\": \"<content of the description>\",\n    \"enumeration\": [\"<content of pt 1>\", \"<content of pt 2>\", ...]\n}}
    \n\nFollow these instructions while generating the content:
    \n1. For every slide there should be only one title.
    \n2. For every slide there should be only one description.
    \n3. For every slide there should be only one enumeration. The content in the enumeration should be generated in form of points.
    \n\nPlease provide the content for each element described by the <> brackets and do not provide any other output other than the JSON file"
    """
    # prompt = f"""You are an assistant for educational content generation.
    # The user will provide the content for first slide. You have to generate the content for 5 slides based on the given content.
    # First slide content : {summary}
    # Desired hierarchy of JSON is given:
    #     {slide_id}:[
    #         slide_01: [
    #             slide_title: ,
    #             text:
    #         ],
    #         slide_02: [
    #             slide_title: ,
    #             text:
    #         ]
    #     ]
    # I have provided outline, you have to fill the content for slide_01, slide_02, slide_03, slide_04 and slide_05. Each key value pair and target_id should be in double quotes.
    # Here, {slide_id} is ID of ppt, and slide_no is the slide number. slide_title is the title of the slide and text is the content of the slide. Slide 1 will be the content I provided, generate the content for 2 to 5th slide.
    # """

    
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

def save_slide_content_to_json(slide_id, slide_content, file_path):
    slide_content_dict = {
        "slide_id": slide_id,
        "title": slide_content["title"],
        "description": slide_content["description"],
        "enumeration": slide_content["enumeration"],
    }
    with open(file_path, 'w') as json_file:
        json.dump(slide_content_dict, json_file, indent=3)

def main():
    slide_summaries = fetch_slide_summaries("code/data/slide_summary_sample.json")
    for slide_id, summary_data in slide_summaries.items():
        summary = summary_data["glensOcr"]
        generated_content = generate_slide_content(slide_id, summary)
        slide_content = parse_generated_content(generated_content)
        if slide_content:
            file_path = f"code/buffer/{slide_id}.json"
            save_slide_content_to_json(slide_id, slide_content, file_path)

if __name__ == "__main__":
    main()
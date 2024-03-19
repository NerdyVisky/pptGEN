import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os



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
    prompt = f"""Given the summary: '{summary}', generate a JSON object for a slide with the following structure:
    \n\n{{\n    \"slide_id\": \"{slide_id}\",\n    \"title\": \"<content of the title>\",\n    \"description\": \"<content of the description>\",\n    \"enumeration\": [\"<content of pt 1>\", \"<content of pt 2>\", ...]\n}}
    \n\nFollow these instructions while generating the content:
    \n1. For every slide there should be only one title and it be between 1 to {MAX_TITLE_WORDS} words long.
    \n2. For every slide there should be only one description and it has to be between 5 to {MAX_DESCRIPTION_WORDS} words long.
    \n3. For every slide there should be only one enumeration. The content in the enumeration should be generated in form of points such that there are between 3 to {MAX_ENUM_POINTS} points for the enumeration. Each point in the enumeration should have between 1 to 3 words.
    \n\nPlease provide the content for each element described by the <> brackets and do not provide any other output other than the JSON file"
    """
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
        summary = summary_data["summary"]
        generated_content = generate_slide_content(slide_id, summary)
        slide_content = parse_generated_content(generated_content)
        if slide_content:
            file_path = f"code/buffer/{slide_id}.json"
            save_slide_content_to_json(slide_id, slide_content, file_path)

if __name__ == "__main__":
    main()
import json
import os
from openai import OpenAI
import random

client = OpenAI(
    api_key="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",
)

def read_json_data(filename):
  with open(filename, 'r', encoding='utf-8') as f:
    return json.load(f)

data = read_json_data("data/seed_Content.json")

def pptGEN():
  for i in range(5):
    # pick any random key from the seed content json file
    target_id = random.choice(list(data.keys()))
    ocr_value = data[str(target_id)].get("glensOcr")
    prompt_data = ocr_value

    prompt = f"""You are an assistant for educational content generation.

    The user will provide the content for first slide. You have to generate the content for 5 slides based on the given content.

    First slide content : {prompt_data}

    Desired hierarchy of JSON is given:
        {target_id}:[
            slide_01: [
                slide_title: ,
                text:
            ],
            slide_02: [
                slide_title: ,
                text:
            ]
        ]
    I have provided outline, you have to fill the content for slide_01, slide_02, slide_03, slide_04 and slide_05. Each key value pair and target_id should be in double quotes.
    Here, {target_id} is ID of ppt, and slide_no is the slide number. slide_title is the title of the slide and text is the content of the slide. Slide 1 will be the content I provided, generate the content for 2 to 5th slide.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content":prompt}
        ],
    )

    generated_text = response.choices[0].message.content
    print(generated_text)
    jso = json.loads(generated_text)
    print(jso)
    
    if os.path.exists("data/generated_content.json") and os.path.getsize("data/generated_content.json") > 0:
      with open("data/generated_content.json", 'r') as json_file:
        existing_data = json.load(json_file)
    else:
      existing_data = []
    existing_data.append(jso)
    with open('data/generated_content.json', 'w') as f:
      json.dump(existing_data, f, indent=4)
      
pptGEN()

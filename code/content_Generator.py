import json
import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
)

def read_json_data(filename):
  with open(filename, 'r', encoding='utf-8') as f:
    return json.load(f)
data = read_json_data("data/seed_Content.json")

# read the OCR of slides
# for key, value in data.items():
#   glens_ocr_value = value.get("glensOcr")
#   if glens_ocr_value:
#     print(f"ID: {key}, glensOcr: {glens_ocr_value}")

# Specify the ID you want the glensOcr value for
target_id = "11111"
ocr_value = data[target_id].get("glensOcr")

prompt_data = ocr_value

prompt = f"""You are an assistant for educational content generation.

The user requests to generate the content for 5 slides based on the following content for the first slide:

{prompt_data}

Please provide the content in JSON format, with ppt_id, slide_id, slide_title and text as the elements."""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # prompt=prompt
    messages=[
      {"role": "user", "content":prompt}
    ],
    # response_format={ "type": "json_object" }
)

generated_text = response.choices[0].message.content
jso = json.loads(generated_text)

with open('data/generated_content.json', 'w') as f:
  json.dump(jso, f, indent=4)


import json

# Function to read data from a JSON file
def read_json_data(filename):
  with open(filename, 'r') as f:
    return json.load(f)

# Function to write data to a JSON file
def write_json_data(data, filename):
  with open(filename, 'w') as f:
    json.dump(data, f, indent=4)

# Read data from the JSON file
data = read_json_data("slide_summary.json")

prompt_data = data["key"]

# Construct the prompt with the data
prompt = f"""You are a helpful assistant.

The user says: Hello!

Based on the information provided, {prompt_data}"""

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    prompt=prompt
)

# Extract the response
response = completion.choices[0].message

write_json_data({"response": response}, "content_API.json")

print(response)

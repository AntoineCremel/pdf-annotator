import json

with open("data/AttestationDroits_du_13-08-2018 (1) (2)output-1-to-1.json", "r") as json_file:
    content = json_file.read()

content = json.loads(content)
second_page = content['responses'][0]
text = second_page['fullTextAnnotation']['text']

print(text)
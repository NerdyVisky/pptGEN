import json
import os
from bs4 import BeautifulSoup

ppt = 'ppts/1.pptx'
folder = 'ppts/xml1'
json_file = 'ppts/1.json'
images = os.listdir('ppts/1ff07c/1/')

def get_xml(id):
    return f'{folder}/ppt/slides/slide{id}.xml'

def get_rel(id):
    return f'{folder}/ppt/slides/_rels/slide{id}.xml.rels'

def get_xml_data(xml_path):
    with open(xml_path, 'r') as file:
        data = file.read()
    return data

def get_json_data(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def main():
    json_data = get_json_data(json_file)
    for i, slide in enumerate(json_data['slides']):
        xml_path = get_xml(i+1)
        rel_path = get_rel(i+1)
        rel_data = BeautifulSoup(get_xml_data(rel_path), 'xml')
        xml_data = BeautifulSoup(get_xml_data(xml_path), 'xml')
        relationship = rel_data.find('Relationship')
        target = relationship['Target'] if relationship else None
        path = f'{folder}/ppt/{target[3:]}'
        layout_data = BeautifulSoup(get_xml_data(path), 'xml') if target else None
        
        # play with data here
        
        
        
        break
        
        
if __name__ == '__main__':
    main()
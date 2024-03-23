from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import json
import os

class Element:
    def __init__(self, content, style, bounding_box):
        self.content = content
        self.style = style
        self.bounding_box = bounding_box
    
    def apply_font_style_on_run(self, run):
        if 'font_name' in self.style:
            run.font.name = self.style['font_name']
        if 'font_size' in self.style:
            run.font.size = Pt(self.style['font_size'])
        if 'font_color' in self.style:
            run.font.color.rgb = RGBColor(self.style['font_color']['r'], self.style['font_color']['g'], self.style['font_color']['b'])
        if 'bold' in self.style:
            run.font.bold = self.style['bold']
        if 'italics' in self.style:
            run.font.italic = self.style['italics']
        if 'underlined' in self.style:
            run.font.underline = self.style['underlined']

    
    def apply_font_style(self, shape):
        if 'font_name' in self.style:
            shape.text_frame.paragraphs[0].font.name = self.style['font_name']
        if 'font_size' in self.style:
            shape.text_frame.paragraphs[0].font.size = Pt(self.style['font_size'])
        if 'font_color' in self.style:
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(self.style['font_color']['r'], self.style['font_color']['g'], self.style['font_color']['b'])
        if 'bold' in self.style:
            shape.text_frame.paragraphs[0].font.bold = self.style['bold']
        else:
            shape.text_frame.paragraphs[0].font.bold = False 
        if 'italics' in self.style:
            shape.text_frame.paragraphs[0].font.italic = self.style['italics']
        else:
            shape.text_frame.paragraphs[0].font.italic = False 
        if 'underlined' in self.style:
            shape.text_frame.paragraphs[0].font.underline = self.style['underlined']
        else:
            shape.text_frame.paragraphs[0].font.underline = False
    
    def position_element(self, shape):
        shape.left = Inches(self.bounding_box[0])
        shape.top = Inches(self.bounding_box[1])
        shape.width = Inches(self.bounding_box[2])
        shape.height = Inches(self.bounding_box[3])

        if shape.has_text_frame:
            shape.text_frame.margin_left = Pt(5)
            shape.text_frame.margin_right = Pt(5)
            shape.text_frame.margin_top = Pt(5)
            shape.text_frame.margin_bottom = Pt(5)


    def render(self, slide):
        raise NotImplementedError("Subclasses must implement this method")

class Title(Element):
    def render(self, slide):
        print(slide.shapes.title)
        title_shape = slide.shapes.title
        # self.position_element(title_shape)
        title_shape.text = self.content
        self.apply_font_style(title_shape)
        self.position_element(title_shape)
        title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    def clean_up(self, slide):
        pass

class Description(Element):
    def render(self, slide):
        left, top, width, height = self.bounding_box
        textbox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        # textbox.text = self.content
        # self.apply_font_style(textbox)
        lines = self.content.split('\n')
        # Add each line as a separate paragraph with its own run
        for line in lines:
            paragraph = textbox.text_frame.add_paragraph()
            run = paragraph.add_run()
            run.text = line
            self.apply_font_style_on_run(run)
        # Store the textbox for later clean-up
        textbox.text_frame.auto_size = True
        textbox.text_frame.word_wrap = True 
        self.position_element(textbox)
        self.textbox = textbox

class Enumeration(Description):
    def render(self, slide):
        left, top, width, height = self.bounding_box
        textbox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        text_frame = textbox.text_frame
        for i, point_text in enumerate(self.content):
            p = text_frame.add_paragraph()
            run = p.add_run()
            run.text = "• " + point_text
            self.apply_font_style_on_run(run)
        textbox.text_frame.auto_size = True
        textbox.text_frame.word_wrap = True
        self.position_element(textbox)
        self.textbox = textbox
            

class Figure(Element):
    def render(self, slide):
        left, top, width, height = self.bounding_box
        img = slide.shapes.add_picture(self.content, Inches(left), Inches(top), Inches(width), Inches(height))
        # original_width, original_height = img.image.size
        # # Convert dimensions from pixels to inches
        # img.width = Inches(original_width * scale_factor / img.image.dpi[0])
        # img.height = Inches(original_height * scale_factor / img.image.dpi[1])
        self.image = img 

class PresentationGenerator:
    def __init__(self, json_payload, ppt_id):
        self.json_payload = json_payload
        self.ppt_id = ppt_id
        self.presentation = Presentation()

    def generate_presentation(self):
        for slide_info in self.json_payload['slides']:
            slide_layout = self.presentation.slide_layouts[0]
            slide = self.presentation.slides.add_slide(slide_layout)
            slide.background.fill.solid()
            if slide_info['bg_color']:
                slide.background.fill.fore_color.rgb = RGBColor(slide_info['bg_color']['r'], slide_info['bg_color']['g'], slide_info['bg_color']['b'])
            else:
                slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

            for element_type, elements in slide_info['elements'].items():
                for element_info in elements:
                    if element_type == 'figure':
                        element = Figure(element_info['path'], None, (element_info['xmin'], element_info['ymin'], element_info['width'], element_info['height']))
                    elif element_type == 'description':
                        if element_info['label'] == "enumeration":
                            element = Enumeration(element_info['value'], element_info['style'], (element_info['xmin'], element_info['ymin'], element_info['width'], element_info['height']))
                        else:
                            element = Description(element_info['value'], element_info['style'], (element_info['xmin'], element_info['ymin'], element_info['width'], element_info['height']))
                    elif element_type == 'title':
                        print(element_info['value'])
                        element = Title(element_info['value'], element_info['style'], (element_info['xmin'], element_info['ymin'], element_info['width'], element_info['height']))
                    else:
                        raise ValueError(f"Unsupported element type: {element_type}")

                    element.render(slide)

    
        # Clean-up empty elements
        for slide in self.presentation.slides:
            for shape in slide.shapes:
                # print(shape.shape_type)
                if shape.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER:
                    if not shape.text_frame.text:
                        sp = slide.shapes._spTree
                        sp.remove(shape._element)
        
        ppts_path = "./ppts/"
        if os.path.isdir(ppts_path) == False:
            print("false")
            os.mkdir(ppts_path)

        self.presentation.save(os.path.join(ppts_path, f'{self.ppt_id}.pptx'))

def load_json_payload(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    # Load the JSON payload
    buffer_folder_path = "./code/buffer/full"
    base_topic_folder_path = "./code/json"

    json_files = [f for f in os.listdir(buffer_folder_path) if f.endswith('.json')]

    for json_file in json_files:
        #Load JSON file from buffer
        ppt_id , _ = os.path.splitext(json_file)
        json_file_path = os.path.join(buffer_folder_path, json_file)
        json_payload = load_json_payload(json_file_path)

        # print(json_payload)
        
        
        #Generate Presentation from JSON file and save it
        presentation_generator = PresentationGenerator(json_payload, ppt_id)
        presentation_generator.generate_presentation()
        print(f"Presentation generated successfully for {ppt_id}.")

        #Move JSON file from buffer to respective topic folder
        # if not os.path.exists(base_topic_folder_path):
        #     os.makedirs(base_topic_folder_path)

        # destination_file_path = os.path.join(base_topic_folder_path, json_file)
        # os.rename(json_file_path, destination_file_path)
        # print(f"Moved {json_file} to {base_topic_folder_path}.")
        # print('\n')
    
    print("All presentations generated and files moved successfully.")

if __name__ == "__main__":
    main()
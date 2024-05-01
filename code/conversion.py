from pptxtopdf import convert
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import fitz
import os
import json
import io
      
ppt_path = 'ppts/'
pdf_path = 'pdfs/'
image_path = 'images/'
json_path = 'code/json/'

# Currently, the code only converts pptx to pdf and pdf to images
# Will change for mass conversion later

# PPTX to PDF
for ppt in os.listdir(ppt_path):
  if ppt.endswith('.pptx'):
    convert(ppt_path + ppt, pdf_path + ppt[:-5] + '.pdf')
    
# PDF to Image
for pdf in os.listdir(pdf_path):
  if pdf.endswith('.pdf'):
    images = convert_from_path(pdf_path + pdf)
    for i, image in enumerate(images):
      image_resized = image.resize((800, 600))
      image.save(image_path + pdf[:-4] + '/page' + str(i) + '.png', 'PNG')

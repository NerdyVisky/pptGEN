from pptxtopdf import convert
from pdf2image import convert_from_path
import os

def main():
  if not os.path.exists('dataset/images'):
    os.makedirs('dataset/images')
  if not os.path.exists('dataset/pdfs'):
    os.makedirs('dataset/pdfs')
  if not os.path.exists('dataset/json'):
    os.makedirs('dataset/json')
  
  ppt_path = 'ppts/'
  pdf_path = 'dataset/pdfs/'
  img_path = 'dataset/images/'

  # PPTX to PDF
  for ppts in os.listdir(ppt_path):
    for ppt in os.listdir(ppt_path + ppts):
      if ppt.endswith('.pptx'):
          print(ppt_path + ppts + '/' + ppt)
          convert(ppt_path + ppts + '/' + ppt, pdf_path + ppts + '/')
      
  # PDF to Image
  for pdfs in os.listdir(pdf_path):
    for pdf in os.listdir(pdf_path + pdfs):
      if pdf.endswith('.pdf'):
        print(pdf_path + pdfs + '/' + pdf)
        images = convert_from_path(pdf_path + pdfs + '/' + pdf)
        for i, image in enumerate(images):
          image_path = img_path + pdfs + '/' + pdf[:-4]
          print(image_path)
          if not os.path.exists(image_path):
            os.makedirs(image_path)
          image_resized = image.resize((1280, 720))
          image_resized.save(image_path + '/slide' + str(i) + '.png', 'PNG')
        
  # Remove PDFs
  # for pdfs in os.listdir(pdf_path):
  #   for pdf in os.listdir(pdf_path + pdfs):
  #     if pdf.endswith('.pdf'):
  #       os.remove(pdf_path + pdfs + '/' + pdf)
  
        
if __name__ == '__main__':
  main()
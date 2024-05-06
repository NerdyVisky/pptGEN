from pptxtopdf import convert
from pdf2image import convert_from_path
import os

def main():
  if not os.path.exists('dataset/images'):
    os.makedirs('dataset/images')
  if not os.path.exists('dataset/pdfs'):
    os.makedirs('dataset/pdfs')

  ppt_path = 'dataset/ppts/'
  pdf_path = 'dataset/pdfs/'
  img_path = 'dataset/images/'

  # PPTX to PDF
  for ppt in os.listdir(ppt_path):
    if ppt.endswith('.pptx'):
      convert(ppt_path + ppt, pdf_path)
      
  # PDF to Image
  for pdf in os.listdir(pdf_path):
    if pdf.endswith('.pdf'):
      images = convert_from_path(pdf_path + pdf)
      for i, image in enumerate(images):
        image_path = img_path + pdf[:-4]
        if not os.path.exists(image_path):
          os.makedirs(image_path)
        image_resized = image.resize((1280, 720))
        image_resized.save(image_path + '/slide' + str(i) + '.png', 'PNG')
        
  # Remove PDFs
  for pdf in os.listdir(pdf_path):
    os.remove(pdf_path + pdf)
        
if __name__ == '__main__':
  main()
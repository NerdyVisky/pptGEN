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
  for subject in os.listdir(ppt_path):
    for topic in os.listdir(f"{ppt_path}{subject}"):
      for ppt in os.listdir(f"{ppt_path}{subject}/{topic}"):
        if ppt.endswith('.pptx'):
          print(f"{ppt_path}{subject}/{topic}/{ppt}")
          convert(f"{ppt_path}{subject}/{topic}/{ppt}", f"{pdf_path}{subject}/{topic}/")
      
  # PDF to Image
  for subject in os.listdir(pdf_path):
    print(subject)
    for topic in os.listdir(pdf_path + subject):
      print(topic)
      for pdf in os.listdir(pdf_path + subject + '/' + topic):
        if pdf.endswith('.pdf'):
          print(pdf_path + subject + '/' + topic + '/' + pdf)
          images = convert_from_path(pdf_path + subject + '/' + topic + '/' + pdf)
          for i, image in enumerate(images):
            image_path = img_path + subject + '/' + topic + '/' + pdf[:-4]
            print(image_path)
            if not os.path.exists(image_path):
              os.makedirs(image_path)
            image_resized = image.resize((1280, 720))
            image_resized.save(image_path + '/slide' + str(i) + '.png', 'PNG')
        
  # Remove PDFs
  # for subject in os.listdir(pdf_path):
  #   for topic in os.listdir(pdf_path + subject):
  #     for pdf in os.listdir(pdf_path + subject + '/' + topic):
  #       if pdf.endswith('.pdf'):
  #         os.remove(pdf_path + subject + '/' + topic + '/' + pdf)
  
  # move topics.json to dataset/
  os.rename('code/data/topics.json', 'dataset/topics.json')
        
if __name__ == '__main__':
  main()
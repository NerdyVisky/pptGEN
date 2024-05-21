from pptxtopdf import convert
from pdf2image import convert_from_path
import os
import datetime

def main():
  print("Running post processing module...")
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
          convert(f"{ppt_path}{subject}/{topic}/{ppt}", f"{pdf_path}{subject}/{topic}/")

  print(f"🟢 (1/5) All PPT files converted to PDF for processing")

  # PDF to Image
  for subject in os.listdir(pdf_path):
    for topic in os.listdir(pdf_path + subject):
      for pdf in os.listdir(pdf_path + subject + '/' + topic):
        if pdf.endswith('.pdf'):
          # print(pdf_path + subject + '/' + topic + '/' + pdf)
          images = convert_from_path(pdf_path + subject + '/' + topic + '/' + pdf)
          for i, image in enumerate(images):
            image_path = img_path + subject + '/' + topic + '/' + pdf[:-4]
            # print(image_path)
            if not os.path.exists(image_path):
              os.makedirs(image_path)
            image_resized = image.resize((1280, 720))
            image_resized.save(image_path + '/slide' + str(i) + '.png', 'PNG')
  print(f"🟢 (2/5) All images generated and saved to dataset/images")
       
  # Remove PDFs
  # for subject in os.listdir(pdf_path):
  #   for topic in os.listdir(pdf_path + subject):
  #     for pdf in os.listdir(pdf_path + subject + '/' + topic):
  #       if pdf.endswith('.pdf'):
  #         os.remove(pdf_path + subject + '/' + topic + '/' + pdf)
  
  # move topics.json to dataset/
  now = datetime.datetime.now()
  formatted_now = now.strftime("%H_%M_%d_%m")
  try:
    os.rename('code/data/topics.json', f'dataset/topics/{formatted_now}.json')
    print(f"🟢 (3/5) New batch of topics saved as dataset/topics/{formatted_now}.json")
  except:
    print(f"🔴 Error in moving topics to {formatted_now}.json")

        
if __name__ == '__main__':
  main()
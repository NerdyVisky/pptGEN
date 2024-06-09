from pptxtopdf import convert
from pdf2image import convert_from_path
import os
import datetime

def main():
  print("Running post processing module...")
  if not os.path.exists(f"dataset/images"):
    os.makedirs(f"dataset/images")
  if not os.path.exists(f"dataset/pdfs"):
    os.makedirs(f"dataset/pdfs")
  if not os.path.exists(f"dataset/json"):
    os.makedirs(f"dataset/json")
  
  ppt_dir = f"ppts/"
  pdf_dir = f"dataset/pdfs/"
  img_dir = f"dataset/images/"

  # PPTX to PDF
  a = 0
  for subject in os.listdir(ppt_dir):
    for topic in os.listdir(f"{ppt_dir}{subject}"):
      for ppt in os.listdir(f"{ppt_dir}{subject}/{topic}"):
        if ppt.endswith('.pptx'):
          convert(f"{ppt_dir}{subject}/{topic}/{ppt}", f"{pdf_dir}{subject}/{topic}/")
          a += 1

  print(f"🟢 (1/5) {a} PPT files converted to PDF for processing")

  # PDF to Image
  a = 0
  for subject in os.listdir(pdf_dir):
    for topic in os.listdir(pdf_dir + subject):
      for pdf in os.listdir(pdf_dir + subject + '/' + topic):
        if pdf.endswith('.pdf'):
          # print(pdf_dir + subject + '/' + topic + '/' + pdf)
          images = convert_from_path(pdf_dir + subject + '/' + topic + '/' + pdf)
          for i, image in enumerate(images):
            image_path = img_dir + subject + '/' + topic + '/' + pdf[:-4]
            # print(image_path)
            if not os.path.exists(image_path):
              os.makedirs(image_path)
            image_resized = image.resize((1280, 720))
            if i <= 9:
              id = '0' + str(i)
            else:
              id = str(i)
            image_name = image_path + '/' + id + pdf[:-4] + topic + '.png'
            # print(image_name)
            image_resized.save(image_name, 'PNG')
            a += 1
  print(f"🟢 (2/5) {a} images generated and saved to dataset/images")
       
  # Remove PDFs
  # for subject in os.listdir(pdf_dir):
  #   for topic in os.listdir(pdf_dir + subject):
  #     for pdf in os.listdir(pdf_dir + subject + '/' + topic):
  #       if pdf.endswith('.pdf'):
  #         os.remove(pdf_dir + subject + '/' + topic + '/' + pdf)
  #     os.rmdir(pdf)
  
  # move topics.json to dataset/
  now = datetime.datetime.now()
  formatted_now = now.strftime("%H_%M_%d_%m")
  try:
    os.rename(f"code/data/topics.json", f"dataset/topics/{formatted_now}.json")
    print(f"🟢 (3/5) New batch of topics saved as dataset/topics/{formatted_now}.json")
  except:
    print(f"🔴 Error in moving topics to {formatted_now}.json")

        
if __name__ == '__main__':
  main()
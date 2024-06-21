from pptxtopdf import convert
from pdf2image import convert_from_path
import os
import datetime
import contextlib
from tqdm import tqdm

@contextlib.contextmanager
def suppress_output():
    import sys
    import os
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

def convert_ppt_to_pdf(ppt_path, pdf_dir):
    convert(ppt_path, pdf_dir)

def convert_pdf_to_images(pdf_path, img_dir, subject, topic):
    images = convert_from_path(pdf_path)
    pdf_name = os.path.basename(pdf_path)[:-4]
    image_path = os.path.join(img_dir, subject, topic, pdf_name)
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    for i, image in enumerate(images):
        image_resized = image.resize((1280, 720))
        id = f'{i:02}'
        image_name = os.path.join(image_path, f'{id}{pdf_name}{topic}.png')
        image_resized.save(image_name, 'PNG')

def convert_ppt_to_images(ppt_path, pdf_output_dir, pdf_path, img_dir, subject, topic):
  if not os.path.exists(pdf_output_dir):
      os.makedirs(pdf_output_dir)
  convert_ppt_to_pdf(ppt_path, pdf_output_dir)
  convert_pdf_to_images(pdf_path, img_dir, subject, topic)


def main():
  print("Running post processing module...")
  os.makedirs("dataset/images", exist_ok=True)
  os.makedirs("dataset/pdfs", exist_ok=True)
  os.makedirs("dataset/json", exist_ok=True)

  ppt_dir = "ppts/"
  pdf_dir = "dataset/pdfs/"
  img_dir = "dataset/images/"

  # PPTX to PDF
  subjects = os.listdir(ppt_dir)
  print(subjects)
  for subject in subjects:
    # if subject == 'CS':
      for topic in tqdm(os.listdir(os.path.join(ppt_dir, subject)), desc="Processing topics"):
        for ppt in os.listdir(os.path.join(ppt_dir, subject, topic)):
          if ppt.endswith('.pptx'):
            ppt_path = os.path.join(ppt_dir, subject, topic, ppt)
            pdf_output_dir = os.path.join(pdf_dir, subject, topic)
            pdf_path = os.path.join(pdf_dir, subject, topic, ppt[:-4] + 'pdf')
            # check if pdf already exists
            if not os.path.exists(pdf_path):
              with suppress_output():
                convert_ppt_to_images(ppt_path, pdf_output_dir, pdf_path, img_dir, subject, topic)
                    
  
  

       
  # Remove PDFs
  # for subject in os.listdir(pdf_dir):
  #   for topic in os.listdir(pdf_dir + subject):
  #     for pdf in os.listdir(pdf_dir + subject + '/' + topic):
  #       if pdf.endswith('.pdf'):
  #         os.remove(pdf_dir + subject + '/' + topic + '/' + pdf)
  #     os.rmdir(pdf)
  
  # move topics.json to dataset/
  # now = datetime.datetime.now()
  # formatted_now = now.strftime("%H_%M_%d_%m")
  # try:
  #   os.rename(f"code/data/topics.json", f"dataset/topics/{formatted_now}.json")
  #   print(f"🟢 (3/5) New batch of topics saved as dataset/topics/{formatted_now}.json")
  # except:
  #   print(f"🔴 Error in moving topics to {formatted_now}.json")

        
if __name__ == '__main__':
  main()
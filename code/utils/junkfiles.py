import os
import shutil


SOURCE = f"ppts"
DESTINATION = f"dataset/pptfiles"

subjects = os.listdir(SOURCE)
for sub in subjects:
    sub_path = os.path.join(SOURCE, sub)
    ppts_in_sub = os.listdir(sub_path)
    for ppt in ppts_in_sub:
        # check if file exists at destination, if not, move it
        src = os.path.join(sub_path, ppt)
        dest = os.path.join(DESTINATION, sub, ppt)
        # print(src, dest)
        if not os.path.exists(dest):
            shutil.move(src, dest)
        #     # print(f"Moved {ppt} to {dest}")
print("PPT files saved and transferred.")

# parent_directories = [f"code/json/final", f"dataset/pdfs"]
# parent_directories = [f"code/buffer", f"code/temp", f"code/json/content", f"dataset/pdfs"]
parent_directories = [f"dataset/pdfs"]
def delete_subdirectories(parent_dirs):
    for parent_dir in parent_dirs:
        for item in os.listdir(parent_dir):
            if(item != 'full'):
                item_path = os.path.join(parent_dir, item)
                if os.path.isdir(item_path):
                    ppt_folders = os.listdir(item_path)
                    for ppt_folder in ppt_folders:
                        path = os.path.join(item_path, ppt_folder)
                        if(os.path.isdir(path)):
                            shutil.rmtree(path)
                            # print(f"Deleted directory: {path}")
                        elif(os.path.isfile(path)):
                            _, ext = os.path.splitext(path)
                            if ext.lower() == '.json':
                                os.remove(path)
                                # print(f"Deleted file: {path}")
    print("Temporary files discarded.")


# Example usage
delete_subdirectories(parent_directories)


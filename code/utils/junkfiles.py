import os
import shutil


SOURCE = f"ppts"
DESTINATION = f"dataset/pptfiles"

subjects = os.listdir(SOURCE)
for sub in subjects:
    sub_path = os.path.join(SOURCE, sub)
    ppts_in_sub = os.listdir(sub_path)
    for ppt in ppts_in_sub:
        shutil.move(f"{sub_path}/{ppt}", f"{DESTINATION}/{sub}")
print("PPT files saved and transferred.")

parent_directories = [f"code/json/final", f"dataset/pdfs"]
# parent_directories = ['code\\buffer', 'code\\temp', 'code\json\content', 'dataset\pdfs']
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


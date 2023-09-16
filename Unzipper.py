import zipfile
import os

folder_path = "E:/Dataset/"
destination_path = "E:/Dataset_Unzipped/"
for filename in os.listdir(folder_path):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(os.path.join(folder_path, filename), "r") as zip_ref:
            zip_ref.extractall(destination_path)
        print("The zip file " + filename + " has been extracted.")

print("All zip files in the folder have been extracted.")

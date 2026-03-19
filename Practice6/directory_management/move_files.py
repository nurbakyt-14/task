import shutil
import os

source = "../file_handling/sample.txt"
destination = "../sample.txt"

if os.path.exists(source):
    shutil.move(source, destination)
    print("Moved successfully")
else:
    print("File not found")
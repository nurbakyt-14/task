import os

# Create nested directories
os.makedirs("test/folder", exist_ok=True)
print("Directories created")

# List files and folders
print("\nFiles and folders:")
for item in os.listdir("."):
    print(item)
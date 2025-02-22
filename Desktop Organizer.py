import os
import shutil
import logging
from tqdm import tqdm

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

directory = input("Enter the directory to organize (leave empty for Desktop): ").strip()
directory = directory if directory else os.path.expanduser("~/Desktop")

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".dmg"],
}

if input("Do you want to add custom file categories? (yes/no): ").strip().lower() == "yes":
    while True:
        category = input("Enter category name (or press Enter to finish): ").strip()
        if not category:
            break
        extensions = input(f"Enter file extensions for {category} (comma-separated, e.g., .py, .js): ").strip().split(",")
        categories[category] = [ext.strip() for ext in extensions]
        print(f"Added category '{category}' with extensions: {categories[category]}")

for folder in categories:
    os.makedirs(os.path.join(directory, folder), exist_ok=True)

files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

for file in tqdm(files, desc="Organizing files", unit="file"):
    try:
        file_path = os.path.join(directory, file)
        file_ext = os.path.splitext(file)[1].lower()
        
        for folder, extensions in categories.items():
            if file_ext in extensions:
                shutil.move(file_path, os.path.join(directory, folder))
                logging.info(f"Moved: {file} → {folder}")
                break
    except Exception as e:
        logging.error(f"Failed to move {file}: {e}")

print("File organization completed.")

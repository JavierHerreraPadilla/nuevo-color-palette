"""
this file has a function to delete the images in the server everytime the page refreshes
based on the time
"""
import os
from pathlib import Path
import time

def delete_image(upload_folder: str):
    path = Path(upload_folder)
    img_paths = [Path(os.path.join(path, doc)) for doc in os.listdir(path)]
    for file in img_paths:
        if time.time() - os.path.getmtime(file) > 20:
            os.remove(file)

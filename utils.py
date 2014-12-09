'''
utils.py contains useful functions for collagen.

'''
import imghdr
import os
import os.path
import urllib.request
import shutil
import yaml

def is_image(input_path):
    return imghdr.what(input_path)

def delete_file(file_path):
    try:
        if imghdr.what(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

def delete_folder_files(folder):
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        try:
            if imghdr.what(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def download_url(url, folder_path):
    basename = os.path.basename(url)
    with urllib.request.urlopen(url) as response, open(os.path.join(folder_path, basename), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def get_ext(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[1]

def load_config():
    config_path = 'config.yml'
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)
    return config

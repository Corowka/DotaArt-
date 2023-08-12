import os

from data import create_images_database_json
from data import create_names_database_json

images_path = '../data/pics'
names_path = '../data/names/en_gpt_names.txt'
jsonImages_name = 'imagedata.json'
jsonNames_name = 'namedata.json'
json_path = '../data'
jsonImages_path = os.path.join(json_path, jsonImages_name)
jsonNames_path = os.path.join(json_path, jsonNames_name)

# create_images_database_json(images_path, jsonImages_path, json_path)
# create_names_database_json(names_path, jsonNames_path, json_path)
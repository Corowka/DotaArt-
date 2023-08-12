from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import uvicorn

from data import create_images_database_json
from data import create_names_database_json
from data import read_images_data_json
from data import read_names_data_json
from data import image_download
from data import tokenize_word
from data import tokenize_word_with_alph
from model import KNN
from features import calc_new_image_descriptor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

images_path = '../data/pics'
names_path = '../data/names.txt'
jsonImages_name = 'imagedata.json'
jsonNames_name = 'namedata.json'
json_path = '../data'
jsonImages_path = os.path.join(json_path, jsonImages_name)
jsonNames_path = os.path.join(json_path, jsonNames_name)

image_amount,\
    image_numbers,\
    image_descriptors,\
    image_constants,\
    image_extension = read_images_data_json(jsonImages_path, images_path)

name_amount, names, name_descriptors = read_names_data_json(jsonNames_path)

image_model = KNN(image_numbers, image_descriptors)
name_model = KNN(names, name_descriptors)

image_order = [[int(img), 1] for img in image_numbers]
name_order = [[str(name), 1] for name in names]


@app.get('/')
async def root():
    return {'status': 'model is ready'}


@app.get('/createImagesDataJson')
async def create_images_data():
    create_images_database_json(images_path, jsonImages_path, json_path)


@app.get('/createNamesDataJson')
async def create_names_data():
    create_names_database_json(names_path, jsonNames_path, json_path)


@app.get('/pagination/')
async def pagination(image_page, image_offset, image_skip, name_page, name_offset, name_skip):
    global image_order
    global name_order
    image_page, image_offset, image_skip, name_page, name_offset, name_skip = \
        int(image_page), int(image_offset), int(image_skip), int(name_page), int(name_offset), int(name_skip)
    return {
        'image_part': get_pagination_part(image_order, image_page, offset=image_offset, skip=image_skip),
        'name_part': get_pagination_part(name_order, name_page, offset=name_offset, skip=name_skip),
    }


@app.get('/search/')
async def search(url: str = '', name: str = ''):
    global image_order
    global name_order
    if url != '':
        img = image_download(url)
        if img is not None:
            image_descriptor = calc_new_image_descriptor(img, image_constants)
            image_order = image_model.calc_order(image_descriptor)
    if name != '':
        name_descriptor = tokenize_word(name)
        name_order = name_model.calc_order(name_descriptor)
    print(name_order[:5])
    return {
        'best_images': image_order[:3],
        'best_names': name_order[:15],
    }


def get_pagination_part(order, page, offset=24, skip=0):
    start = skip + offset * page
    end = start + offset
    part = order[start:end]
    return part


if __name__ == '__main__':
    uvicorn.run('api:app', port=8000, reload=True)
    
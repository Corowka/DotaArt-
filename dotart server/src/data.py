import json
import os
import numpy as np
import cv2
import requests
from tqdm import tqdm

from features import calc_image_descriptor

from features import tokenize_word
from features import tokenize_word_with_alph

from features import compute_mean
from features import compute_std
from features import compute_min_val
from features import compute_max_val
from features import normalize_descriptors
from features import min_max_scaling_descriptors
from features import weight_cld_descriptors
from features import replace_zeros_with_value
from features import normalize_vector


def create_images_database_json(images_path, json_name, json_save_path=''):

    # calc all
    image_numbers = []
    image_descriptors = []
    for i, image_name in tqdm(enumerate(sorted(os.listdir(images_path)))):
        img = cv2.imread(os.path.join(images_path, image_name))
        if img is None:
            continue
        image_numbers.append(int(image_name.split(sep='.')[0]))
        image_descriptors.append(calc_image_descriptor(img))

    image_descriptors = np.array(image_descriptors)

    mean = compute_mean(image_descriptors)
    std = compute_std(image_descriptors)
    min_val = compute_min_val(image_descriptors)
    max_val = compute_max_val(image_descriptors)
    cld_weight = 1
    zero_value = 1e-6

    image_descriptors = normalize_descriptors(image_descriptors, mean, std)
    image_descriptors = min_max_scaling_descriptors(image_descriptors, min_val, max_val)
    image_descriptors = weight_cld_descriptors(image_descriptors, cld_weight)
    for i, desc in enumerate(image_descriptors):
        image_descriptors[i] = normalize_vector(replace_zeros_with_value(desc, zero_value)).tolist()

    images_data = {
        'amount': len(image_descriptors),
        'constants': {
            'mean': mean.tolist(),
            'std': std.tolist(),
            'min': min_val.tolist(),
            'max': max_val.tolist(),
            'cld_weight': cld_weight,
            'zero_value': zero_value,
        },
        'numbers': image_numbers,
        'descriptors': image_descriptors.tolist(),
        'extension': '.jpg',
    }

    # save json
    with open(os.path.join(json_save_path, json_name), 'w') as json_file:
        json.dump(images_data, json_file)


def create_names_database_json(names_path, json_name, json_save_path=''):

    # calc all
    with open(names_path, "r", encoding="utf-8") as file:
        names = file.read()
    names = names.split(sep='\n')
    names = list(set(names))
    names = [_ for _ in names if len(_) > 0]

    tokens = []
    for i, name in tqdm(enumerate(sorted(names))):
        tokens.append(normalize_vector(tokenize_word(name)).tolist())

    names_data = {
        'amount': len(tokens),
        'names': names,
        'descriptors': tokens,
    }

    # save json
    with open(os.path.join(json_save_path, json_name), 'w') as json_file:
        json.dump(names_data, json_file)


def read_images_data_json(jsonfile_path, images_path):
    with open(jsonfile_path, 'r') as json_file:
        json_data = json_file.read()
        data = json.loads(json_data)
        amount = data['amount']
        numbers = np.array(data['numbers'])
        descriptors = np.array(data['descriptors'])
        constants = data['constants']
        extension = data['extension']

        # delete nums that's not exists
        mask = np.isin(numbers, np.array([_.split(sep='.')[0] for _ in os.listdir(images_path)]))
        numbers = numbers[mask]
        descriptors = descriptors[mask]

        return amount, numbers, descriptors, constants, extension


def read_names_data_json(jsonfile_path):
    with open(jsonfile_path, 'r') as json_file:
        json_data = json_file.read()
        data = json.loads(json_data)
        amount = data['amount']
        names = data['names']
        descriptors = np.array(data['descriptors'])

        return amount, names, descriptors


def image_download(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_array = np.frombuffer(response.content, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except requests.exceptions.RequestException as e:
        return None



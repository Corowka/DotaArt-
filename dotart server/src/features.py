import cv2
import numpy as np
from scipy.fftpack import dct


# Color Layout Desctiptor
def calc_cld(img: np.ndarray) -> np.ndarray:

    img = cv2.resize(img, (64, 64))
    avg = np.zeros((8, 8, 3), dtype=float)
    for i in range(64):
        for j in range(64):
            avg[i // 8][j // 8] += img[i][j]
    avg = (avg // 64).astype(np.uint8)
    avg = cv2.resize(avg, (64, 64))

    avgYCbCr = cv2.cvtColor(avg, cv2.COLOR_BGR2YCrCb)
    Y, Cb, Cr = cv2.split(avgYCbCr)

    Y_dct = np.zeros(64, dtype=float)
    Cb_dct = np.zeros(64, dtype=float)
    Cr_dct = np.zeros(64, dtype=float)
    for i in range(0, 64, 8):
        for j in range(0, 64, 8):
            Y_block = Y[i:i + 8, j:j + 8]
            Y_dct[(i // 8) * 8 + (j // 8)] = dct(Y_block)[0][0]
            Cb_block = Cb[i:i + 8, j:j + 8]
            Cb_dct[(i // 8) * 8 + (j // 8)] = dct(Cb_block)[0][0]
            Cr_block = Cr[i:i + 8, j:j + 8]
            Cr_dct[(i // 8) * 8 + (j // 8)] = dct(Cr_block)[0][0]

    cld = np.concatenate([Y_dct, Cb_dct, Cr_dct], axis=0)

    return cld


def calc_ehd(img: np.ndarray, threshold: np.uint16) -> np.ndarray:

    h, w, _ = img.shape
    cell_h, cell_w = h // 4, w // 4
    h, w = cell_h * 4, cell_w * 4
    img = cv2.resize(img, (h, w))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    conv = np.array([
        [1, -1,  1, -1],
        [1,  1, -1, -1],
        [1.41421, 0, 0, -1.41421],
        [0, 1.41421, -1.41421, 0],
        [2, -2, -2, 2]
    ])
    bins = np.zeros((17, 5), dtype=float)
    for i in range(0, h, cell_h):
        for j in range(0, w, cell_w):
            for x in range(i, i+cell_h-1, 2):
                for y in range(j, j+cell_w-1, 2):
                    block = np.array([img[y][x], img[y][x+1], img[y+1][x], img[y+1][x+1]])

                    block_bin = np.zeros(5)
                    for b in range(5):
                        block_bin[b] = np.sum(block * conv[b])

                    n = np.argmax(block_bin)
                    if block_bin[n] > threshold:
                        bins[(i*4+j)//cell_h][n] += 1

    T_bins = bins.T
    for b in range(5):
        bins[16][b] = np.mean(T_bins[b])

    return bins.flatten()


def calc_mhd(img: np.ndarray) -> np.ndarray:
    img = cv2.resize(img, (8, 8))
    return img.flatten()


def tokenize_word(word):
    fp = np.array([ord(c) for c in word])
    if len(fp) > 1:
        x = np.linspace(0, 32, 32)
        xp = np.linspace(0, 32, len(fp))
        return np.interp(x, xp, fp)
    else:
        return np.ones(32) * fp[0]


def tokenize_word_with_alph(word):
    alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.upper() + \
           'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + \
           'abcdefghijklmnopqrstuvwxyz'.upper() + \
           'abcdefghijklmnopqrstuvwxyz'
    fp = np.zeros(len(word))
    for i, _ in enumerate(word):
        if _ in alph:
            fp[i] = alph.index(_) + 1
        elif i == ' ':
            fp[i] = len(alph) + 11
        else:
            fp[i] = len(alph) + 21
    if len(fp) > 1:
        x = np.linspace(0, 32, 32)
        xp = np.linspace(0, 32, len(fp))
        return np.interp(x, xp, fp).tolist()
    else:
        return np.ones(32) * fp[0]


def compute_mean(descriptors: np.ndarray) -> np.ndarray:
    mean = np.mean(descriptors, axis=0)
    return mean


def compute_std(descriptors: np.ndarray) -> np.ndarray:
    std = np.std(descriptors, axis=0)
    return std


def compute_min_val(descriptors: np.ndarray) -> np.ndarray:
    min_val = np.min(descriptors, axis=0)
    return min_val


def compute_max_val(descriptors: np.ndarray) -> np.ndarray:
    max_val = np.max(descriptors, axis=0)
    return max_val


def normalize_descriptors(descriptors: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    normalized_descriptors = (descriptors - mean) / std
    return normalized_descriptors


def min_max_scaling_descriptors(descriptors: np.ndarray, min_val: np.ndarray, max_val: np.ndarray) -> np.ndarray:
    scaled_descriptors = (descriptors - min_val) / (max_val - min_val)
    return scaled_descriptors


def weight_cld_descriptors(descriptors: np.ndarray, cld_weight: float) -> np.ndarray:
    weights = np.ones(descriptors.shape)
    weights[:192] *= cld_weight
    weighted_descriptors = descriptors * weights
    return weighted_descriptors


def replace_zeros_with_value(arr: np.ndarray, value) -> np.ndarray:
    arr[arr == 0] = value
    return arr


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm != 0:
        normalized_vector = vector / norm
        return normalized_vector
    else:
        return vector


def calc_image_descriptor(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # return np.concatenate([calc_cld(img), calc_ehd(img, 30)], axis=0)
    return np.concatenate([calc_cld(img)], axis=0)


def calc_new_image_descriptor(img, constants):
    descriptor = np.array([calc_image_descriptor(img)])
    descriptor = normalize_descriptors(descriptor, np.array(constants['mean']), np.array(constants['std']))
    descriptor = min_max_scaling_descriptors(descriptor, np.array(constants['min']), np.array(constants['max']))
    descriptor = weight_cld_descriptors(descriptor, constants['cld_weight'])[0]
    descriptor = normalize_vector(replace_zeros_with_value(descriptor, constants['zero_value'])).tolist()
    return descriptor


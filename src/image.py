import requests
import numpy as np
from PIL import Image
from io import BytesIO
from scipy.spatial.distance import cdist

SCALE = 10
colors_rgb = [
    [255, 255, 255],
    [0, 0, 0],
    [255, 255, 255],    # [193, 193, 193], no light grey
    [76, 76, 76],
    [239, 19, 11],
    [116, 11, 7],
    [255, 113, 0],
    [194, 56, 0],
    [255, 228, 0],
    [232, 162, 0],
    [0, 204, 0],
    [0, 85, 16],
    [0, 178, 255],
    [0, 86, 158],
    [35, 31, 211],
    [14, 8, 101],
    [163, 0, 186],
    [85, 0, 105],
    [211, 124, 170],
    [167, 85, 116],
    [160, 82, 45],
    [99, 48, 13]
]


def load_image(url, size):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        im = thumbnail(img, size)
        return im
    except requests.exceptions.RequestException as e:
        print('Error: ' + e)
        return None


def thumbnail(img, size):
    im = img.copy()
    im.thumbnail(size)
    return im


def process_color(im):
    if im is None:
        return None
    test = np.array(im)
    if len(test.shape) == 3:
        if test.shape[2] == 4:
            test[test[..., -1] == 0] = [255, 255, 255, 0]
            img_np = np.delete(test, obj=3, axis=2)
        elif test.shape[2] != 3:
            img_np = np.array(im.convert('RGB'))
        else:
            img_np = test
    else:
        img_np = np.array(im.convert('RGB'))

    ih, iw = img_np.shape[:2]
    img_np = img_np.reshape((ih * iw, 3))
    col_np = np.array(colors_rgb, dtype=np.uint8).reshape(22, 3)
    res_np = np.empty((ih * iw, 3), dtype=np.uint8)
    res_dict = {}
    for i in range(len(colors_rgb)):
        res_dict[i] = np.zeros((ih, iw), dtype=bool)
    for i, p in enumerate(img_np):
        x, y = loc_by_ih_iw(i, iw)
        c = cdist(col_np, p.reshape(1, 3), metric='seuclidean').argmin()
        c = my_color_simplify_rules(c)
        res_np[i] = colors_rgb[c]
        if c == 0:
            continue
        res_dict[c][x, y] = True
    res_im = Image.fromarray(np.reshape(res_np, (ih, iw, 3)), mode='RGB')
    res_im.show()
    return res_dict


def loc_by_ih_iw(i, iw):
    return int(i / iw), (i % iw)


def my_color_simplify_rules(c):
    if c == 1 or c == 3:
        return 1
    elif c == 0 or c == 2:
        return 0
    elif 16 <= c <= 19:
        return 16
    else:
        return c - (c % 2)

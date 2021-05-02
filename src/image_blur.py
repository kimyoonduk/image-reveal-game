from PIL import Image
import math
import numpy as np
import json

from imutils import paths
import os

img_folder = "../data/t1_annotate/input/"
image_paths = sorted(list(paths.list_images(img_folder)))

for img_path in image_paths:

    img = Image.open(img_path)
    imgSmall = img.resize(
        (math.ceil(img.size[0] / 30), math.ceil(img.size[1] / 30)),
        resample=Image.BILINEAR,
    )
    # result = imgSmall.resize(img.size, Image.NEAREST)
    # result.save(new_path)

    new_path = img_path.replace(".jpg", "_blurred.json")

    img_np = np.asarray(imgSmall)
    img_json = {"size": [img_np.shape[0], img_np.shape[1]], "array": img_np.tolist()}

    with open(new_path, "w") as json_file:
        json.dump(img_json, json_file)


import pandas as pd
import json

# annotation file not included due to size
FOLDER_PATH = "./"
val_json = FOLDER_PATH + "instances_val2017.json"


def get_image(data, img_id):
    select_img = [img for img in data["images"] if img["id"] == img_id][0]
    return select_img


def get_annotations(data, img_id):
    select_anno = [anno for anno in data["annotations"] if anno["image_id"] == img_id]
    return select_anno


# get the "correct" boundaries of the object in the image
def get_coordinates(select_anno, category_id):
    select_coordinates = [
        anno["segmentation"]
        for anno in select_anno
        if anno["category_id"] == category_id
    ]

    return select_coordinates


def main():
    with open(val_json) as f:
        data = json.load(f)

    img_id = 22892
    # 'cat' has a category id of 17
    category_id = 17

    select_img = get_annotations(data, 22892)

    select_anno = [anno for anno in data["annotations"] if anno["image_id"] == 22892]

    # use this info for automatic filtering
    # each alternating value in the list corresponds to x and y coordinates respectively
    coordinates = get_coordinates(select_anno, category_id)


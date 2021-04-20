import pandas as pd
import json

# path to annotation metadata file
FOLDER_PATH = "../data/metadata/"
val_json = FOLDER_PATH + "meta.json"


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

    select_img = get_image(data, 22892)

    select_anno = [anno for anno in data["annotations"] if anno["image_id"] == 22892]

    # possible to automatically check if the worker clicked inside the polygon defined by the coordinates
    # each alternating value in the list corresponds to x and y coordinates respectively
    coordinates = get_coordinates(select_anno, category_id)

    t1_path = "../data/t1_annotate/output/sample_output_t1.csv"

    # raw sample for task 1
    # rows 1-3 contain correct annotations
    # row 4 is incorrect (dog)
    # row 5 is incorrect (random)
    t1_df = pd.read_csv(t1_path)

    t2_path = "../data/t2_guess/output/sample_output_t2.csv"

    # raw sample for task 2
    # row 4 is incorrect (random)
    # row 5 is incorrect (wrong input - annotation for dog)
    t2_df = pd.read_csv(t2_path)

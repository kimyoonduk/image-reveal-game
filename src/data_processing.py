import pandas as pd
import json
from numpy import mean
from numpy import percentile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from statistics import mode
import csv


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


def get_bbox(select_anno, category_id):
    bounding_box = [
        anno["bbox"] for anno in select_anno if anno["category_id"] == category_id
    ]
    return bounding_box


# raw sample for task 1
# rows 1-3 contain correct annotations
# row 4 is incorrect (dog)
# row 5 is incorrect (random)
# Task 1 Quality Control and Aggregation
def task1_qca(data, t1_df):
    worker_dictionary = {}
    bbox = None
    bbox_poly = None
    img_id = 0
    for index, row in t1_df.iterrows():
        # this is just a check to see if the img has changed, and if so, to grab new img_id and bounding box
        if row["img_id"] != img_id:
            img_id = row["img_id"]
            bbox = get_bbox(get_annotations(data, img_id), row["category_id"])[0]
            # Polygon is created upper left and then counter clock wise
            bbox_poly = Polygon(
                [
                    (bbox[0], bbox[1]),
                    (bbox[0], bbox[1] + bbox[3]),
                    (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                    (bbox[0] + bbox[2], bbox[1]),
                ]
            )
        # Run through each of the clicks and make a Point, and test if that Point is in the bounding box
        in_box = 0
        total = 0
        worker_id = row["WorkerId"]
        for i in range(1, 11):
            if str(row[f"point_{i}"]) != "nan":
                coordinates = str(row[f"point_{i}"]).split(",")
                point = Point(int(coordinates[0]), int(coordinates[1]))
                if bbox_poly.contains(point):
                    in_box += 1
                    total += 1
                else:
                    total += 1
        # Update existing worker qual, or create new item in dictionary
        if worker_id in worker_dictionary:
            in_not = worker_dictionary.get(worker_id)
            updated_in_not = [in_not[0] + in_box, in_not[1] + total]
            worker_dictionary[worker_id] = updated_in_not
        else:
            worker_dictionary[worker_id] = [in_box, total]
    lst = [(x, round(i[0] / i[1], 3)) for x, i in worker_dictionary.items()]
    return lst


# Task 2 Quality Control and Aggregation (Majority Vote)


def task2_qca(t2_df):
    lst = []
    final_guess = [""] * len(t2_df)
    for i in range(len(t2_df)):
        final_guess[i] = [
            str(t2_df[f"guess_{j}"][i])
            for j in range(1, 6)
            if str(t2_df[f"guess_{j}"][i]) != "nan"
        ][-1]
    t2_df["final_guess"] = final_guess
    label = mode(final_guess)
    for i in range(len(final_guess)):
        if final_guess[i] != label:
            # t2_df = t2_df.drop(index = i)
            lst.append(t2_df["WorkerId"][i])
    # t2_df.to_csv("sample_output_t2_filtered.csv",index=False)
    return lst


def main():
    FOLDER_PATH = "../data/metadata/"
    val_json = FOLDER_PATH + "meta.json"
    t1_path = "../data/t1_annotate/output/sample_output_t1.csv"
    t1_df = pd.read_csv(t1_path)
    t2_path = "../data/t2_guess/output/sample_output_t2.csv"
    t2_df = pd.read_csv(t2_path)
    with open(val_json) as f:
        data = json.load(f)
    task1_csv = task1_qca(data, t1_df)
    with open("task1-quality.csv", "w") as o:
        csv_out = csv.writer(o)
        csv_out.writerow(["worker_id", "quality"])
        csv_out.writerows(task1_csv)
    task2_csv = task2_qca(t2_df)
    with open("task2-quality.csv", "w") as o:
        csv_out = csv.writer(o)
        csv_out.writerow(["wrong answer"])
        csv_out.writerows([task2_csv])


if __name__ == "__main__":
    main()

import pandas as pd
import json

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

def get_bbox (select_anno, category_id):
    bounding_box = [
        anno["bbox"]   
        for anno in select_anno
        if anno["category_id"] == category_id        
    ]
    return bounding_box

with open(val_json) as f:
    data = json.load(f)

img_id = 22892
# 'cat' has a category id of 17

category_id = 17

select_img = get_image(data, 22892)

select_img

select_anno = [anno for anno in data["annotations"] if anno["image_id"] == 22892]

coordinates = get_coordinates(select_anno, category_id)
bbox = get_bbox(select_anno, category_id)

print(coordinates)

t1_path = "../data/t1_annotate/output/sample_output_t1.csv"
# raw sample for task 1
# rows 1-3 contain correct annotations
# row 4 is incorrect (dog)
# row 5 is incorrect (random)

t1_df = pd.read_csv(t1_path)

t1_df

t2_path = "../data/t2_guess/output/sample_output_t2.csv"

t2_df = pd.read_csv(t2_path)

t2_df

# Task 1 Quality Control and Aggregation

from numpy import mean
from numpy import percentile

average_coordinate = [0]*len(t1_df)
for i in range(len(t1_df)):
  average_coordinate[i] = mean([int(str(t1_df[f"point_{j}"][i]).replace(',','')) for j in range(1,11) if str(t1_df[f"point_{j}"][i]) != "nan"])

lower_cutoff = percentile(average_coordinate, 25)
upper_cutoff = percentile(average_coordinate, 75)

good_worker_indexes = []
for i in range(len(average_coordinate)):
  if (average_coordinate[i] <= upper_cutoff and average_coordinate[i] >= lower_cutoff):
    good_worker_indexes.append(i)

average_coordinate_good_workers = []
for i in range(len(t1_df)):
  if i not in good_worker_indexes:
     t1_df = t1_df.drop(index = i)
  else:
    average_coordinate_good_workers.append(average_coordinate[i])
 
t1_df["avg_point"] = average_coordinate_good_workers
best_coordinate = mean(average_coordinate_good_workers)    

t1_df.to_csv('sample_output_t1_filtered.csv',index=False)

# Task 2 Quality Control and Aggregation (Majority Vote)

from statistics import mode

final_guess = [""]*len(t2_df)
for i in range(len(t2_df)):
  final_guess[i] = [str(t2_df[f"guess_{j}"][i]) for j in range(1,6) if str(t2_df[f"guess_{j}"][i]) != "nan"][-1]

t2_df["final_guess"] = final_guess
label = mode(final_guess)

for i in range(len(final_guess)):
  if (final_guess[i] != label):
      t2_df = t2_df.drop(index = i)

t2_df.to_csv("sample_output_t2_filtered.csv",index=False)

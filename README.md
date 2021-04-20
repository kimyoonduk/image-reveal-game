# image-reveal-game
For our NETS 213 Final project, we will be creating a game in which users deblur images in the least amount of clicks for other users to identify the subject of the image. This game's purpose is to provide meaningful insight to image recognition.

[Link to Flow-Diagram](https://raw.githubusercontent.com/kimyoonduk/image-reveal-game/main/docs/d1/flow_diagram.png)

## Deliverable 1 - Major Components and Points Distribution

### Planning (1 point) 
In planning phase of our project, we expect to lay out the guidelines for Task 1 (annotation) and Task 2 (guessing), including the instructions that the user will see. We will also be selecting and inputting a relevant image dataset, setting goals for the size and attributes of our HIT's outputs, and establishing a budget and timeline for our milestones. 

### Task 1: Annotation (8 total points) 
Our first task for the crowdworkers is annotating images. To do this, a crowdworker will be given a clear version of an image, a blurred version of the same image, and a label associated with the image. For example, the label could be 'dog' and the image would be one containing a dog somewhere within it. The annotator's role is to click on pixelated squares of the blurred image to make that square clear, with the goal being to reveal the label in as few clicks as possible.

AMT HIT (4 points)
This will involve creating the interface that the users will interact with to deblur the images strategically.

Raw Data and Aggregation (2 points)
This will involve grabbing the data that we receive from the HIT and processing it in a way that is then usable for our second task.

Quality Control (2 points)
We will have to have a system of checking if the users are actually completing the task and not just selecting random squares quickly and submitting.

Mockup

![Mockup for Task 1](docs/d1/mockup_t1_annotation.png)

### Task 2: Guessing (5 total points)
For this task, users will be given the blurred image and will have to guess what the keyword for the image was. Incrementally, we will deblur the image according to a HIT in Task 1, so that the user in Task 2 will be "responding" to the the user in Task 1's strategic deblurring. They will have a chance to guess the keyword with each square that is deblurred.

AMT HIT (2 points)
This will also involve implementing an interface where the user just needs to guess the keyword, as the picture becomes gradually deblurred, square by square.

Raw Data and Aggregation (2 points)
This will involve again pulling the data from the HIT and making it usable for the final analysis.

Quality Control (1 point)
Here we can simply check if they are making reasonable guesses and not just trying to submit the task with no intelligible inputs.

Mockup

![Mockup for Task 2](docs/d1/mockup_t2_guessing.png)

### Analysis and Writeup (4 total points)

Data Description (2 points)
To characterize the data collected, we will create a heatmap for the click sequences that show which pixels are most commonly included for the given label to be guessed. We plan to also create visualizations for the selected coordinates and their corresponding answer rates. We also want to find characteristics of 'good' annotators and guessers, based on the time it took for themselves or their corresponding guesser to guess the label correctly.


Analysis of Results (2 points)
Analysis of our results will involve answering the big-picture questions and goals that we set for this project. We want to answer questions such as: is the most common sequence the best performing sequence? How do the guesses evolve over time? Do different incentives change the outcome, such as offering a bonus for fewer guesses? Analysis of the click sequences heatmap, coordinate and answer-rate data should give us insights to answer these questions and to better understand the process of image recognition.

## Deliverable 2: Data, Processing, and File Directory

### Data
Our game is split into two parts, one where users will annotate and deblur images and one where users will guess the labels for images. Towards that end, in our /data folder we have things separated by task, Task 1 for annotation and Task 2 for guessing.For Task 1: Annotation, our input data for one task is an image, a blurred version of that image, and a label describing the object of the image.  Task 1's input (/data/t1_annotate/input) will be the images and a .csv file that includes the image paths and the label that we will assign for each image. This is so that it can be easily uploaded to MTurk similar to the way we did in Homework 4:Become a requester. The output for Task 1 (/data/t1_annotate/output) will be the csv file that is outputted from MTurk, giving us the normal information about each HIT, but crucially the coordinates of their click, so that we know what to unblur. In the folder there is a sample csv currently there, and the relevant columns are the "point_X" columns for each time they click to deblur.

For Task 2: Guessing, the input (/data/t2_guess/input) is the output for Task 1, the MTurk csv results file. This is so that we can take the coordinates of their clicks and use them to create the second task. The output for Task 2 (data/t2_guess/output) is another MTurk csv results file, but this time the relevant data that we want to capture is the workers' guesses for the picture that will sequentially become deblurred. We have another sample csv that shows this data, where different users will have a different number of guesses on what the label of the photo is.

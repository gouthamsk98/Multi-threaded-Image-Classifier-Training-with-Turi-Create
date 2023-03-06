# Multi-threaded Image Classifier Training with Turi Create

This repository contains a Python script and a Dockerfile that demonstrate how to train multiple image classifiers concurrently using Turi Create and Docker.

## Dependencies

- Python 3.6.8
- Turi Create 6.3
- Docker

## Usage

1.  Clone this repository.

2.  Ensure that your images are in the JPEG format.

3.  Put your images in the following directory structure:

```
├── person1/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── ...
├── person2/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── ...
├── unknown/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── ...`
```

4.  Build the Docker image:

    sqlCopy code

    `docker build -t image-classifier .`

5.  Run the Docker image:

    rubyCopy code

    `docker run -it -v $(pwd)/<directory>:/app/uploads image-classifier`

    Replace `<directory>` with the name of the directory containing your images.

6.  The output of the program will be saved in the `uploads` directory. The model will be saved as `people.mlmodel` in the directory for each person.

## Note

- The script expects the images to be in the JPEG format.
- Ensure that your images are in the correct directory structure.
- The `unknown` directory is used to store random images that the classifier will attempt to classify.

## Files

- `train.py`: The Python script that trains the image classifiers.
- `Dockerfile`: The Dockerfile that creates the Docker image.
- `uploads`: The directory that contains the training images.

## Usage

### Step 1: Build the Docker image

From the command line, navigate to the directory that contains the `Dockerfile` and run the following command to build the Docker image:

bashCopy code

`docker build -t turi-image-classification .`

This command will create a Docker image named `turi-image-classification` that includes Python 3.6.8, Turi Create, and the `train.py` script.

### Step 2: Run the Docker container

Run the following command to start a Docker container from the `turi-image-classification` image:

bashCopy code

`docker  run -it --cpus=1 turi-image-classification"`

The script will load the images from the corresponding directory, split the data into training and testing sets, Train an image classification model using Turi Create, and export the model as a Core ML model file. The model file will be saved in each dataset's directory as `people.mlmodel`.

## Notes

- The `train.py` script uses the `TrainingThread` class to define a thread that loads and trains the data. If there are no other active threads besides the main thread, the script runs in single-threaded mode and trains the data on the main thread.
- The `train.py` script defines the `getImageFromPath` function, which extracts the name of the parent directory of an image file and uses it as the label for that image. This assumes that each subdirectory within `uploads/` corresponds to a different label, and that each image file within a subdirectory belongs to that label.
- The `Dockerfile` copies both the `train.py` script and the `uploads/` directory into the Docker container. This assumes that the image datasets are stored in the `uploads/` directory, which is created in the same directory as the `train.py` script. You can change this behavior by modifying the `COPY` command in the Dockerfile.

## Author

This project was created by <b>Goutham S Krishna</b>, a team lead at Bibox Labs and full stack developer.

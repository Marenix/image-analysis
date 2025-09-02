# Image Analysis CLI Tool

A robust, configurable command-line tool written in Python for performing batch analysis on image datasets. This tool recursively scans a directory for image files, extracts key metadata, and saves the results in a structured CSV file. The tool uses parallel processing to speed up analysis on multi-core systems.

## Key Features

* **Configurable:** All key parameters (input folder, output file, file extensions) are managed externally in a JSON file (example: configs/config.json).
* **Robust Error Handling:** The application is designed to be resilient. It gracefully handles common errors such as missing directories, invalid image files, and file permissions.
* **Memory Efficient:** Uses a streaming approach (Python generators) to process a large number of images with a very low and constant memory footprint.
* **Platform Independent:** Built with pathlib to ensure it runs correctly on Windows, macOS, and Linux.
* **Clean Architecture:** The code is logically separated into distinct, reusable, and testable modules (ConfigReader, FileExtractor, ImageAnalyzer, CSVWriter).
* **Parallel Processing:** Parallel processing implemented for image analysis to speed up the biggest bottleneck in the pipeline.

## Setup and Installation

1. **Clone the repository:**
```bash
   git clone git@github.com:Marenix/image-analysis.git
   cd image-analysis
```

2. Install dependencies:
   This project requires the Pillow library and OpenCV for image processing.
```bash
   pip install -r requirements.txt
```

   *(Note: All other required modules like pathlib and logging are part of the standard Python library.)*

## Configuration

Before running the application, create your JSON config file in configs/. You can use available config.json file as a template.

```json
{
    "FileExtractor": {
        "input_location": "data/",
        "extensions": [".jpg", ".jpeg", ".png"]
    },
    "CSVWriter": {
        "output_location": "output/image_metadata.csv"
    }
}
```

* **input_location**: The directory containing the images you want to analyze (NOTE: all subdirectories are searched as well).
* **extensions**: A list of file extensions to include in the scan.
* **output_location**: The path where the final CSV report will be saved. The directory will be created if it doesn't exist.

## How to Run

Execute the main.py script from the root directory of the project, providing the path to your configuration file.

Optional arguments:
* --input_location: Path to the input folder.
* --output_location: Path to the output folder (including the CSV file name).

```bash
python main.py --config_path configs/config.json
```

The script will then process the images and generate the CSV file in the location specified in your config.

## Current Extracted Data

The current version of this tool extracts the following basic metadata:

* filename: The name of the image file.
* filesize: The size of the file in bytes.
* width: The width of the image in pixels.
* height: The height of the image in pixels.
* aspect_ratio: The aspect ratio of the image.
* average_color: The average color of the whole image.
* num_of_faces: The number of faces detected in the image.

## Future Work

This project is built to be easily extended. The next planned steps include:

* Add a flag to save images with bounding-boxes around detected faces.
* Perform object detection in the image to detect some common/interesting objects.
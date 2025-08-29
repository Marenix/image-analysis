# Image Analysis CLI Tool

A robust, configurable command-line tool written in Python for performing batch analysis on image datasets. This tool recursively scans a directory for image files, extracts key metadata, and saves the results in a structured CSV file.

## Key Features

* **Configurable:** All key parameters (input folder, output file, file extensions) are managed externally in a JSON file (example configs/config.json).
* **Robust Error Handling:** The application is designed to be resilient. It gracefully handles common errors such as missing directories, invalid image files, and file permissions.
* **Memory Efficient:** Uses a streaming approach (Python generators) to process a large number of images with a very low and constant memory footprint.
* **Platform Independent:** Built with pathlib to ensure it runs correctly on Windows, macOS, and Linux.
* **Clean Architecture:** The code is logically separated into distinct, reusable, and testable modules (ConfigReader, FileExtractor, ImageAnalyzer, CSVWriter).

## Setup and Installation

1. **Clone the repository:**
```bash
   git clone git@github.com:Marenix/image-analysis.git
   cd image-analysis
```

2. Install dependencies:
   This project requires the Pillow library for image processing.
```bash
   pip install Pillow
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

```bash
python main.py --config_path configs/config.json
```

The script will then process the images and generate the CSV file in the location specified in your config.

## Current Extracted Data

The first version of this tool extracts the following basic metadata:

* filename: The name of the image file.
* filesize: The size of the file in bytes.
* width: The width of the image in pixels.
* height: The height of the image in pixels.

## Future Work

This project is built to be easily extended. The next planned steps include:

* Extracting calculated metadata like **aspect ratio** and **average color**.
* Performing content-based analysis, such as **face detection**.
* Implementing **parallel processing** to significantly speed up analysis on multi-core systems.
from image_analyzer.analyzer import analyze_single_image, initialize_worker, DATA_HEADERS
from image_analyzer.config_reader import ConfigReader
from image_analyzer.file_extractor import FileExtractor
from image_analyzer.csv_writer import CSVWriter
import argparse
from pathlib import Path
import logging
import concurrent.futures
import time

def main(args):
    start = time.time()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    config_reader = ConfigReader(args.config_path)
    file_extractor_config = config_reader.get_setting("FileExtractor", {})

    input_location = Path(file_extractor_config.get("input_location", Path("data/"))) if args.input_location is None else args.input_location
    extensions = file_extractor_config.get("extensions", [".png", ".jpg"])

    file_extractor = FileExtractor(input_location, extensions)

    image_analyzer_config = config_reader.get_setting("AnalyzerSettings", {})
    face_detection_model_path = Path(image_analyzer_config.get("face_detection_model_path", "models/haarcascade_frontalface_default.xml"))

    with concurrent.futures.ProcessPoolExecutor(
        initializer=initialize_worker,
        initargs=(face_detection_model_path,)
    ) as executor:
        raw_results_generator = executor.map(analyze_single_image, file_extractor.get_file_paths())

    valid_results = (result for result in raw_results_generator if result is not None)

    csv_writer_config = config_reader.get_setting("CSVWriter", {})
    output_location = Path(csv_writer_config.get("output_location", Path("output.csv"))) if args.output_location is None else args.output_location
    csv_writer = CSVWriter(output_location, DATA_HEADERS)
    csv_writer.write_data(valid_results)

    end = time.time()

    logging.info(f"Time needed for processing all images: {end - start}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ImageAnalyzer",
        description="Find and return all files in a specified folder and all subfolders"
    )
    parser.add_argument("--config_path", required=True, help="Path to config in JSON format")
    parser.add_argument("--input_location", required=False, help="Path to the input location")
    parser.add_argument("--output_location", required=False, help="Path to CSV output file (including output file name)")
    args = parser.parse_args()

    main(args)


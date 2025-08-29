from image_analyzer.analyzer import ImageAnalyzer
from image_analyzer.config_reader import ConfigReader
from image_analyzer.file_extractor import FileExtractor
from image_analyzer.csv_writer import CSVWriter
import argparse
from pathlib import Path
import logging

def main(args):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    config_reader = ConfigReader(args.config_path)
    file_extractor_config = config_reader.get_setting("FileExtractor", {})

    input_location = Path(file_extractor_config.get("input_location", Path("data/")))
    extensions = file_extractor_config.get("extensions", [".png", ".jpg"])

    file_extractor = FileExtractor(input_location, extensions)
    image_analyzer = ImageAnalyzer()

    results_generator = image_analyzer.analyze(file_extractor.get_file_paths())

    csv_writer_config = config_reader.get_setting("CSVWriter", {})
    output_location = Path(csv_writer_config.get("output_location", Path("output.csv")))
    csv_writer = CSVWriter(output_location, image_analyzer.DATA_HEADERS)
    csv_writer.write_data(results_generator)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ImageAnalyzer",
        description="Find and return all files in a specified folder and all subfolders"
    )
    parser.add_argument("--config_path", required=True, help="Path to config")
    args = parser.parse_args()

    main(args)


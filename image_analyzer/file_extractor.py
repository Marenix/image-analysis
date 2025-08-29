import argparse
from pathlib import Path
from typing import Union

class FileExtractor:
    """Finds and provides paths for all files in a specified folder.

    This class is responsible for searching the specified folder for all
    files with specified extensions.

    Attributes:
        input_location (Path): The path to the location of the image folder.
        extensions (list): The list containing all acceptable extensions.
    """

    def __init__(self, input_location: Union[Path, str], extensions: list[str]):
        """Initializes the FileExtractor and validates the input path.

        Args:
            input_location (Union[Path, str]): The directory path to search for files.
            extensions (list): List of acceptable extensions
        """
        self.input_location = Path(input_location)
        self.extensions = extensions

        if not self.input_location.is_dir():
            raise FileNotFoundError(f"Input directory not found at: {self.input_location}")

    def get_file_paths(self) -> list[Path]:
        """Retrieves all files in the folder, filtering by extension.

        Returns:
            list[Path]: A list of Path object for all found image files.
        """
        valid_extensions = {f".{ext.lower().strip('.')}" for ext in self.extensions}

        all_files_in_dir = self.input_location.rglob("*")

        accepted_images = [path for path in all_files_in_dir
                           if path.is_file() and path.suffix.lower() in valid_extensions]
        return accepted_images

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FileExtractor",
        description="Find and return all files in a specified folder and all subfolders"
    )
    parser.add_argument("--input_directory", required=True, help="Path to input directory")
    parser.add_argument("--extensions", nargs='+', required=True, help="One or more acceptable file extensions (e.g., .jpg .png)")
    args = parser.parse_args()

    try:
        file_extractor = FileExtractor(args.input_directory, args.extensions)
        all_files = file_extractor.get_file_paths()

        if not all_files:
            print("No image files found with the specified extensions.")
        else:
            print(f"Found {len(all_files)} image files:")
            for file_path in all_files:
                print(f"-{file_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")


    ##shutil.copy(all_files[0], "../data/something/yes.jpg")
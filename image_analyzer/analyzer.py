from PIL import Image, UnidentifiedImageError
from pathlib import Path
from typing import Iterator
import logging

class ImageAnalyzer:

    DATA_HEADERS = ['filename', 'filesize', 'width', 'height']

    def analyze(self, file_paths: list[Path]) -> Iterator[dict]:
        """Analyzes a collection of images and yields their metadata one by one.

        This method iterates through a list of file paths, extracts basic
        metadata (filename, size, dimensions) from each valid image file.
        It operates as a generator for memory efficiency.

        This method is resilient to errors. If an image file is corrupted,
        missing, or causes an unexpected error during processing, that file
        will be skipped, an appropriate warning or error will be logged, and
        the process will continue with the next file.

        Args:
            file_paths (list[Path]): A list of Path object pointing to the
                images that need to be analyzed

        Yields:
            dict: A dictionary containing the metadata for a single image.
            The keys for this dictionary correspond to the 'DATA_HEADERS'
            class attribute.
        """
        for path in file_paths:
            try:
                with Image.open(path) as img:
                    width, height = img.size
    
                image_data = {
                    'filename': path.name,
                    'filesize': path.stat().st_size,
                    'width': width,
                    'height': height
                }

                yield image_data

            except UnidentifiedImageError as e:
                logging.warning(f"Could not read image file {path}: {e}. Skipping.")
                continue

            except FileNotFoundError:
                logging.warning(f"File '{path.name}' not found. It may have been moved or deleted. Skipping.")
                continue

            except Exception as e:
                logging.error(f"An unexpected error occured with '{path.name}': {e}. Skipping.")
                continue
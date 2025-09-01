from PIL import Image, UnidentifiedImageError
from pathlib import Path
from typing import Iterator
import logging
from fractions import Fraction

class ImageAnalyzer:

    DATA_HEADERS = ['filename', 'filesize', 'width', 'height', 'aspect_ratio', 'average_color']

    def _get_average_color(self, image: Image) -> str:
        """Calculates the average color of the image and returns a hex string"""
        resized_image = image.resize((1, 1))
        rgb_pixel = resized_image.convert('RGB')
        r, g, b = rgb_pixel.getpixel((0, 0))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _calculate_aspect_ratio(self, width: int, height: int) -> str:
        """Calculates the image aspect ratio and returns it as a simplified string (e.g., '16:9').
        
        Handles the edge case of an image with a height of 0.
        """
        try:
            aspect_ratio = Fraction(width, height)
            return f"{aspect_ratio.numerator}:{aspect_ratio.denominator}"
        except ZeroDivisionError:
            logging.warning("Image has a height of 0, cannot calculate aspect ratio.")
            return "N/A"



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
                    average_color = self._get_average_color(img)
                
                image_data = {
                    'filename': path.name,
                    'filesize': path.stat().st_size,
                    'width': width,
                    'height': height,
                    'aspect_ratio': self._calculate_aspect_ratio(width, height),
                    'average_color': average_color
                }

                yield image_data

            except UnidentifiedImageError as e:
                logging.warning(f"Could not read image file {path}: {e}. Skipping.")
                continue

            except FileNotFoundError:
                logging.warning(f"File '{path.name}' not found. It may have been moved or deleted. Skipping.")
                continue

            except Exception as e:
                logging.error(f"An unexpected error occurred with '{path.name}': {e}. Skipping.")
                continue
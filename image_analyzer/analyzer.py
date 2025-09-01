from PIL import Image
from pathlib import Path
from typing import Union
import logging
from fractions import Fraction
import cv2
from typing import Optional

DATA_HEADERS = ['filename', 'filesize', 'width', 'height', 'aspect_ratio', 'average_color', 'num_of_faces']

face_detector = None

def get_average_color(image: Image) -> str:
    """Calculates the average color of the image and returns a hex string"""
    resized_image = image.resize((1, 1))
    rgb_pixel = resized_image.convert('RGB')
    r, g, b = rgb_pixel.getpixel((0, 0))
    return f"#{r:02x}{g:02x}{b:02x}"
    
def calculate_aspect_ratio(width: int, height: int) -> str:
    """Calculates the image aspect ratio and returns it as a simplified string (e.g., '16:9').
    
    Handles the edge case of an image with a height of 0.
    """
    try:
        aspect_ratio = Fraction(width, height)
        return f"{aspect_ratio.numerator}:{aspect_ratio.denominator}"
    except ZeroDivisionError:
        logging.warning("Image has a height of 0, cannot calculate aspect ratio.")
        return "N/A"
    
def get_number_of_faces_in_image(img_bgr: cv2.Mat) -> int:
    """Detects faces in an image, returns the number of faces found"""
    faces = face_detector.detect(img_bgr)

    if faces[1] is not None:
        return len(faces[1])
    return 0

def initialize_worker(model_path: Path):
    """An initializer function that is run once per worker process.
    Loads the face detection model into the global variable for that process.
    
    Args:
        model_path (Path): Path to the model to be used
    """
    global face_detector
    logging.info(f"Initialiting worker with model: {model_path}")
    face_detector = cv2.FaceDetectorYN.create(str(model_path),
                                                "",
                                                (320, 320))

def analyze_single_image(path: Path) -> Optional[dict]:
    """Performs all analysis for a single image file
    
    The function receives a path to a single image, extracts all specified
    metadata and information and returns is as a dictionary.
    
    Args:
        path (Path): Path to the image file.

    Returns:
        A dictionary of image metadata or None if analysis fails.
    """
    try:
        img_bgr = cv2.imread(str(path))
        if img_bgr is None:
            logging.warning(f"{path} could not be read by OpenCV. It may be corrupt. Skipping.")
            return None
        
        height, width, _ = img_bgr.shape
        face_detector.setInputSize((width, height))

        number_of_faces = get_number_of_faces_in_image(img_bgr)
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)
        average_color = get_average_color(pil_image)
                
        image_data = {
            'filename': path.name,
            'filesize': path.stat().st_size,
            'width': width,
            'height': height,
            'aspect_ratio': calculate_aspect_ratio(width, height),
            'average_color': average_color,
            'num_of_faces': number_of_faces
        }

        return image_data

    except FileNotFoundError:
        logging.warning(f"File '{path}' not found. It may have been moved or deleted. Skipping.")
        return None

    except Exception as e:
        logging.error(f"An unexpected error occurred with '{path}': {e}. Skipping.")
        return None
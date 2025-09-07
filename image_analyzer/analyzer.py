from PIL import Image
from pathlib import Path
from typing import Union
import logging
from fractions import Fraction
import cv2
from typing import Optional

DATA_HEADERS = ['filename', 'filesize', 'width', 'height', 'aspect_ratio', 'average_color', 'num_of_faces']

face_detector = None
visualize = False
save_location = Path("/output/visualize")

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
    
def visualize_images_with_faces(img_bgr: cv2.Mat, faces: cv2.Mat, image_name: str):
    """Draw rectangle around each found face and save the image to output location.

    Args:
        img_bgr (cv2.Mat): Image on which the faces were detected.
        faces (cv2.Mat): Information on detected face positions.
        image_name (str): Filename of the original image.
    """
    for row in faces[1]:
        cv2.rectangle(img_bgr, (round(row[0]), round(row[1])), (round(row[0])+round(row[2]), round(row[1])+round(row[3])), (0,255,0), 4)
    cv2.imwrite(str(save_location / image_name), img_bgr)
    
def get_number_of_faces_in_image(img_bgr: cv2.Mat, image_name:str) -> int:
    """Detects faces in an image, returns the number of faces found."""
    faces = face_detector.detect(img_bgr)

    if faces[1] is not None:
        if visualize:
            visualize_images_with_faces(img_bgr, faces, image_name)
        return len(faces[1])
    return 0

def _prepare_directory(output_file: Path):
        """Ensures the parent directory for the output file exists."""
        try:
            output_file.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logging.error(f"Error: Permission denied to create directory {output_file}")
            raise

def initialize_worker(model_path: Path, save_example: bool, output_location: Path):
    """An initializer function that is run once per worker process.
    Loads the face detection model into the global variable for that process.
    Sets flag for saving images with bounding boxed around detected faces.
    Saves the output location used for saving images using output_location/visualize
    folder.
    
    Args:
        model_path (Path): Path to the model to be used.
        save_example (bool): True if images want to be saved.
        output_location (Path): Path to the folder used for saving.
    """
    global face_detector
    logging.info(f"Initialiting worker with model: {model_path}")
    face_detector = cv2.FaceDetectorYN.create(str(model_path),
                                                "",
                                                (320, 320))
    
    global visualize, save_location
    visualize = save_example
    save_location = output_location / "visualize"
    _prepare_directory(save_location)

def analyze_single_image(path: Path) -> Optional[dict]:
    """Performs all analysis for a single image file.
    
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

        number_of_faces = get_number_of_faces_in_image(img_bgr, path.name)
        
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
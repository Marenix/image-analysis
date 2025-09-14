from pathlib import Path
from image_analyzer.file_extractor import FileExtractor

def test_get_file_paths(tmp_path: Path):
    image_folder = tmp_path / "images"
    image_folder.mkdir()
    subdir1 = image_folder / "good_images"
    subdir1.mkdir()
    (image_folder / "pic1.jpg").touch()
    (image_folder / "pic2.png").touch()
    (image_folder / "pic3.jpeg").touch()
    (image_folder / "not_a_pic.txt").touch()
    (subdir1 / "pic4.png").touch()
    (subdir1 / "not_a_pic2.txt").touch()
    expected_filenames = {"pic1.jpg", "pic2.png", "pic3.jpeg", "pic4.png"}

    file_extractor = FileExtractor(image_folder, ["jpg", "png", "jpeg"])
    actual_filenames = {path.name for path in file_extractor.get_file_paths()}

    assert expected_filenames == actual_filenames
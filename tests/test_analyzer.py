from image_analyzer.analyzer import calculate_aspect_ratio, get_average_color
from PIL import Image
import pytest

@pytest.mark.parametrize("test_size, expected_ratio", [
    ((1920, 1080), "16:9"),
    ((0, 100), "0:1"),
    ((290, 0), "N/A")
])
def test_aspect_ratio_calculation(test_size: tuple[int, int], expected_ratio: str):
    actual_ratio = calculate_aspect_ratio(test_size[0], test_size[1])

    assert expected_ratio == actual_ratio

@pytest.mark.parametrize("test_color_tuple, expected_hex_code", [
    ((255, 255, 255), "#ffffff"),
    ((0, 0, 0), "#000000"),
    ((255, 0, 0), "#ff0000"),
    ((0, 255, 0), "#00ff00"),
    ((0, 0, 255), "#0000ff"),
    ((128, 128, 128), "#808080"),
    ((15, 195, 63), "#0fc33f")
])
def test_get_average_color(test_color_tuple: tuple[int, int, int], expected_hex_code: str):
    image = Image.new(mode="RGB", size=(10, 10), color=test_color_tuple)

    actual_output = get_average_color(image)

    assert expected_hex_code == actual_output
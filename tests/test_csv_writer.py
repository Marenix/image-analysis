from pathlib import Path
from image_analyzer.csv_writer import CSVWriter
import csv

def test_write_data(tmp_path: Path):
    output_file = tmp_path / "results.csv"
    headers = ["col1", "col2", "col3", "col4"]
    expected_output = [{"col1": "row11", "col2": "row12", "col3": "row13", "col4": "row14"},
                       {"col1": "row21", "col2": "row22", "col3": "row23", "col4": "row24"}]


    csv_writer = CSVWriter(output_file, headers)
    csv_writer.write_data(expected_output)
    with open(output_file, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        actual_output = list(reader)

    assert expected_output == actual_output
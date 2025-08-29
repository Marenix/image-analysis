import csv
from pathlib import Path
from typing import Iterable, Union
import logging

class CSVWriter():
    """A class for writing data to a CSV file.

    This writer handles directory creation, file permissions and data validation
    to ensure a resilient writing process. It is designed to work with an iterable
    of dictionaries, making it suitable for streaming data.

    Attributes:
        output_file (Path): The Path object for the destination file.
        headers (list[str]): A list of strings for the CSV header row.
    """

    def __init__(self, output_file: Union[Path, str], headers: list[str]):
        """Initializes the CSVWriter and prepares the output directory.

        Args:
            output_file (Union[Path, str]): The destination file path, can be a string or Path object.
            headers (list[str]): An ordered list of strings to use as the CSV header.
        """
        self.output_file = Path(output_file)
        self.headers = headers

        self._prepare_directory()

    def _prepare_directory(self):
        """Ensures the parent directory for the output file exists."""
        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logging.error(f"Error: Permission denied to create directory {self.output_file.parent}")
            raise

    def write_data(self, data: Iterable[dict]):
        """Writes all rows from an iterable of dictionaries to the CSV file.

        This method will first write the header row, then iterate through the
        provided data, writing one dictionary per row. It will skip and print a
        warning for any rows that have keys not present in the headers.

        Args:
            data (Iterable[dict]): An iterable (like a list or generator) that
                yields dictionaries to be written as rows.
        
        Raises:
            IOError: If a major I/O error occurs (e.g., disk full, permissions).
        """
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.headers)
                writer.writeheader()

                for row_dict in data:
                    try:
                        writer.writerow(row_dict)
                    except ValueError:
                        logging.warning(f"Warning: Skipping row with mismatched data: {row_dict}")
                        continue
        except PermissionError:
            logging.error(f"Error: Permission denied to create file {self.output_file}")
            raise
        except IOError as e:
            logging.error(f"Fatal I/O Error writing to {self.output_file}: {e}")
            raise
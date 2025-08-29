import json
import logging

class ConfigReader:
    """Reads and provides access to the project's JSON config.

    This class is responsible for loading the main config.json file,
    handling potential file errors, and providing a simple interface
    for other parts of the application to retrieve settings.

    Attributes:
        config_path (str): The path to the configuration file.
        config (dict): The loaded configuration dictionary.
    """

    def __init__(self, config_path: str):
        """Initializes the ConfigReader and loads the configuration.

        Args:
            config_path (str): The path to the JSON configuration file.

        Raises:
            ValueError: If the config file cannot be loaded or parsed.
        """
        self.config_path = config_path
        self.config = self._load_config()

        if self.config is None:
            raise ValueError("Config could not be loaded. Exiting.")

    def _load_config(self):
        """Loads and parses the JSON configuration file.

        This method handles FileNotFoundError and json.JSONDecodeError internally.
        
        Returns:
            dict: The loaded config file if successful.
            None: If the file is not found or cannot be parsed.
        """
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                return config
        except FileNotFoundError:
            logging.error(f"Error: Config file not found at '{self.config_path}'")
            return None
        except json.JSONDecodeError:
            logging.error(f"Error: The file at '{self.config_path}' is not a valid JSON file")
            return None
        
    def get_setting(self, key: str, default=None):
        """Retrieves a setting from the loaded config.

        Args:
            key (str): The top-level configuration key to retrieve.
            default: The value to return if the key is not found.
                     Defaults to None.

        Returns:
            The value associated with the key or the default value.
        """
        if self.config:
            return self.config.get(key, default)
        return default
import yaml
import os
import importlib

class ConfigLoader:
    def __init__(self, config_path=None):
        """
        Initializes the ConfigLoader with a path to the YAML config file.
        """
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = os.path.join(os.path.dirname(__file__), 'scraper_config.yaml')
        self.config = None

    def load_yml(self):
        """
        Loads the configuration from the YAML file.
        """
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        return self.config

    def get_available_scrapers(self):
        """
        Returns the available scrapers from the configuration.
        """
        if self.config is None:
            self.load_yml()
        return self.config.get('available_scrapers', [])

    def import_class_path(self, class_path):
        """
        Dynamically imports a class from a string.
        """
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

# Usage example:
# loader = ConfigLoader()
# config = loader.load_config()
# available_scrapers = loader.get_available_scrapers()
# scraper_class = loader.import_class_from_string('module.class_name')

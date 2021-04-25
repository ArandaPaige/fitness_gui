from pathlib import Path

BASE_DIR = Path().resolve()
INI_FILE = 'settings.ini'
INI_PATH = BASE_DIR / INI_FILE


class Settings:

    def __init__(self):
        self.settings = None
        self.check_settings()
        self.units = self.set_units()

    def __repr__(self):
        return f'{self.settings}'

    def check_settings(self):
        """Checks for settings file and updates instance attribute

        Checks to see if a settings.ini file already exists and reads it. If the file does not exist, it is created
        with the default settings of the application.
        :return: None
        """
        if INI_PATH.exists():
            self.settings = self.read_settings_file()
            return
        else:
            self.create_settings_file()
            self.settings = self.create_settings_dictionary()
            self.write_settings_file()

    def create_settings_file(self):
        """Creates the settings.ini file. Raises exception if it exists and returns None."""
        try:
            fcreate = open(INI_FILE, 'x', encoding='utf-8')
        except FileExistsError:
            return
        else:
            fcreate.close()

    def write_settings_file(self):
        """Writes the settings dictionary to the settings.ini.

        The contents of the settings dictionary are written to the settings.ini file line by line. An exception is
        raised if the file does not exist. It will then create a new settings.ini file with a default implementation of
        the application settings.
        :return: None
        """
        try:
            fwrite = open(INI_FILE, 'w', encoding='utf-8')
        except FileNotFoundError:
            self.check_settings()
        else:
            with fwrite:
                for k, v in self.settings.items():
                    fwrite.write(f'{k}:{v} \n')

    def read_settings_file(self):
        """Reads the contents of the settings.ini file.

        The contents of the settings.ini are read and constructed as a dictionary. An exception is raised if the file
        does not exist. It will then create a new settings.ini file with a default implementation of the application
        settings.
        :return: dictionary
        """
        try:
            fread = open(INI_FILE, 'r')
        except FileNotFoundError:
            self.check_settings()
        else:
            with fread:
                settings = {k: v for k, v in [line.rstrip().split(':', 1) for line in fread]}
                return settings

    def create_settings_dictionary(self):
        """Creates a dictionary with key-value pairs that correspond to the default program values and returns None"""
        settings = {
            'Measurement System': 'Imperial',
            'Theme': 'Light',
            'Default Graph Entry Range': 'All',
            'Default Graph Future Range': 'None'
        }
        return settings

    def set_measurement_system(self, system='Imperial'):
        """Sets the dictionary value to the measurement system provided and returns None."""
        self.settings['Measurement System'] = system

    def set_theme(self, theme='Light'):
        """Sets the dictionary value to the theme provided and returns None."""
        self.settings['Theme'] = theme

    def set_graph_entry_default(self, default='All'):
        """Sets the dictionary value to the range provided and returns None."""
        self.settings['Default Graph Entry Range'] = default

    def set_graph_future_default(self, default='None'):
        """Sets the dictionary value to the range provided and returns None."""
        self.settings['Default Graph Future Range'] = default

    def set_units(self):
        if self.settings['Measurement System'] == 'Imperial':
            return 'lbs'
        if self.settings['Measurement System'] == 'Metric':
            return 'kg'
        if self.settings['Measurement System'] == 'British Imperial':
            return 'stones'

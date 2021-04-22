from pathlib import Path

BASE_DIR = Path().resolve()
INI_FILE = 'settings.ini'
INI_PATH = BASE_DIR / INI_FILE


class Settings:

    def __init__(self):
        self.check_settings()
        self.measurement_system = None
        self.date_system = None
        self.theme = None
        self.graph_entry_default = None
        self.graph_future_default = None
        self.settings = self.create_settings_dictionary()

    def check_settings(self):
        if INI_PATH.exists():
            settings = self.read_settings_file()
            self.settings = settings
            return
        else:
            self.create_settings_file()

    def create_settings_file(self):
        with open(INI_FILE, 'x', encoding='utf-8') as fout:
            pass

    def write_settings_file(self):
        try:
            fwrite = open(INI_FILE, 'w', encoding='utf-8')
        except FileNotFoundError:
            self.create_settings_file()
        else:
            with fwrite:
                for k, v in self.settings.items():
                    fwrite.write(f'{k}:{v} \n')

    def read_settings_file(self):
        try:
            fread = open(INI_FILE, 'r')
        except FileNotFoundError:
            self.create_settings_file()
            self.write_settings_file()
        else:
            with fread:
                settings = {}
                for line in fread:
                    k, v = line.rstrip().split(':', 1)
                    settings[k] = v
                return settings

    def set_measurement_system(self, system='Imperial'):
        self.measurement_system = system

    def set_date_system(self, system='ISO'):
        self.date_system = system

    def set_theme(self, theme='Light'):
        self.theme = theme

    def set_graph_entry_default(self, default='All'):
        self.graph_entry_default = default

    def set_graph_future_default(self, default='None'):
        self.graph_lerp_default = default

    def create_settings_dictionary(self):
        settings = {
            'Measurement System': self.measurement_system,
            'Date System': self.date_system,
            'Theme': self.theme,
            'Default Graph Entry Range': self.graph_entry_default,
            'Default Graph Future Range': self.graph_future_default
        }
        return settings

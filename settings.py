from pathlib import Path

BASE_DIR = Path().resolve()
INI_FILE = 'settings.ini'
INI_PATH = BASE_DIR / INI_FILE


class Settings:

    def __init__(self):
        self.settings = None
        self.check_settings()

    def __repr__(self):
        return f'{self.settings}'

    def check_settings(self):
        if INI_PATH.exists():
            self.settings = self.read_settings_file()
            return
        else:
            self.create_settings_file()
            self.settings = self.create_settings_dictionary()
            self.write_settings_file()

    def create_settings_file(self):
        try:
            fcreate = open(INI_FILE, 'x', encoding='utf-8')
        except FileExistsError:
            return
        else:
            fcreate.close()

    def write_settings_file(self):
        try:
            fwrite = open(INI_FILE, 'w', encoding='utf-8')
        except FileNotFoundError:
            self.check_settings()
        else:
            with fwrite:
                for k, v in self.settings.items():
                    fwrite.write(f'{k}:{v} \n')

    def read_settings_file(self):
        try:
            fread = open(INI_FILE, 'r')
        except FileNotFoundError:
            self.check_settings()
        else:
            with fread:
                settings = {k: v for k, v in [line.rstrip().split(':', 1) for line in fread]}
                return settings

    def create_settings_dictionary(self):
        settings = {
            'Measurement System': 'Imperial',
            'Date System': 'ISO',
            'Theme': 'Light',
            'Default Graph Entry Range': 'All',
            'Default Graph Future Range': 'None'
        }
        return settings

    def set_measurement_system(self, system='Imperial'):
        self.settings['Measurement System'] = system

    def set_date_system(self, system='ISO'):
        self.settings['Date System'] = system

    def set_theme(self, theme='Light'):
        self.settings['Theme'] = theme

    def set_graph_entry_default(self, default='All'):
        self.settings['Default Graph Entry Range'] = default

    def set_graph_future_default(self, default='None'):
        self.settings['Default Graph Future Range'] = default

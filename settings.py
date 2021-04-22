INI_FILE = 'settings.ini'


class Settings:

    def __init__(self):
        self.measurement_system = None
        self.date_system = None
        self.theme = None
        self.graph_entry_default = None
        self.graph_lerp_default = None

    def create_settings_file(self):
        with open(INI_FILE, 'x', encoding='utf-8') as fout:
            pass

    def write_settings_file(self):
        with open(INI_FILE, 'w', encoding='utf-8') as fwrite:
            pass

    def read_settings_file(self):
        with open(INI_FILE, 'r') as fread:
            pass

    def set_measurement_system(self, system):
        pass

    def set_date_system(self, system):
        pass

    def set_theme(self, theme):
        pass

    def set_graph_entry_default(self, default):
        pass

    def set_graph_lerp_default(self, default):
        pass

    def create_settings_dictionary(self):
        settings = {
            'Measurement System': self.measurement_system,
            'Date System': self.date_system,
            'Theme': self.theme,
            'Default Graph Entry Range': self.graph_entry_default,
            'Default Graph Lerp Range': self.graph_lerp_default
        }
        return settings

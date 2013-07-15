import json
import os.path


class BaseConfigParser:
    CONFIG_DIR = '.gmrh'

    def parse_file(self):
        pass

    def find_config_file(self, path=None):
        real_path = os.path.realpath(path)
        config_path = os.path.join(path, self.CONFIG_FILE)
        config_dir = os.path.join(path, self.CONFIG_DIR)
        if os.path.isfile(config_path):
            self.config_path = config_path
            self.working_path = real_path
            if os.path.isdir(config_dir):
                self.config_dir = config_dir
            else:
                self.config_dir = None

        if real_path != '/':
            new_path = os.path.join(real_path, os.path.pardir)
            self.find_config_file(new_path)


class JsonConfigParser(BaseConfigParser):
    CONFIG_FILE = '.gmrh.json'

    def parse_file(self):
        with open(self.config_path) as config_file:
            json_data = json.loads(config_file.read())

        self.repositories = json_data['repos']
        self.remotes = json_data['remotes']

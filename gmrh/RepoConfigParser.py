import json
import os.path


class BaseConfigParser:
    def parse_file(self):
        pass

    def find_config_file(self, path=None):
        real_path = os.path.realpath(path)
        config_path = os.path.join(path, self.CONFIG_FILE)
        if os.path.isfile(config_path):
            return config_path, real_path
        elif real_path != '/':
            new_path = os.path.join(real_path, os.path.pardir)
            return self.find_config_file(new_path)
        else:
            return None, None


class JsonConfigParser(BaseConfigParser):
    CONFIG_FILE = '.gmrh.json'

    def parse_file(self, config_file_path):
        with open(config_file_path) as config_file:
            json_data = json.loads(config_file.read())

        self.repositories = json_data['repos']
        self.remotes = json_data['remotes']

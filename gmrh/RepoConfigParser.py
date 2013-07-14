import json


class BaseConfigParser:
    def parse_file(self):
        pass


class JsonConfigParser(BaseConfigParser):
    CONFIG_FILE = '.gmrh.json'

    def parse_file(self):
        with open(self.CONFIG_FILE) as config_file:
            json_data = json.loads(config_file.read())

        self.repositories = json_data['repos']
        self.remotes = json_data['remotes']

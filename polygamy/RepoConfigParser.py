from __future__ import absolute_import

import json
import os.path


class BaseConfigParser:
    CONFIG_DIR = '.polygamy'

    def parse_file(self):
        pass

    def find_config_file(self, path):
        real_path = os.path.realpath(path)

        config_file = os.path.join(path, self.CONFIG_FILE)
        config_dir = os.path.join(path, self.CONFIG_DIR)
        config_dir_file = os.path.join(config_dir, self.CONFIG_FILE)

        # Search for a config file within a .polygamy directory
        if os.path.isdir(config_dir):
            for f in (self.CONFIG_FILE, self.DIR_CONFIG_FILE):
                config_dir_file = os.path.join(config_dir, f)
                if os.path.isfile(config_dir_file):
                    self.config_path = config_dir_file
                    self.working_directory = real_path
                    return config_dir_file

        # Look or a .polygamy.json file.
        if os.path.isfile(config_file):
            self.config_path = config_file
            self.working_directory = real_path
            return config_file

        # Stop recursively searching when we hit the root directory.
        if real_path == os.path.realpath(os.path.join(path, os.path.pardir)):
            # TODO: Better error handling for not finding a config file. Some
            # kind of wizard for generating a config would be very cool indeed.
            raise ValueError('Cannot find config file or directory')

        return self.find_config_file(
            os.path.join(path, os.path.pardir)
        )


class JsonConfigParser(BaseConfigParser):
    CONFIG_FILE = '.polygamy.json'
    DIR_CONFIG_FILE = 'polygamy.json'

    def parse_file(self):
        with open(self.config_path) as config_file:
            json_data = json.loads(config_file.read())

        self.repositories = json_data['repos']
        self.remotes = json_data['remotes']

from __future__ import absolute_import

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser
import json
import os.path

from blessings import Terminal
term = Terminal()


class BaseConfigParser:
    CONFIG_DIR = '.polygamy'

    def parse_file(self):
        pass

    def find_config_file(self, path):
        real_path = os.path.realpath(path)

        config_dir = os.path.join(path, self.CONFIG_DIR)
        config_dir_file = os.path.join(
            config_dir, 'polygamy', self.CONFIG_FILE
        )

        # Search for a config file within a .polygamy directory
        if os.path.isdir(config_dir):
            if not os.path.isdir(os.path.join(config_dir, 'polygamy')):
                print(term.red(
                    "Found polygamy directory %s, but not a config"
                    " repository." % config_dir
                ))
                raise Exception()

            if not os.path.isfile(config_dir_file):
                print(term.red(
                    "Found polygamy directory %s, but not a config file." %
                    config_dir
                ))
                raise Exception()

            self.config_path = config_dir_file
            self.working_directory = real_path
            self.config_dir = config_dir
            return config_dir_file

        # Stop recursively searching when we hit the root directory.
        if real_path == os.path.realpath(os.path.join(path, os.path.pardir)):
            # TODO: Better error handling for not finding a config file. Some
            # kind of wizard for generating a config would be very cool indeed.
            raise ValueError('Cannot find config file or directory')

        return self.find_config_file(
            os.path.join(path, os.path.pardir)
        )


class JsonConfigParser(BaseConfigParser):
    CONFIG_FILE = 'polygamy.json'

    def parse_file(self):
        with open(self.config_path) as config_file:
            json_data = json.loads(config_file.read())

        self.repositories = json_data['repos']
        self.remotes = json_data['remotes']

        self.preference_config = ConfigParser()
        self.preference_config.add_section('groups')
        self.preference_config.add_section('git')
        self.preference_config.read(
            os.path.join(self.config_dir, 'preferences.ini')
        )
        self.enabled_groups = {
            k for k, v in self.preference_config.items('groups')
        }
        self.git_config = self.preference_config.items('git')

    def save_preferences(self):
        self.preference_config.remove_section('groups')
        self.preference_config.add_section('groups')
        for group in self.enabled_groups:
            self.preference_config.set('groups', group, '')

        with open(os.path.join(self.config_dir, 'preferences.ini'), 'w') as f:
            self.preference_config.write(f)

    def save_config_file(self):
        with open(self.config_path, 'w') as config_file:
            config_file.write(json.dumps(
                {
                    'remotes': self.remotes,
                    'repos': self.repositories,
                },
                indent=4,
                separators=(',', ': '),
            ))

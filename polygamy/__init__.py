import os

import RepoConfigParser
import RepositoryHandler


def main():
    parser = RepoConfigParser.JsonConfigParser()
    parser.find_config_file(path=os.getcwd())
    parser.parse_file()
    repository_handler = RepositoryHandler.GitRepositoryHandler(
        config=parser
    )

    repository_handler.update_repositories()

import os

import RepoConfigParser
import RepositoryHandler


def main():
    parser = RepoConfigParser.JsonConfigParser()
    parser.find_config_file(path=os.getcwd())
    parser.parse_file()
    repository_handler = RepositoryHandler.DefaultRepositoryHandler(
        cwd=parser.working_path
    )

    for path, repo_details in parser.repositories.iteritems():
        remote = parser.remotes[repo_details['remote']]
        remote_url = remote['url'] + repo_details['name']
        remote_branch = remote['branch']

        repository_handler.update_or_clone(path, remote_url, remote_branch)

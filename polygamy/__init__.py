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

    default_remote_name = None
    for name, settings in parser.remotes.iteritems():
        if settings.get('default', False):
            default_remote_name = name
            break
    else:
        if len(parser.remotes) == 1:
            default_remote_name = parser.remotes.keys()[0]

    for path, repo_details in parser.repositories.iteritems():
        remote_name = repo_details.get('remote', default_remote_name)
        remote = parser.remotes[remote_name]
        remote_url = remote['url'] + repo_details['name']
        remote_branch = remote['branch']

        repository_handler.update_or_clone(path, remote_url, remote_branch)
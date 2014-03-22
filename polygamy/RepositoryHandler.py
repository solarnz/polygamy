from __future__ import absolute_import

import os
import os.path

from blessings import Terminal
term = Terminal()

from . import git


class GitRepository(object):
    def __init__(self, name, path, remote_name, remote_url, remote_branch):
        self.name = name
        self.path = path
        self.remote_name = remote_name
        self.remote_url = remote_url
        self.remote_branch = remote_branch

    def repository_exists(self):
        return os.path.exists(
            os.path.join(self.path, '.git')
        )

    def update_repository(self):
        print ('Fetching repository %s ...' % self.name)

        url = git.get_remote_url(self.path, self.remote_name)
        if url != self.remote_url:
            git.set_remote_url(self.path, self.remote_name, self.remote_url)

        git.fetch_remote(self.path, self.remote_name)

        local_change_count = git.count_different_commits(
            self.path,
            '%s/%s' % (self.remote_name, self.remote_branch),
            'HEAD'
        )
        remote_change_count = git.count_different_commits(
            self.path,
            'HEAD',
            '%s/%s' % (self.remote_name, self.remote_branch)
        )

        if remote_change_count or local_change_count:
            print (
                'Branch has %s more commits and %s less commits '
                'than %s/%s' % (
                    local_change_count, remote_change_count, self.remote_name,
                    self.remote_branch
                )
            )

        if remote_change_count and not local_change_count:
            print (term.green("Fast forwarding repository..."))
            git.fast_forward(self.path, self.remote_name, self.remote_branch)

    def clone_repository(self):
        print (term.green('Cloning repository %s ...' % self.name))
        git.clone(self.path, self.remote_url, self.remote_branch)

    def update_or_clone(self):
        if self.repository_exists():
            self.update_repository()
        else:
            self.clone_repository()


class GitRepositoryHandler(object):
    def __init__(self, config):
        self.config = config
        remotes = config.remotes

        self.repositories = []

        # Determine the default remote
        default_remote_name = None
        for name, settings in remotes.items():
            if settings.get('default', False):
                default_remote_name = name
                break
        else:
            if len(remotes) == 1:
                default_remote_name = list(remotes.keys())[0]

        # Load the repositories
        for path, repo_details in config.repositories.items():
            remote_name = repo_details.get('remote', default_remote_name)
            if not remote_name:
                raise ValueError(
                    'Repo %s has no remote set, and there is no'
                    'valid default remote!' % path
                )

            remote = config.remotes[remote_name]
            remote_url = remote['url'] + repo_details['name']
            remote_branch = remote['branch']

            repo = GitRepository(
                name=path,
                path=os.path.realpath(
                    os.path.join(config.working_directory, path)
                ),
                # TODO: Proper updating of the remotes if the remote is not
                # already set.
                #remote_name=remote_name,
                remote_name='origin',
                remote_url=remote_url,
                remote_branch=remote_branch,
            )
            self.repositories.append(repo)

    def update_repositories(self):
        for repo in self.repositories:
            repo.update_or_clone()

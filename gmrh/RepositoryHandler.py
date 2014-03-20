import os
import os.path
import subprocess

from blessings import Terminal
term = Terminal()

import git


class DefaultRepositoryHandler():
    def __init__(self, cwd=None):
        self.cwd = cwd or os.getcwd()

    def repository_exists(self, path):
        return os.path.exists(os.path.join(self.cwd, path, '.git'))

    def update_repository(self, path, remote_url, remote_branch):
        print 'Fetching repository %s ...' % path

        remote_name = 'origin'
        repository_path = os.path.join(self.cwd, path)

        url = git.get_remote_url(repository_path, remote_name)
        if url != remote_url:
            git.set_remote_url(repository_path, remote_name, remote_url)

        git.fetch_remote(repository_path, remote_name)

        output = subprocess.check_output(
            ['git', 'cherry', '%s/%s' % (remote_name, remote_branch), 'HEAD'],
            cwd=repository_path
        ).strip()
        local_change_count = len(filter(None, output.split('\n')))

        output = subprocess.check_output(
            ['git', 'cherry', 'HEAD', '%s/%s' % (remote_name, remote_branch)],
            cwd=repository_path
        ).strip()
        remote_change_count = len(filter(None, output.split('\n')))

        if remote_change_count or local_change_count:
            print (
                'Branch has %s more commits and %s less commits '
                'than %s/%s' % (
                    local_change_count, remote_change_count, remote_name,
                    remote_branch
                )
            )

        if remote_change_count and not local_change_count:
            print term.green("Fast forwarding repository...")
            subprocess.check_call(
                [
                    'git', 'merge', '%s/%s' % (remote_name, remote_branch),
                    '--ff-only'
                ],
                cwd=repository_path
            )

    def clone_repository(self, path, remote_url, remote_branch):
        print term.green('Cloning repository %s ...' % path)
        git.clone(self.cwd, path, remote_url, remote_branch)

    def update_or_clone(self, path, remote_url, remote_branch):
        if self.repository_exists(path):
            self.update_repository(path, remote_url, remote_branch)
        else:
            self.clone_repository(path, remote_url, remote_branch)

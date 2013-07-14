import os.path
import subprocess


class DefaultRepositoryHandler():
    def __init__(self, cwd):
        self.cwd = cwd

    def repository_exists(self, path):
        return os.path.exists(path + os.path.sep + '.git')

    def update_repository(self, path, remote_url, remote_branch):
        print 'Updating repository %s ...' % path
        subprocess.check_call(['git', 'pull', '--rebase'])

    def clone_repository(self, path, remote_url, remote_branch):
        print 'Cloning repository %s ...' % path
        subprocess.check_call(['git', 'clone', remote_url, '-b',  remote_branch, path])

    def update_or_clone(self, path, remote_url, remote_branch):
        if self.repository_exists(path):
            self.update_repository(path, remote_url, remote_branch)
        else:
            self.clone_repository(path, remote_url, remote_branch)


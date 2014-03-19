import os
import os.path
import subprocess


class DefaultRepositoryHandler():
    def __init__(self, cwd=None):
        self.cwd = cwd or os.getcwd()

    def repository_exists(self, path):
        return os.path.exists(os.path.join(self.cwd, path, '.git'))

    def update_repository(self, path, remote_url, remote_branch):
        print 'Fetching repository %s ...' % path

        remote_name = 'origin'
        repository_path = os.path.join(self.cwd, path)

        url = subprocess.check_output(
            ['git', 'config', 'remote.%s.url' % remote_name],
            cwd=repository_path
        )

        if url != remote_url:
            subprocess.check_call(
                ['git', 'config', 'remote.%s.url' % remote_name, remote_url],
                cwd=repository_path
            )

        subprocess.check_call(
            ['git', 'fetch', remote_name],
            cwd=repository_path
        )

        output = subprocess.check_output(
            ['git', 'cherry', '%s/%s' % (remote_name, remote_branch), 'HEAD']
        ).strip()
        remote_change_count = len(output.split('\n')) - 1

        output = subprocess.check_output(
            ['git', 'cherry', 'HEAD', '%s/%s' % (remote_name, remote_branch)]
        ).strip()
        local_change_count = len(output.split('\n')) - 1

        if remote_change_count or local_change_count:
            print (
                'Branch has %s more commits and %s less commits '
                'than %s/%s' % (
                    local_change_count, remote_change_count, remote_name,
                    remote_branch
                )
            )

    def clone_repository(self, path, remote_url, remote_branch):
        print 'Cloning repository %s ...' % path
        subprocess.check_call(
            ['git', 'clone', remote_url, '-b',  remote_branch, path],
            cwd=self.cwd
        )

    def update_or_clone(self, path, remote_url, remote_branch):
        if self.repository_exists(path):
            self.update_repository(path, remote_url, remote_branch)
        else:
            self.clone_repository(path, remote_url, remote_branch)

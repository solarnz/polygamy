import subprocess


def clone(cwd, path, remote_url, remote_branch):
        subprocess.check_call(
            ['git', 'clone', remote_url, '-b',  remote_branch, path],
            cwd=cwd
        )

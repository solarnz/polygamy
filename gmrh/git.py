import subprocess


def clone(cwd, path, remote_url, remote_branch):
        subprocess.check_call(
            ['git', 'clone', remote_url, '-b',  remote_branch, path],
            cwd=cwd
        )


def get_remote_url(path, remote_name):
    url = subprocess.check_output(
        ['git', 'config', 'remote.%s.url' % remote_name],
        cwd=path
    )
    return url


def set_remote_url(path, remote_name, remote_url):
    subprocess.check_call(
        ['git', 'config', 'remote.%s.url' % remote_name, remote_url],
        cwd=path
    )


def fetch_remote(path, remote_name):
    subprocess.check_call(
        ['git', 'fetch', remote_name],
        cwd=path
    )

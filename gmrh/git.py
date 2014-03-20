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


def calculate_different_commits(path, to_reference, from_reference):
    """ Return the commits in the `from_reference` that are not in
    `to_reference`
    """
    output = subprocess.check_output(
        ['git', 'cherry', to_reference, from_reference],
        cwd=path
    ).strip()

    lines = output.split('\n')
    # Return those lines that are 'truthy'
    return filter(None, lines)


def count_different_commits(path, to_reference, from_reference):
    """ Count the commits in the `from_reference` that are not in
    `to_reference`
    """
    return len(calculate_different_commits(path, to_reference, from_reference))

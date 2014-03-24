from __future__ import absolute_import

import subprocess


def clone(path, remote_url, remote_branch):
        subprocess.check_call(
            ['git', 'clone', remote_url, '-b',  remote_branch, path],
        )


def get_remote_url(path, remote_name):
    url = subprocess.check_output(
        ['git', 'config', 'remote.%s.url' % remote_name],
        cwd=path
    )
    return url.strip()


def get_current_branch(path):
    try:
        branch = subprocess.check_output(
            ['git', 'symbolic-ref', '--short', 'HEAD'],
            cwd=path
        )
        return branch.strip()
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            pass
        else:
            raise
    commit_hash = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD'],
        cwd=path
    )
    return commit_hash.strip()


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


def fast_forward(path, remote_name, remote_branch):
    subprocess.check_call(
        [
            'git', 'merge', '%s/%s' % (remote_name, remote_branch),
            '--ff-only'
        ],
        cwd=path
    )

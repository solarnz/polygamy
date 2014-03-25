from __future__ import absolute_import

import os
import subprocess


class NoSuchRemote(Exception):
    pass


def clone(path, remote_url, remote_branch):
    try:
        subprocess.check_call(
            ['git', 'clone', remote_url, '-b',  remote_branch, path],
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            return False
        else:
            raise
    return True


def get_remote_url(path, remote_name):
    remotes = subprocess.check_output(
        ['git', 'remote'],
        cwd=path
    ).strip().split('\n')

    if remote_name not in remotes:
        raise NoSuchRemote()

    url = subprocess.check_output(
        ['git', 'config', 'remote.%s.url' % remote_name],
        cwd=path
    )
    return url.strip()


def add_remote(path, remote_name, remote_url):
    subprocess.check_output(
        ['git', 'remote', 'add', remote_name, remote_url],
        cwd=path
    )


def get_current_branch(path):
    try:
        branch = subprocess.check_output(
            ['git', 'symbolic-ref', '--short', 'HEAD'],
            stderr=open(os.devnull, 'w'),
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


def is_on_branch(path):
    return get_proper_current_branch(path) is not None


def get_proper_current_branch(path):
    try:
        return subprocess.check_output(
            ['git', 'symbolic-ref', '--short', 'HEAD'],
            stderr=open(os.devnull, 'w'),
            cwd=path
        ).strip()
    except subprocess.CalledProcessError:
        pass
    return None


def set_remote_url(path, remote_name, remote_url):
    subprocess.check_call(
        ['git', 'config', 'remote.%s.url' % remote_name, remote_url],
        cwd=path
    )


def fetch_remote(path, remote_name):
    try:
        subprocess.check_call(
            ['git', 'fetch', remote_name],
            cwd=path
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            return False
        else:
            raise
    return True


def calculate_different_commits(path, to_reference, from_reference):
    """ Return the commits in the `from_reference` that are not in
    `to_reference`
    """
    try:
        output = subprocess.check_output(
            ['git', 'cherry', to_reference, from_reference],
            stderr=open(os.devnull, 'w'),
            cwd=path
        ).strip()
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            return None
        else:
            raise

    lines = output.split('\n')
    # Return those lines that are 'truthy'
    return filter(None, lines)


def count_different_commits(path, to_reference, from_reference):
    """ Count the commits in the `from_reference` that are not in
    `to_reference`
    """
    diff = calculate_different_commits(path, to_reference, from_reference)
    if diff is None:
        return float('nan')
    return len(diff)


def fast_forward(path, remote_name, remote_branch):
    subprocess.check_call(
        [
            'git', 'merge', '%s/%s' % (remote_name, remote_branch),
            '--ff-only'
        ],
        cwd=path
    )

def push(path, remote_name, local_branch, remote_branch):
    subprocess.check_call(
        ['git', 'push', remote_name, '%s:%s' % (local_branch, remote_branch)],
        cwd=path
    )

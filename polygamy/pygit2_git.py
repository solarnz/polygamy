from __future__ import absolute_import

import pygit2

from .base_git import NoSuchRemote
from .plain_git import PlainGit


class Pygit2Git(PlainGit):
    @staticmethod
    def is_on_branch(path):
        repo = pygit2.Repository(path)

        return not (repo.head_is_detached or repo.head_is_unborn)

    @staticmethod
    def get_remote_url(path, remote_name):
        repo = pygit2.Repository(path)

        for remote in repo.remotes:
            if remote.name == remote_name:
                break
        else:
            raise NoSuchRemote()

        return remote.url

    @staticmethod
    def add_remote(path, remote_name, remote_url):
        repo = pygit2.Repository(path)
        repo.create_remote(remote_name, remote_url)

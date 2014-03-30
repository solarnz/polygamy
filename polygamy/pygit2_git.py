from __future__ import absolute_import

import pygit2

from .base_git import NoSuchRemote
from .plain_git import PlainGit


class Pygit2Git(PlainGit):
    @staticmethod
    def _find_remote(repo, remote_name):
        for remote in repo.remotes:
            if remote.name == remote_name:
                return remote
        else:
            raise NoSuchRemote()

    @staticmethod
    def is_on_branch(path):
        repo = pygit2.Repository(path)

        return not (repo.head_is_detached or repo.head_is_unborn)

    @staticmethod
    def get_remote_url(path, remote_name):
        repo = pygit2.Repository(path)
        remote = Pygit2Git._find_remote(repo, remote_name)

        return remote.url

    @staticmethod
    def add_remote(path, remote_name, remote_url):
        repo = pygit2.Repository(path)
        repo.create_remote(remote_name, remote_url)

    @staticmethod
    def set_remote_url(path, remote_name, remote_url):
        repo = pygit2.Repository(path)
        remote = Pygit2Git._find_remote(repo, remote_name)
        remote.url = remote_url
        remote.save()

    @staticmethod
    def get_current_branch(path):
        repo = pygit2.Repository(path)
        if repo.head_is_unborn:
            return PlainGit.get_current_branch(path)

        if repo.head_is_detached:
            return str(repo.head.target)

        return repo.head.shorthand

    @staticmethod
    def get_proper_current_branch(path):
        repo = pygit2.Repository(path)
        if repo.head_is_detached or repo.head_is_unborn:
            return None
        return repo.head.shorthand

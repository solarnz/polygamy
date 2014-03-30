from __future__ import absolute_import

import pygit2

from .plain_git import PlainGit


class Pygit2Git(PlainGit):
    @staticmethod
    def is_on_branch(path):
        repo = pygit2.Repository(path)

        return not (repo.head_is_detached or repo.head_is_unborn)

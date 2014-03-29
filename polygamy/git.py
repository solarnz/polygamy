from __future__ import absolute_import

try:
    from . import pygit2_git
    git = pygit2_git.Pygit2Git()
except ImportError:
    from . import plain_git
    git = plain_git.PlainGit()

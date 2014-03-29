from __future__ import absolute_import


class NoSuchRemote(Exception):
    pass


class BaseGit(object):
    @staticmethod
    def clone(path, remote_url, remote_branch):
        raise NotImplementedError()

    @staticmethod
    def get_remote_url(path, remote_name):
        raise NotImplementedError()

    @staticmethod
    def add_remote(path, remote_name, remote_url):
        raise NotImplementedError()

    @staticmethod
    def get_current_branch(path):
        raise NotImplementedError()

    @staticmethod
    def is_on_branch(path):
        raise NotImplementedError()

    @staticmethod
    def get_proper_current_branch(path):
        raise NotImplementedError()

    @staticmethod
    def set_remote_url(path, remote_name, remote_url):
        raise NotImplementedError()

    @staticmethod
    def fetch_remote(path, remote_name):
        raise NotImplementedError()

    @staticmethod
    def calculate_different_commits(path, to_reference, from_reference):
        raise NotImplementedError()

    @staticmethod
    def count_different_commits(path, to_reference, from_reference):
        raise NotImplementedError()

    @staticmethod
    def fast_forward(path, remote_name, remote_branch):
        raise NotImplementedError()

    @staticmethod
    def push(path, remote_name, local_branch, remote_branch):
        raise NotImplementedError()

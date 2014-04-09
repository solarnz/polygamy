from __future__ import absolute_import

import os
import subprocess

from .base_git import (BaseGit, NoSuchRemote)


class PlainGit(BaseGit):
    @staticmethod
    def clone(path, remote_url, remote_branch, remote_name='origin'):
        try:
            subprocess.check_call(
                [
                    'git', 'clone', remote_url, '-b',  remote_branch, '-o',
                    remote_name, path
                ],
            )
        except subprocess.CalledProcessError as e:
            if e.returncode == 128:
                return False
            else:
                raise
        return True

    @staticmethod
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

    @staticmethod
    def add_remote(path, remote_name, remote_url):
        subprocess.check_output(
            ['git', 'remote', 'add', remote_name, remote_url],
            cwd=path
        )

    @staticmethod
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

    @staticmethod
    def is_on_branch(path):
        return PlainGit.get_proper_current_branch(path) is not None

    @staticmethod
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

    @staticmethod
    def set_remote_url(path, remote_name, remote_url):
        subprocess.check_call(
            ['git', 'config', 'remote.%s.url' % remote_name, remote_url],
            cwd=path
        )

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def count_different_commits(path, to_reference, from_reference):
        """ Count the commits in the `from_reference` that are not in
        `to_reference`
        """
        diff = PlainGit.calculate_different_commits(
            path, to_reference, from_reference
        )
        if diff is None:
            return float('nan')
        return len(diff)

    @staticmethod
    def fast_forward(path, remote_name, remote_branch):
        subprocess.check_call(
            [
                'git', 'merge', '%s/%s' % (remote_name, remote_branch),
                '--ff-only'
            ],
            cwd=path
        )

    @staticmethod
    def push(path, remote_name, local_branch, remote_branch):
        subprocess.check_call(
            [
                'git', 'push', remote_name,
                '%s:%s' % (local_branch, remote_branch)
            ],
            cwd=path
        )

    @staticmethod
    def start_new_branch(path, branch_name, remote_name, remote_branch):
        subprocess.check_call(
            [
                'git', 'checkout', '-b', branch_name,
                '%s/%s' % (remote_name, remote_branch)
            ],
            cwd=path
        )

    @staticmethod
    def checkout_branch(path, branch_name):
        subprocess.check_call(
            ['git', 'checkout', branch_name],
            cwd=path
        )

    @staticmethod
    def list_branches(path):
        output = subprocess.check_output(
            ['git', 'branch'],
            cwd=path
        )

        branches = []

        for branch in output.split('\n'):
            branch = branch.strip()
            if not branch:
                continue
            if branch.startswith('* '):
                current_branch = branch[2:]
            else:
                branches.add(branch)

        return current_branch, branches

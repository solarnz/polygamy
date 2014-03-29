from __future__ import absolute_import

import math
import os
import os.path

from blessings import Terminal
term = Terminal()
import tabulate

from .git import git
from .base_git import NoSuchRemote


class GitRepository(object):
    def __init__(self, name, path, remote_name, remote_url, remote_branch):
        self.name = name
        self.path = path
        self.remote_name = remote_name
        self.remote_url = remote_url
        self.remote_branch = remote_branch

    def repository_exists(self):
        return os.path.exists(
            os.path.join(self.path, '.git')
        )

    def update_remote(self, dry_run):
        try:
            url = git.get_remote_url(self.path, self.remote_name)
        except NoSuchRemote:
            if dry_run:
                print(term.red(
                    'Would add remote %s for %s.' % (
                        self.remote_name, self.path
                    )
                ))
                return False
            git.add_remote(self.path, self.remote_name, self.remote_url)
            url = self.remote_url

        if url.strip() != self.remote_url.strip():
            if dry_run:
                print(term.red(
                    'Remote url for %s is incorrect, will update it.' %
                    self.name
                ))
                return False
            git.set_remote_url(self.path, self.remote_name, self.remote_url)
        return True

    def update_repository(self, dry_run):
        print('Fetching repository %s ...' % self.name)

        if not self.update_remote(dry_run):
            return

        if not self.fetch():
            return

        local_change_count = self.local_change_count()
        remote_change_count = self.remote_change_count()

        if remote_change_count or local_change_count:
            print(
                'Branch has %s more commits and %s less commits '
                'than %s/%s' % (
                    local_change_count, remote_change_count, self.remote_name,
                    self.remote_branch
                )
            )

        if (remote_change_count and not local_change_count and
                git.is_on_branch(self.path)):
            if dry_run:
                print(term.red('Would attempt to fastforward %s.' % self.name))
                return

            print(term.green("Fast forwarding repository..."))
            git.fast_forward(self.path, self.remote_name, self.remote_branch)
        elif remote_change_count:
            print(term.red(
                'Not fastforwarding %s. Branch has %s local changes.' %
                (self.name, local_change_count)
            ))

    def clone_repository(self):
        print(term.green('Cloning repository %s ...' % self.name))
        git.clone(self.path, self.remote_url, self.remote_branch)

    def fetch(self):
        if self.repository_exists():
            if not git.fetch_remote(self.path, self.remote_name):
                print(term.red("Unable to fetch %s in %s." % (self.remote_name,
                                                              self.path)))
                return False
            return True
        return False

    def local_change_count(self):
        local_change_count = git.count_different_commits(
            self.path,
            '%s/%s' % (self.remote_name, self.remote_branch),
            'HEAD'
        )
        return local_change_count

    def remote_change_count(self):
        remote_change_count = git.count_different_commits(
            self.path,
            'HEAD',
            '%s/%s' % (self.remote_name, self.remote_branch)
        )
        return remote_change_count

    def update_or_clone(self, dry_run):
        if self.repository_exists():
            self.update_repository(dry_run)
        else:
            if dry_run:
                print(term.red(
                    "Repo %s doesn't exist, will create it." % self.name
                ))
                return
            if not self.clone_repository():
                print(term.red(
                    "Unable to clone %s with remote %s." % (
                        self.path, self.remote_name
                    )
                ))

    def status(self):
        local_change_count = self.local_change_count()
        remote_change_count = self.remote_change_count()
        branch = git.get_current_branch(self.path)
        return {
            'branch': branch,
            'local_change_count': local_change_count,
            'remote_change_count': remote_change_count,
        }

    def push(self):
        current_branch = git.get_proper_current_branch(self.path)
        git.push(self.path, self.remote_name, current_branch, current_branch)


class GitRepositoryHandler(object):
    def __init__(self, config, dry_run):
        self.config = config
        self.dry_run = dry_run

        remotes = config.remotes

        self.repositories = {}

        # Determine the default remote
        default_remote_name = None
        for name, settings in remotes.items():
            if settings.get('default', False):
                default_remote_name = name
                break
        else:
            if len(remotes) == 1:
                default_remote_name = list(remotes.keys())[0]

        # Load the repositories
        for path, repo_details in config.repositories.items():
            remote_name = repo_details.get('remote', default_remote_name)
            if not remote_name:
                raise ValueError(
                    'Repo %s has no remote set, and there is no'
                    'valid default remote!' % path
                )

            remote = config.remotes[remote_name]
            remote_url = remote['url'] + repo_details['name']
            remote_branch = remote['branch']

            repo = GitRepository(
                name=path,
                path=os.path.realpath(
                    os.path.join(config.working_directory, path)
                ),
                remote_name=remote_name,
                remote_url=remote_url,
                remote_branch=remote_branch,
            )
            self.repositories[path] = repo

    def update_repositories(self):
        for repo in self.repositories.values():
            repo.update_or_clone(self.dry_run)

    def fetch(self):
        for repo in self.repositories.values():
            repo.fetch()

    def list(self, seperator, local_changes_only):
        repo_names = []
        for repo in self.repositories.values():
            change_count = repo.local_change_count()
            if not local_changes_only or (change_count and
                                          not math.isnan(change_count)):
                repo_names.append(repo.name)

        print(seperator.join(repo_names))

    def status(self):
        statuses = []
        for repo in sorted(self.repositories.values(), key=lambda r: r.name):
            status = repo.status()
            statuses.append([
                repo.name,
                status['branch'],
                status['local_change_count'],
                status['remote_change_count']
            ])

        print(tabulate.tabulate(
            statuses,
            headers=['Repo', 'Branch', 'Local Changes', 'Remote Changes'],
            tablefmt='simple'
        ))

    def push(self, repositories):
        for repository in repositories:
            self.repositories[repository].push()

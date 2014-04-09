from __future__ import absolute_import

from collections import defaultdict
import math
import os
import os.path

from blessings import Terminal
term = Terminal()
import tabulate

from . import RepoConfigParser
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

        on_branch = git.is_on_branch(self.path)

        if remote_change_count and not local_change_count and on_branch:
            if dry_run:
                print(term.red('Would attempt to fastforward %s.' % self.name))
                return

            print(term.green("Fast forwarding repository..."))
            git.fast_forward(self.path, self.remote_name, self.remote_branch)
        elif remote_change_count and not on_branch:
            print(term.red(
                "Unable to fastforward. Checkout a branch first."
            ))
        elif remote_change_count:
            print(term.red(
                'Not fastforwarding %s. Branch has %s local changes.' %
                (self.name, local_change_count)
            ))

    def clone_repository(self):
        print(term.green('Cloning repository %s ...' % self.name))
        return git.clone(self.path, self.remote_url, self.remote_branch,
                         remote_name=self.remote_name)

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

    def start(self, branch):
        current_branch, branches = git.list_branches(self.path)
        if branch not in branches:
            print branch
            git.start_new_branch(
                self.path, branch, self.remote_name, self.remote_branch
            )
        else:
            print(term.red(
                "Branch %s already exists in %s." % (branch, self.name)
            ))


class GitRepositoryHandler(object):
    def __init__(self, dry_run):
        self.dry_run = dry_run

        self.config = RepoConfigParser.JsonConfigParser()
        self.config.find_config_file(os.getcwd())

        self.configure()

    def configure(self):
        config = self.config
        config.parse_file()
        remotes = config.remotes

        self.repositories = {}
        self.repo_groups = defaultdict(list)

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
            repo_group = repo_details.get('group')

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
            self.repo_groups[repo_group].append(repo)

        self.enabled_groups = {None} | config.enabled_groups

    def _repository_iter(self):
        for group in self.enabled_groups:
            for repo in self.repo_groups[group]:
                yield repo

    def update_repositories(self):
        for repo in self._repository_iter():
            repo.update_or_clone(self.dry_run)

    def fetch(self):
        for repo in self._repository_iter():
            repo.fetch()

    def list(self, seperator, local_changes_only):
        repo_names = []
        for repo in self._repository_iter():
            change_count = repo.local_change_count()
            if not local_changes_only or (change_count and
                                          not math.isnan(change_count)):
                repo_names.append(repo.name)

        print(seperator.join(repo_names))

    def status(self):
        statuses = []
        for repo in sorted(self._repository_iter(), key=lambda r: r.name):
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

    def groups(self):
        for group in sorted(self.repo_groups.keys()):
            if group is None:
                continue

            enabled = u'\u2714' if group in self.enabled_groups else ' '
            print '[%s] %s' % (enabled, group)

    def enable_groups(self, groups):
        self.config.enabled_groups |= set(groups)
        self.config.save_preferences()

    def disable_groups(self, groups):
        self.config.enabled_groups -= set(groups)
        self.config.save_preferences()

    def start(self, branch_name, repositories):
        for repo in repositories:
            self.repositories[repo].start(branch_name)

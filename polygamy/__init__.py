from __future__ import absolute_import

import argparse
import os

from blessings import Terminal
term = Terminal()

from . import RepositoryHandler
from .git import git

__author__ = 'Chris Trotman'
__email__ = 'chris@trotman.io'
__version__ = '0.1.2'


class ArgumentHandler(object):
    def __init__(self):
        self.config_parser = argparse.ArgumentParser(
            description='Handle multiple scm repos.'
        )

        sub_parsers = self.config_parser.add_subparsers(title="action")
        self.build_init_argument(sub_parsers)
        self.build_pull_argument(sub_parsers)
        self.build_status_argument(sub_parsers)
        self.build_fetch_argument(sub_parsers)
        self.build_list_argument(sub_parsers)
        self.build_push_argument(sub_parsers)
        self.build_group_arguments(sub_parsers)
        self.build_start_argument(sub_parsers)
        self.build_add_argument(sub_parsers)

    def parse_args(self):
        self.args = self.config_parser.parse_args()
        return self.args

    def run_action(self, repository_handler):
        function_name = 'run_action_%s' % self.args.action
        if not hasattr(self, function_name):
            raise ValueError(
                'Action %s has no run function' % self.args.action
            )

        getattr(self, function_name)(repository_handler)

    def build_init_argument(self, sub_parsers):
        # Init action
        init_parser = sub_parsers.add_parser(
            "init",
            help="Initialise a polygamy workspace"
        )
        init_parser.add_argument(
            'url',
            help='The url of the polygamy config repository you want to clone'
        )
        init_parser.add_argument('branch', nargs='?', default='master')
        init_parser.set_defaults(action='init')

    def run_action_init(self, repository_handler):
        self.run_action_pull(repository_handler)

    def build_pull_argument(self, sub_parsers):
        # Pull action
        pull_parser = sub_parsers.add_parser(
            'pull',
            help="Update your local repositories"
        )
        pull_parser.add_argument(
            '-n', '--dry-run', action='store_true',
            help=("Run in dry run mode. Remoted will be fetched, but"
                  " configuration will not be updated, and branches will not"
                  " be fast forwarded.")
        )
        pull_parser.set_defaults(action='pull')

    def run_action_pull(self, repository_handler):
        repository_handler.fetch_polygamy_repo()
        repository_handler.update_repositories()

    def build_status_argument(self, sub_parsers):
        # Status action
        status_parser = sub_parsers.add_parser(
            'status',
            help=("Shows the current status of your repositories. Included the"
                  " branch you're on, the number of commits you're head of the"
                  " default remote branch, and how many commits you are"
                  " behind.")
        )
        status_parser.set_defaults(action='status')

    def run_action_status(self, repository_handler):
        repository_handler.status()

    def build_fetch_argument(self, sub_parsers):
        # Fetch action
        fetch_parser = sub_parsers.add_parser(
            'fetch',
            help=("Fetches changes from the remote repository. This will not"
                  " clone new repositories, or fast-forward exsiting"
                  " repositories.")
        )
        fetch_parser.set_defaults(action='fetch')

    def run_action_fetch(self, repository_handler):
        repository_handler.fetch_polygamy_repo()
        repository_handler.fetch()

    def build_list_argument(self, sub_parsers):
        # List action
        list_action = sub_parsers.add_parser(
            'list',
            help="Lists the repositories under control by polygamy."
        )
        list_action.add_argument(
            '-s', '--seperator',
            default='\n',
            help=("String to seperate the repositories with. Defaults to a new"
                  " line.")
        )
        list_action.add_argument(
            '-l', '--local-only',
            action='store_true',
            help=("Only list repositories that have local changes.")
        )
        list_action.set_defaults(action='list')

    def run_action_list(self, repository_handler):
        repository_handler.list(self.args.seperator, self.args.local_only)

    def build_push_argument(self, sub_parsers):
        # Push action
        push_action = sub_parsers.add_parser(
            'push',
            help=("Pushes the current branch to the remote. Note: this does a"
                  " simple push. I.e the local branch name will be the branch"
                  " that will be pushed to on the remote.")
        )
        push_action.add_argument(
            'repositories',
            type=str,
            nargs='+',
            help="The repositories to push."
        )
        push_action.set_defaults(action='push')

    def run_action_push(self, repository_handler):
        repository_handler.push(self.args.repositories)

    def build_group_arguments(self, sub_parsers):
        # Groups action
        groups = sub_parsers.add_parser(
            'groups',
            help=("Shows the enabled and disabled groups.")
        )
        groups.set_defaults(action='groups')

        groups_enable = sub_parsers.add_parser(
            'enable',
            help=("Enable groups")
        )
        groups_enable.add_argument(
            'groups',
            type=str,
            nargs='+',
            help="The groups to enable."
        )
        groups_enable.set_defaults(action='enable_groups')

        groups_disable = sub_parsers.add_parser(
            'disable',
            help=("Disable groups.")
        )
        groups_disable.add_argument(
            'groups',
            type=str,
            nargs='+',
            help="The groups to disable."
        )
        groups_disable.set_defaults(action='disable_groups')

    def run_action_groups(self, repository_handler):
        repository_handler.groups()

    def run_action_enable_groups(self, repository_handler):
        repository_handler.enable_groups(self.args.groups)

    def run_action_disable_groups(self, repository_handler):
        repository_handler.disable_groups(self.args.groups)

    def build_start_argument(self, sub_parsers):
        # Push action
        start_action = sub_parsers.add_parser(
            'start',
            help=("Starts a new branch on the specified repositories.")
        )
        start_action.add_argument(
            'branch_name',
            type=str,
            help="The branch name you want to create"
        )
        start_action.add_argument(
            'repositories',
            type=str,
            nargs='+',
            help="The repositories to start the new branch on."
        )
        start_action.set_defaults(action='start')

    def run_action_start(self, repository_handler):
        repository_handler.start(
            self.args.branch_name,
            self.args.repositories
        )

    def build_add_argument(self, sub_parsers):
        # Push action
        add_action = sub_parsers.add_parser(
            'add',
            help=("Adds the repository to the working directory.")
        )
        add_action.add_argument(
            'repository_url',
            type=str,
            help="The url of the repository you want to add.",
        )
        add_action.add_argument(
            'directory',
            type=str,
            help="The path to clone the repository into.",
        )
        add_action.add_argument(
            '--group',
            type=str,
            help="The group to add this repository to.",
        )
        add_action.add_argument(
            '--branch',
            type=str,
            help="The branch to checkout in the repository."
        )
        add_action.set_defaults(action='add')

    def run_action_add(self, repository_handler):
        repository_handler.add_repository(
            self.args.repository_url,
            self.args.directory,
            self.args.group,
            self.args.branch,
        )


def main():
    argument_handler = ArgumentHandler()
    args = argument_handler.parse_args()

    if args.action == 'init':
        os.mkdir('.polygamy')
        git.clone('.polygamy/polygamy', args.url, args.branch)

    repository_handler = RepositoryHandler.GitRepositoryHandler(
        dry_run=getattr(args, 'dry_run', False)
    )

    argument_handler.run_action(repository_handler)

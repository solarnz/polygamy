from __future__ import absolute_import

import argparse
import os

from blessings import Terminal
term = Terminal()

from . import git
from . import RepoConfigParser
from . import RepositoryHandler


def main():
    config_parser = argparse.ArgumentParser(
        description='Handle multiple scm repos.'
    )

    sub_parsers = config_parser.add_subparsers(title="action")

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

    # Pull action
    pull_parser = sub_parsers.add_parser(
        'pull',
        help="Update your local repositories"
    )
    pull_parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help=("Run in dry run mode. Remoted will be fetched, but"
              " configuration will not be updated, and branches will not be"
              " fast forwarded.")
    )
    pull_parser.set_defaults(action='pull')

    args = config_parser.parse_args()

    if args.action == 'init':
        git.clone('.polygamy', args.url, args.branch)

    parser = RepoConfigParser.JsonConfigParser()
    parser.find_config_file(path=os.getcwd())
    parser.parse_file()
    repository_handler = RepositoryHandler.GitRepositoryHandler(
        config=parser,
        dry_run=getattr(args, 'dry_run', False)
    )

    if args.action in ('pull', 'init'):
        repository_handler.update_repositories()

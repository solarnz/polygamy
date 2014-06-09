import unittest

from polygamy.plain_git import PlainGit


class TestUrlParsing(unittest.TestCase):
    def test_http_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'http://github.com/solarnz/polygamy.git'
            ),
            'polygamy'
        )

    def test_ssh_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'ssh://github.com/solarnz/polygamy.git'
            ),
            'polygamy'
        )

    def test_ssh_url_with_username(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'ssh://solarnz@github.com/solarnz/polygamy.git'
            ),
            'polygamy'
        )

    def test_git_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'git://github.com/solarnz/polygamy.git'
            ),
            'polygamy'
        )

    def test_minimal_ssh_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'git@github.com/solarnz/polygamy.git'
            ),
            'polygamy'
        )


class TestUrlParsingWithoutGitSuffix(unittest.TestCase):
    def test_http_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'http://github.com/solarnz/polygamy'
            ),
            'polygamy'
        )

    def test_ssh_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'ssh://github.com/solarnz/polygamy'
            ),
            'polygamy'
        )

    def test_ssh_url_with_username(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'ssh://solarnz@github.com/solarnz/polygamy'
            ),
            'polygamy'
        )

    def test_git_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'git://github.com/solarnz/polygamy'
            ),
            'polygamy'
        )

    def test_minimal_ssh_url(self):
        self.assertEqual(
            PlainGit.repo_name_from_url(
                'git@github.com/solarnz/polygamy'
            ),
            'polygamy'
        )

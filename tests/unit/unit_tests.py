import unittest
import mock
from biautomation.utils import set_repo


def get_env(key, default):
    return "super-secret-token"


class AutomationSetRepoTest(unittest.TestCase):
    def test_set_repo_without_env_variable(self):
        output = set_repo("hellofresh/great-repo", "1.2.3")
        self.assertEqual("git+ssh://git@github.com/hellofresh/great-repo.git@master#egg=1.2.3", output)

        output = set_repo("hellofresh/great-repo", "1.2.3", "no-master-branch")
        self.assertEqual("git+ssh://git@github.com/hellofresh/great-repo.git@no-master-branch#egg=1.2.3", output)

    @mock.patch('os.getenv', side_effect=get_env)
    def test_set_repo_with_env_variable(self, os):

        output = set_repo("hellofresh/thanks-obama", "3.4.2")
        self.assertEqual("https://super-secret-token@github.com/hellofresh/thanks-obama/tarball/master#egg=3.4.2", output)

        output = set_repo("hellofresh/thanks-obama", "3.4.2", "no-master-branch")
        self.assertEqual("https://super-secret-token@github.com/hellofresh/thanks-obama/tarball/no-master-branch#egg=3.4.2", output)

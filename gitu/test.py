import unittest

from gitu import __main__
from gitu.config import Config


def run_cmd(cmd: str):
    __main__.main(cmd.split())


class GituTestCase(unittest.TestCase):
    def expect_user(self, name_or_alias: str, user_dict: dict):
        config = Config()
        user = config.get_user(name_or_alias)
        self.assertIsNotNone(user)
        for k, v in user_dict.items():
            self.assertEqual(v, user.to_dict().get(k))


class TestRegister(GituTestCase):
    def test_register(self):
        run_cmd('add Misaka misaka@example.com -a Mikoto -g true -k xxx')
        self.expect_user('Mikoto', {
            'name': 'Misaka',
            'email': 'misaka@example.com',
            'gpgsign': True,
            'gpgkey': 'xxx'
        })


class TestEdit(GituTestCase):
    def test_edit(self):
        run_cmd(
            'edit Misaka -n MisakaMikoto -e mikoto@example.com --remove-alias Mikoto -a Onee-sama -g false -k yyy'
        )
        self.expect_user('Onee-sama', {
            'name': 'MisakaMikoto',
            'email': 'mikoto@example.com',
            'gpgsign': False,
            'gpgkey': 'yyy'
        })


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestRegister('test_register'))
    suite.addTest(TestEdit('test_edit'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

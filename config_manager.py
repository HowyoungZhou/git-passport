import json
import os

CONF_ENV = 'GIT_PASS_CONF'
CONF_FILE = 'config.json'
ETC_LOC = '/etc/git-pass'

DEFAULT_CONFIG = {
    'users': {
    },
    'aliases': {
    }
}


def get_conf_file() -> str:
    for conf_loc in (os.environ.get(CONF_ENV), os.curdir, os.path.expanduser("~"), ETC_LOC):
        if conf_loc is None:
            continue
        conf_file = os.path.join(conf_loc, CONF_FILE)
        if os.path.exists(conf_file):
            return conf_file
    return None


def get_default_conf_loc() -> str:
    loc_map = {
        'linux': ETC_LOC,
        'nt': os.path.expanduser("~")
    }
    return loc_map.get(os.name, os.curdir)


class ConfigManager:
    def __init__(self):
        self.conf_file = get_conf_file()
        if self.conf_file is None:
            self.conf_file = os.path.join(get_default_conf_loc(), CONF_FILE)
            self.config = DEFAULT_CONFIG
        else:
            self.config = self._read_conf_file()

    def _read_conf_file(self) -> dict:
        if self.conf_file is None:
            return None
        with open(self.conf_file, 'r') as f:
            return json.load(f, encoding='utf-8')

    def save(self) -> None:
        with open(self.conf_file, 'w')as f:
            json.dump(self.config, f)

    def get(self, name: str, default=None):
        return self.config.get(name, default)

    def get_user(self, name: str) -> dict:
        user = self.get('users').get(name)
        if user is None:
            name = self.get('aliases').get(name)
            return self.get('users').get(name)
        else:
            return user

    def add_user(self, name, email):
        self.get('users')[name] = {
            'user.name': name,
            'user.email': email
        }
        self.save()

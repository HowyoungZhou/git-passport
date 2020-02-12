import json
import os

import gitu

CONF_ENV = 'GITU_CONF'
CONF_FILE = 'config.json'
LINUX_CONF_LOC = '/etc/gitu'
NT_CONF_LOC = os.path.join(os.path.expanduser("~"), '.gitu')

GIT_CONF = {
    'name': 'user.name',
    'email': 'user.email',
    'gpgkey': 'user.signingkey',
    'gpgsign': 'commit.gpgsign'
}


class User:
    def __init__(self):
        self.name = None
        self.email = None
        self.gpgkey = None
        self.gpgsign = None

    @staticmethod
    def from_dict(conf: dict):
        user = User()
        for k, v in user.__dict__.items():
            setattr(user, k, conf.get(k))
        return user

    def get_git_configs(self) -> dict:
        res = {}
        for attr, git_conf in GIT_CONF.items():
            conf = getattr(self, attr)
            if conf is not None:
                res[git_conf] = conf
        return res

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def update(self, conf: dict):
        for k, v in conf.items():
            if v is not None:
                setattr(self, k, v)


def get_conf_file() -> str or None:
    if CONF_ENV in os.environ:
        return os.path.join(os.environ[CONF_ENV], CONF_FILE)

    for conf_loc in (os.curdir, NT_CONF_LOC, LINUX_CONF_LOC):
        if conf_loc is None:
            continue
        conf_file = os.path.join(conf_loc, CONF_FILE)
        if os.path.exists(conf_file):
            return conf_file
    return None


def get_default_conf_loc() -> str:
    loc_map = {
        'posix': LINUX_CONF_LOC,
        'nt': NT_CONF_LOC
    }
    return loc_map.get(os.name, os.curdir)


class Config:
    def __init__(self):
        self.users = {}
        self.aliases = {}
        self.conf_file = get_conf_file()
        if self.conf_file is None:
            self.conf_file = os.path.join(get_default_conf_loc(), CONF_FILE)
        self._read_conf_file()

    def _read_conf_file(self):
        if not os.path.exists(self.conf_file):
            return

        with open(self.conf_file, 'r') as f:
            conf = json.load(f, encoding='utf-8')
            self.aliases = conf.get('aliases', {})
            self.users = {}
            for user_dict in conf.get('users', []):
                user = User.from_dict(user_dict)
                self.users[user.name] = user

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.conf_file), exist_ok=True)
        with open(self.conf_file, 'w')as f:
            conf = {
                'version': gitu.__version__,
                'aliases': self.aliases,
                'users': [user.to_dict() for user in self.users.values()],
            }
            json.dump(conf, f, indent=2)

    def get_user(self, name_or_alias: str) -> User:
        user = self.users.get(name_or_alias)
        if user is None:
            name_or_alias = self.aliases.get(name_or_alias)
            return self.users.get(name_or_alias)
        else:
            return user

    def add_user(self, user: User):
        self.users[user.name] = user
        self.save()

    def get_users(self):
        return self.users.values()

    def remove_user(self, name):
        if name not in self.users:
            return
        self.users.pop(name)
        # Remove all aliases of the user
        self.aliases = {alias: orig for alias, orig in self.aliases.items() if name != orig}
        self.save()

    def update_user(self, user):
        self.users[user.name] = user
        self.save()

    def update_user_name(self, name, new_name):
        user = self.users[name]
        user.name = new_name
        self.users[new_name] = user
        self.users.pop(name)
        aliases = self.aliases
        for alias, orig in aliases.items():
            if name == orig:
                aliases[alias] = new_name
        self.save()

    def append_alias(self, name: str, alias: str):
        self.aliases[alias] = name
        self.save()

    def remove_alias(self, alias: str):
        if alias in self.aliases:
            self.aliases.pop(alias)
        self.save()

    def get_aliases_of_users(self):
        res = {}
        for alias, name in self.aliases.items():
            res.setdefault(name, [])
            res[name].append(alias)
        return res

from gitpassport import git_config
from gitpassport.config_manager import ConfigManager

config = ConfigManager()


def login(args):
    user = config.get_user(args.name)
    if user is None:
        print('User %s not found.' % args.name)
        exit(-1)
    for k, v in user.items():
        git_config.replace_all(k, v, args.git_conf_file)
    print('You are now logged in as %s <%s>.' % (user['user.name'], user['user.email']))


def register(args):
    config.add_user(args.name, args.email)
    print('%s <%s> registered.' % (args.name, args.email))


def view(args):
    print('You are now logged in as %s <%s>.' % (
        git_config.get('user.name', args.git_conf_file), git_config.get('user.email', args.git_conf_file)))


def list_users(args):
    print('Registered users:')
    for user in config.get_users():
        print('%s <%s>' % (user['user.name'], user['user.email']))


def remove(args):
    config.remove_user(args.name)

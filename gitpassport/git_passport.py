from gitpassport import git_config
from gitpassport.config_manager import ConfigManager

config = ConfigManager()


def get_user(name_or_alias) -> dict:
    user = config.get_user(name_or_alias)
    if user is None:
        print('User %s not found.' % name_or_alias)
        exit(1)
    return user


def check_name_conflict(name_or_alias: str, replace: bool):
    user = config.get_user(name_or_alias)
    if user is not None:
        if replace:
            config.remove_user(user['user.name'])
        else:
            print('User %s already exists.' % name_or_alias)
            exit(2)


def login(args):
    user = get_user(args.name)
    for k, v in user.items():
        git_config.replace_all(k, v, args.git_conf_file)
    print('You are now logged in as %s <%s>.' % (user['user.name'], user['user.email']))


def register(args):
    check_name_conflict(args.name, args.replace)
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
    user = get_user(args.name)
    config.remove_user(user['user.name'])


def edit(args):
    user = get_user(args.name)
    if args.email is not None:
        user['user.email'] = args.email
        config.update_user(user['user.name'], user)
    if args.new_name is not None:
        check_name_conflict(args.new_name, args.replace)
        config.update_user_name(user['user.name'], args.new_name)
    if args.alias is not None:
        check_name_conflict(args.alias, args.replace)
        config.append_alias(user['user.name'], args.alias)
    if args.remove_alias is not None:
        config.remove_alias(args.remove_alias)

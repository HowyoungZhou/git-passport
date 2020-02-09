#!/usr/bin/python3

import argparse

import git_config
from config_manager import ConfigManager

manager = ConfigManager()


def login(args):
    user = manager.get_user(args.name)
    if user is None:
        print('User %s not found.' % args.name)
        exit(-1)
    for k, v in user.items():
        git_config.replace_all(k, v, 'global' if vars(args)['global'] else 'local')
    print('You are now logged in as %s <%s>.' % (user['user.name'], user['user.email']))


def register(args):
    manager.add_user(args.name, args.email)
    print('%s <%s> registered.' % (args.name, args.email))


def view(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    subparsers = parser.add_subparsers()

    login_parser = subparsers.add_parser('login', aliases=['l'])
    login_parser.add_argument('name')
    login_parser.add_argument('-g', '--global', action='store_true')
    login_parser.set_defaults(func=login)

    register_parser = subparsers.add_parser('register', aliases=['r'])
    register_parser.add_argument('name')
    register_parser.add_argument('email')
    register_parser.set_defaults(func=register)

    view_parser = subparsers.add_parser('view', aliases=['v'])
    view_parser.add_argument('-a', '--all')
    view_parser.set_defaults(func=view)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

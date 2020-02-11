import argparse

import gitu
import gitu.functions as functions


def print_help(args):
    args.parser.print_help()


def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + gitu.__version__)
    parser.set_defaults(func=print_help)
    parser.set_defaults(parser=parser)
    subparsers = parser.add_subparsers()

    git_conf_parser = argparse.ArgumentParser(add_help=False)
    git_conf_parser.add_argument('--local', action='store_const', const='local', dest='git_conf_file',
                                 help='write to or read from the repository .git/config file (default)')
    git_conf_parser.add_argument('-g', '--global', action='store_const', const='global', dest='git_conf_file',
                                 help='write to or read from global ~/.gitconfig file')
    git_conf_parser.add_argument('-s', '--system', action='store_const', const='system', dest='git_conf_file',
                                 help='write to or read from system-wide $(prefix)/etc/gitconfig')
    git_conf_parser.add_argument('-w', '--worktree', action='store_const', const='worktree', dest='git_conf_file',
                                 help='write to or read from .git/config.worktree if extensions.worktreeConfig is present')
    git_conf_parser.set_defaults(git_conf_file='local')

    user_parser = argparse.ArgumentParser(add_help=False)
    user_parser.add_argument('-a', '--alias', help='add a alias to the user')
    user_parser.add_argument('-g', '--gpgsign', type=str2bool, help='whether all commits should be GPG signed')
    user_parser.add_argument('-k', '--gpgkey', help='GPG signing key')
    user_parser.add_argument('-r', '--replace', action='store_true',
                             help='replace the user if the name or alias already exists')

    login_parser = subparsers.add_parser('login', aliases=['l'], parents=[git_conf_parser],
                                         help='switch users')
    login_parser.add_argument('name', help='name or alias of the user')
    login_parser.set_defaults(func=functions.login)

    register_parser = subparsers.add_parser('add', aliases=['a'], help='add a new user', parents=[user_parser])
    register_parser.add_argument('name', help='name of the user')
    register_parser.add_argument('email', help='email of the user')
    register_parser.set_defaults(func=functions.register)

    view_parser = subparsers.add_parser('view', aliases=['v'], parents=[git_conf_parser],
                                        help='view information of users')
    view_parser.add_argument('-l', '--list', action='store_true', help='list all users')
    view_parser.add_argument('-a', '--all', action='store_true', help='show all information of users')
    view_parser.set_defaults(func=functions.view)

    edit_parser = subparsers.add_parser('edit', aliases=['e'], help='edit the information of a user',
                                        parents=[user_parser])
    edit_parser.add_argument('name', help='name or alias of the user')
    edit_parser.add_argument('-n', '--name', dest='new_name', help='new name of the user')
    edit_parser.add_argument('-e', '--email', help='new email of the user')
    edit_parser.add_argument('--remove-alias', metavar='ALIAS', help='remove the alias of the user')
    edit_parser.set_defaults(func=functions.edit)

    remove_parser = subparsers.add_parser('remove', aliases=['r'], help='remove a user')
    remove_parser.add_argument('name', help='name or alias of the user')
    remove_parser.set_defaults(func=functions.remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

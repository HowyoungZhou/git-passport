import argparse

import gitpassport.git_passport as gitpass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    subparsers = parser.add_subparsers()

    git_conf_parser = argparse.ArgumentParser(add_help=False)
    git_conf_parser.add_argument('-g', '--global', action='store_const', const='global', dest='git_conf_file')
    git_conf_parser.add_argument('-s', '--system', action='store_const', const='global', dest='git_conf_file')
    git_conf_parser.add_argument('-w', '--worktree', action='store_const', const='global', dest='git_conf_file')
    git_conf_parser.set_defaults(git_conf_file='local')

    login_parser = subparsers.add_parser('login', aliases=['l'], parents=[git_conf_parser])
    login_parser.add_argument('name')
    login_parser.set_defaults(func=gitpass.login)

    register_parser = subparsers.add_parser('register', aliases=['r'])
    register_parser.add_argument('name')
    register_parser.add_argument('email')
    register_parser.set_defaults(func=gitpass.register)

    view_parser = subparsers.add_parser('view', aliases=['v'], parents=[git_conf_parser])
    view_parser.set_defaults(func=gitpass.view)

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-a', '--all', action='store_true')
    list_parser.set_defaults(func=gitpass.list_users)

    remove_parser = subparsers.add_parser('remove', aliases=['d', 'delete'])
    remove_parser.add_argument('name')
    remove_parser.set_defaults(func=gitpass.remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

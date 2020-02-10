# git-passport
Account manager for git users with multiple accounts.

## Install
Install git-passport from PyPi:

```
pip3 install gitpassport
```

## Usage
```
usage: git-pass [-h] {login,l,add,a,view,v,edit,e,remove,r} ...

positional arguments:
  {login,l,add,a,view,v,edit,e,remove,r}
    login (l)           switch users
    add (a)             add a new user
    view (v)            view information of users
    edit (e)            edit the information of a user
    remove (r)          remove a user

optional arguments:
  -h, --help            show this help message and exit
```

### Add a user
#### Usage
```
usage: git-pass add [-h] [-r] [-a ALIAS] [-g] name email

positional arguments:
  name                  name of the user
  email                 email of the user

optional arguments:
  -h, --help            show this help message and exit
  -r, --replace         replace the user if the name or alias already exists
  -a ALIAS, --alias ALIAS
                        add a alias to the user
  -g, --gpgsign         set commit.gpgsign to true
```

#### Example
```bash
# Add a new user Misaka
git-pass add Misaka misaka@example.com
# Add a new user Shirai with alias Kuroko
git-pass a -a Kuroko Shirai shirai@example.com
```

### Switch users
#### Usage
```
usage: git-pass login [-h] [--local] [-g] [-s] [-w] name

positional arguments:
  name            name or alias of the user

optional arguments:
  -h, --help      show this help message and exit
  --local         write to or read from the repository .git/config file
                  (default)
  -g, --global    write to or read from global ~/.gitconfig file
  -s, --system    write to or read from system-wide $(prefix)/etc/gitconfig
  -w, --worktree  write to or read from .git/config.worktree if
                  extensions.worktreeConfig is present
```

#### Example
```bash
# Login as Misaka
git-pass login Misaka
# Login as Shirai Kuroko globally
git-pass l -g Kuroko
```

### View users
#### Usage
```
usage: git-pass view [-h] [--local] [-g] [-s] [-w] [-l] [-a]

optional arguments:
  -h, --help      show this help message and exit
  --local         write to or read from the repository .git/config file
                  (default)
  -g, --global    write to or read from global ~/.gitconfig file
  -s, --system    write to or read from system-wide $(prefix)/etc/gitconfig
  -w, --worktree  write to or read from .git/config.worktree if
                  extensions.worktreeConfig is present
  -l, --list      list all users
  -a, --all       show all information of users
```

#### Example
```bash
# View local user
git-pass view
# View global user
git-pass v -g
# List all users
git-pass v -l
# List all users in details
git-pass v -la
```

### Edit a user
#### Usage
```
usage: git-pass edit [-h] [-n NEW_NAME] [-e EMAIL] [-a ALIAS]
                     [--remove-alias ALIAS] [-g] [-r]
                     name

positional arguments:
  name                  name or alias of the user

optional arguments:
  -h, --help            show this help message and exit
  -n NEW_NAME, --name NEW_NAME
                        new name of the user
  -e EMAIL, --email EMAIL
                        new email of the user
  -a ALIAS, --alias ALIAS
                        add a new alias to the user
  --remove-alias ALIAS  remove the alias of the user
  -g, --gpgsign         set commit.gpgsign to true
  -r, --replace         replace the user if the name or alias already exists
```

#### Example
```bash
# Rename Misaka to Mikoto
git-pass edit Misaka -n Mikoto
# Change Email
git-pass e Shirai -e shirai@gakuen-toshi.tech
# Add alias
git-pass e -a Onee-sama Mikoto
# Remove alias
git-pass e --remove-alias Onee-sama Mikoto
```

### Remove a user
#### Usage
```
usage: git-pass remove [-h] name

positional arguments:
  name        name or alias of the user

optional arguments:
  -h, --help  show this help message and exit
```

#### Example
```bash
# Remove a user
git-pass remove Kamijou
```

## Exit status

The status is one of the follows:

- `0 (SUCCESS)`: the operation succeeded.
- `1 (USER_NOT_FOUND)`: the user doesn't exist.
- `2 (USER_EXISTS)`: the user already exists. To replace the user, use `-r`/`--replace`.
- `3 (GIT_ERROR)`: failed to execute a git command.

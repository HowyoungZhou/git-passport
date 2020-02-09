import subprocess


def replace_all(name: str, value: str, file: str = 'local'):
    subprocess.run(['git', 'config', '--' + file, name, value], check=True)

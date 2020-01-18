# FireCatcherBot

## Installation

### UPDATE APT

`
sudo apt update
`

### PIP3

`
sudo apt install python3-pip
`

### PIPENV

`
pip3 install --user pipenv
`

### PYENV

#### PRERREQUISITES

`
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
`

#### INSTALL PYENV

`
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
`

`
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
`

`
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
`

`
exec "$SHELL"
`

`
pyenv install  3.7.5
`

`
cd env_folder
`

`
pipenv install
`

`
pipenv shell
`

`
python echobot.py
`

## TODO

- Implement propper logging
- Handle user, conversations properly (with redis)
- Implement states
- Handle concurrency and asyncronicity
- Properly give options to download or not the pics (via commandline instead of hardcoding it)
- Add environments, constants
- Add comments
- More refactoring
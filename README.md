# hackenv
Handy dotfiles, environments, and tools for binary exploitation

## Usage

For using the ``python`` scripts, set up a virtual environment like is done below

```sh
#!/bin/sh

# Start a virtual environment and upgrade pip

VENV_DIR="$HOME/venvs/hacker"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python3 -m pip install --upgrade pip

# Install from requirements
# Alternatively, get the latest version of the libraries like this
# python3 -m pip install qiling pwntools angr ropper lief
python3 -m pip install -r requirements.txt
```

The ``vimrc`` can be copied to wherever your ``vim`` program expects it to be.

``git.core.excludesFile`` are a nice set of excludes for
text editors and IDEs I use.

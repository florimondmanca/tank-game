# tank-game

Tank Game is, as one might expect, a tanks-themed video game.

Made with Python and Pygame in 2015 by Florimond Manca and @GCoiffier.


## Installation

### For developers

First, clone the repo. Then, make sure Pygame is installed. Then create a virtualenv install dependencies:

```
$ virtualenv env -p python3
$ source env/bin/activate
(env) $ env/bin/pip install -r requirements.txt
```

> On macOS, there is a known problem with Pygame and virtual environments, presumably due to how macOS handles the SDL framework shipped with Pygame. This problem makes Pygame not recognize input events such as mouse or keyboard. You'll have to use a system installation instead.

You can start the game with the `main.py` script:

```
$ python3 main.py
```

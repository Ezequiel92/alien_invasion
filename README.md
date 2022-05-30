<div align="center">
    <h1>👾 Alien invasion</h1>
</div>

<p align="center">
    <a href="https://www.python.org/"><img src="https://forthebadge.com/images/badges/made-with-python.svg"></a>
</p>

<p align="center">
    <a href="https://github.com/ezequiel92/alien_invasion/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ezequiel92/alien_invasion?style=flat&logo=GNU&labelColor=2B2D2F"></a>
    <a href="https://www.codefactor.io/repository/github/ezequiel92/alien_invasion"><img src="https://img.shields.io/codefactor/grade/github/ezequiel92/alien_invasion?style=flat&logo=CodeFactor&labelColor=2B2D2F"></a>
</p>

A 2D game made with [pygame](https://www.pygame.org/) and based on the exercise proposed in chapters 12, 13 and 14 of [_Python Crash Course_](https://ehmatthes.github.io/pcc_2e/) by Eric Matthes (2ed.), with some added features:

* Initial menu to choose between playing a new game, loading a saved game, or seeing a the ranking of players.
* Menu to choose between playing with at full screen or in window mode.
* Menu to choose the difficulty level.
* Menu to create an user, play as an already created user or play anonymously.
* You can pause the game, and then resume, quit or save it.
* Sound effects.

## 🚀 Description

This game resembles the classic [Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders) from the 70'.

You can control the ship's horizontal position and shoot bullets (there can be up to three bullets on the screen at any time). When a bullet hits an alien, it disappears and you get points. When the whole fleet of aliens is eliminated, you go to the next level. In each new level the fleet descends faster.

## 🕹️ Controls and shortcuts

### Gameplay

* Press the **right arrow** and **left arrow** keys to move the ship.
* Press **space bar** to shot bullets.

### Shortcuts

* Press **s** to start a game when the _Play_ button is on the screen.
* Press **p** to pause or resume the game.
* Press **q** to quit the game and return to the main menu.

## ℹ️ Some things to note

* Trailing and leading white spaces will be ignored in usernames, so "User_1" and " User_1 " will be considered the same and will be stored as "User_1".

* The maximum level is 100, if you reach it, you win the game. Because the score for ending the game is fixed, whoever wins the game first (with all 3 lives left) will have the first place in the ranking.

* The game stores locally the users, their scores, their saved games, and the ranking in `.json` files.

## 🖥️ Setup

To run the game from source

* Clone the project

```bash
 git clone https://github.com/Ezequiel92/alien_invasion.git
```

* Go to the project directory

```bash
cd path/to/alien_invasion
```

* Install the dependencies given by the `requirements.txt` file

```bash
pip install -r requirements.txt
```

* Run the game

```bash
python ./src/alien_inavasion.py
```

The game can be compiled into a binary file with the [pyinstaller](https://www.pyinstaller.org/) library. An already compiled version for Windows 10/11 is provided in the `alien_invasion.zip` file. The `.exe` within should work in any Windows 10/11 machine.

To create a portable version of your own, run (within the game folder)

```sh
pyinstaller --clean --workpath "binary/TEMP" --distpath "binary" alien_invasion.spec
```

* pyinstaller is in the `requirements.txt` as a dependency and the `.spec` file is provided.
* The executable will be saved inside the folder `binary/alien_invasion/`, along with all the necessary dependencies.
* The `binary/TEMP` folder can be deleted.
* The executable should work in any system like the one in which you run `pyinstaller`.

## ⚙️ Game assets

* 🖼️ All images (.bmp) are from the [book website](https://ehmatthes.github.io/pcc_2e/).
* 🎵 All the sounds (.wav) are from [freesound.org](https://freesound.org/):
  * [laser](https://freesound.org/people/jobro/sounds/35684/)
  * [fail_shot](https://freesound.org/people/KlawyKogut/sounds/154934/)
  * [click](https://freesound.org/people/stijn/sounds/43676/)
  * [loose_ship](https://freesound.org/people/myfox14/sounds/382310/)
  * [ambient](https://freesound.org/people/joshuaempyre/sounds/251461/)
  * [game_won](https://freesound.org/people/LittleRobotSoundFactory/sounds/270404/)

All the remaining game assets are rendered by `pygame` on the fly.

## ⚠️ Warning

This game is written as an exercise and may break at any moment. So, use it at your own risk.

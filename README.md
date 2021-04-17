# 👾 Alien invasion

[![ForTheBadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![GitHub](https://img.shields.io/github/license/Ezequiel92/BiblographyFormatter?style=flat-square)](https://github.com/Ezequiel92/BiblographyFormatter/blob/main/LICENSE) [![Maintenance](https://img.shields.io/maintenance/yes/2021?style=flat-square)](mailto:lozano.ez@gmail.com)

A 2D game made with the [pygame](https://www.pygame.org/) library and heavily based in the exercise proposed in chapters 12, 13 and 14 of [_Python Crash Course 2ed_](https://ehmatthes.github.io/pcc_2e/) by Eric Matthes, with some added features:

* Menu to choose between full screen or a floating window.
* Menu to choose the level of difficulty.
* Menu to create a user, play as an already created user or play anonymously.
* You can pause, and then resume, quit or save the game.
* Menu to choose between playing the game, seeing a ranking of users according to their scores, or loading up saved games (the exact screen state from when the game was saved is reproduced).
* Sound effects.

## 🚀 Description

You can control the ship's left and right position and shoot bullets (up to three bullets on screen at any time). When a bullet hits an alien, it disappears and you get points. When the whole fleet is eliminated, you go to the next level, and the new fleets start descending faster.

The game stores locally the users, scores, saved games, and the ranking, in `.json` files.

Trailing and leading whitespaces will be ignored in usernames, so "User_1" and " User_1 " will be considered the same user and will be stored as "User_1".

The maximum level is 100, if you reach it, you win the game. Because the score for ending the game is fixed, whoever wins the game first (with all 3 lives left) will forever be in the first place of the local ranking.

## 🕹️ Controls and shortcuts

### Gameplay

* Press the **right arrow** and **left arrow** keys to move the ship.
* Press **space bar** to shot bullets.

### Shortcuts

* Press **s** to start a game when the _Play_ button is on the screen.
* Press **p** to pause or resume the game.
* Press **q** to quit the game and return to the main menu.

## 🖥️ Requirements

To run the game from the source, just run `src/alien_inavasion.py`. The dependencies are given by the `requirements.txt`.

The game can be compiled into a binary file with the [pyinstaller](https://www.pyinstaller.org/) library. An already compiled version for Windows 10 is provided in the `alien_invasion.zip` file. The `.exe` within should work in any Windows 10 machine.

To create a portable version of your own, do as follows:

* Within the game folder, run: 

  ```bash
  pyinstaller --clean --workpath "binary/TEMP" --distpath "binary" alien_invasion.spec
  ```
  
  (pyinstaller is in the `requirements.txt` as a dependency and the `.spec` file provides the instructions to pyinstaller).
* The executable will be saved in the folder `binary/alien_invasion`, along with all the necessary dependencies.
* The `binary/TEMP` folder can be deleted and the executable should work in any system like the one you use to run `pyinstaller`.

## Game assets

* 🖼️ All images (BMP) are from the [book website](https://ehmatthes.github.io/pcc_2e/).
* 🔊 All the sounds (WAV) are from [freesound.org](https://freesound.org/): 
  * [laser](https://freesound.org/people/jobro/sounds/35684/)
  * [fail_shot](https://freesound.org/people/KlawyKogut/sounds/154934/)
  * [click](https://freesound.org/people/stijn/sounds/43676/)
  * [loose_ship](https://freesound.org/people/myfox14/sounds/382310/)
  * [ambient](https://freesound.org/people/joshuaempyre/sounds/251461/)
  * [game_won](https://freesound.org/people/LittleRobotSoundFactory/sounds/270404/)

The rest of the game assets are rendered by `pygame` on the fly.

## ⚠️ Warning

This script is written as an exercise and may break at any moment. So, no guarantees are given.
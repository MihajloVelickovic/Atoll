# Atoll

## About

[Atoll](https://www.marksteeregames.com/Atoll_rules.pdf) is a game played between two people, or versus a CPU player. 

It's a University project for the Artificial Intelligence course.

The CPU uses the Mini-Max algorithm with Alpha-Beta pruning.

Players can put stones on free fields using the mouse, or by pressing the letter + number combination of the desired field, and pressing ```Return``` or ```Space```.

The game has been won after there are at least 7 islands on the shortest perimiter path between islands connected by a single path

## Running

After cloning the repository, its recommended to create a Python Virtual Environment (venv) in the root folder. After activating the virtual environment, requirements must be installed

```pip install -r requirements.txt```

Finally, the game can be run:

```python main.py```

This will run the game in the console, firstly letting the player choose the parameters of the game, those being:

- Board size
- Game type
- ```if game_type == 2:```CPU or Human plays first
- Black or White plays first

After the parameters have been set, a pygame window will open, graphically depicting the board.

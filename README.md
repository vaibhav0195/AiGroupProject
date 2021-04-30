# CSP Model
In this branch is the code related to the CSP model for solving Minesweeper games.

# Requirements
This project requires **Python 3**
The only package requirement is the Python package 'numpy'. Can be installed with the following command:
`pip install numpy`

# Running
This code is meant to be executed on the root folder of this repository, that is, where the file *csp.py* is contained.

```
>>> from minesweeper.msgame import MSGame
>>> from csp import solve_minesweeper_csp
>>> ms = MSGame(10, 10, 10)
>>> solve_minesweeper_csp(ms)
```

# Contributions
The Minesweeper game framework was modified from [duguyue100's Minesweeper](https://github.com/duguyue100/minesweeper). The code inside *csp.py* was entirely written by Jorge González.

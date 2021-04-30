
A python Minesweeper game solved using DFS and BFS.


## How to Install

In order to install this package, you need to have at least

+   `numpy`
+   `pyqt`
+   `pandas`

installed. If you don't want to bother with details of packages installation,
you can use [Anaconda](https://anaconda.org/) as your Python distribution.

And then install the package by

__From PyPI (the latest stable version)__

```bash
pip install minesweeper
```

Once you installed, open cmd from the folder directory 
and then can start the game using the following commands

```bash
python
from minesweeper import *
from bfs_dfs import *
msgame = MSGame(10,10,10)
solve_bfs_dfs(msgame)
```



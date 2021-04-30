from Minesweeper import Minesweeper
import random
import timeit
import pandas as pd

minesweeper = None
AI_Board = None
GRID_SIZE = None
NUM_MINES = None

stat_list = []
stats = {'grid_size': None, 'no_mines': None, 'time': None, 'evaluations': 0, 'games_won': 0, 'games_lost': 0,
              'type': ''}


class AINode:
    def __init__(self, pos):
        self.pos = pos
        self.not_mine = False
        self.is_mine = False


class AIBoard:
    def __init__(self, grid_size):
        self.nodes = [[AINode((i, j)) for j in range(grid_size)] for i in range(grid_size)]

    def get_safe_nodes(self):
        flat = [n for x in self.nodes for n in x]
        return [x for x in flat if x.not_mine]

    def get_flat_nodes(self):
        return [n for x in self.nodes for n in x]

    def get_ainode_from_msnode(self, x):
        return self.nodes[x.pos[0]][x.pos[1]]



def init(grid_size, no_mines):
    global minesweeper
    global AI_Board
    global GRID_SIZE
    global NUM_MINES
    global stats

    minesweeper = Minesweeper(grid_size, no_mines)
    AI_Board = AIBoard(grid_size)
    GRID_SIZE = grid_size
    NUM_MINES = no_mines


def surrounding_nodes(x, y):
    stats['evaluations'] += 1
    a_node = minesweeper.nodes[x][y]
    assert a_node.adjacent_mines > 0
    if a_node.is_unrevealed:
        return
    # All unrevealed adjacent nodes are mines
    if mark_mines(a_node) > 0:
        unrev_adj_nodes = list(filter(lambda n: n.is_unrevealed, minesweeper.get_adj_nodes(*a_node.pos)))
        for unrevealed_adj_node in unrev_adj_nodes:
            mark_safe_node(unrevealed_adj_node)
    # There are unrevealed non-mines around node
    mark_safe_node(a_node)


def mark_safe_node(a_node):
    unrev_adj_nodes = list(filter(lambda n: n.is_unrevealed, minesweeper.get_adj_nodes(*a_node.pos)))
    if len(unrev_adj_nodes) > a_node.adjacent_mines:
        adj_nodes_ai = [AI_Board.get_ainode_from_msnode(a_node) for a_node in unrev_adj_nodes]
        # Nodes with are mines are known
        if sum(an.is_mine for an in adj_nodes_ai) == a_node.adjacent_mines:
            set_nodes_as_safe(unrev_adj_nodes)


def mark_mines(node):
    marked_mine = 0
    unrev_adj_nodes = list(filter(lambda n: n.is_unrevealed, minesweeper.get_adj_nodes(*node.pos)))
    if len(unrev_adj_nodes) == node.adjacent_mines:
        for n in unrev_adj_nodes:
            AI_Board.nodes[n.pos[0]][n.pos[1]].is_mine = True
            marked_mine += 1
    return marked_mine


def evalutable_node(node):
    return (not node.is_unrevealed) and (node.adjacent_mines > 0)


def set_nodes_as_safe(unrev_adj_nodes):
    for node in unrev_adj_nodes:
        x, y = node.pos[0], node.pos[1]
        if not AI_Board.nodes[x][y].is_mine:
            AI_Board.nodes[x][y].not_mine = True


def solve(bfs=True):
    queue = []
    #queue.extend(list(filter(evalutable_node, minesweeper.get_flat_nodes())))
    while 1<10:
        if len(queue)==0:
            starting_node = random.choice([n for n in minesweeper.get_flat_nodes()])
            value = minesweeper.click(starting_node.pos[0], starting_node.pos[1])
            if value == 0:
                stats['games_lost'] += 1
                return
            queue.extend(list(filter(evalutable_node, minesweeper.get_flat_nodes())))
        node_to_evaluate = queue.pop(0)
        surrounding_nodes(*node_to_evaluate.pos)
        safe_nodes = list(map(minesweeper.get_msnode_from_ainode, AI_Board.get_safe_nodes()))
        unrev_safe_nodes = list(filter(lambda n: n.is_unrevealed, safe_nodes))
        if unrev_safe_nodes:
            node_to_click = random.choice(unrev_safe_nodes)
            minesweeper.click(*node_to_click.pos)
            if is_game_won():
                print("GAME WON!!")
                stats['games_won'] += 1
                return
            for n in filter(evalutable_node, minesweeper.get_flat_nodes()):
                if not n in queue:
                    if bfs:
                        queue.append(n)
                    else:
                        queue.insert(0, n)


def is_game_won():
    return len(list(filter(lambda n: n.is_unrevealed, minesweeper.get_flat_nodes()))) == NUM_MINES


def start(bfs=True, grid_size=20, no_mines=40):
    init(grid_size, no_mines)
    stats['type'] = 'BFS' if bfs else 'DFS'
    minesweeper.start_game()
    solve(bfs)


def solve_bfs_dfs(ms):
    global stats

    grid_size = ms.board_height
    no_mines = ms.num_mines

    for bfs in [True, False]:
        stats = {'grid_size': str(grid_size) + "x" + str(grid_size), 'num_mines': no_mines, 'time': None,
                      'evaluations': 0,
                      'games_won': 0, 'games_lost': 0, 'type': ''}

        stats['time'] = timeit.timeit(f'start({bfs}, ' + str(grid_size) + ', ' + str(no_mines) + ')'
                                           , globals=globals(), number=200)

        stats['win_rate'] = stats['games_won']/(stats['games_won'] + stats['games_lost'])

        stat_list.append(stats)

    print(pd.DataFrame(stat_list))

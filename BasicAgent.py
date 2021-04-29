import numpy as np


class BaseAgent:

    def __init__(self, gameObject):
        self.gameObject = gameObject
        self.flags = []
        self.gameMap = self.gameObject.getGameState()


    def _basic_solver(self):
        
        
        ground = np.reshape(np.asarray(self.gameObject.getGameState()), -1)
        print("abc"+ground)
        for row in range(ground.shape[0]):
            for column in range(ground.shape[1]):
                if np.isnan(ground[row, column]) or self.flags[row, column]:
                    continue
                else:
                    if ground[row, column] == 0:
                        return ["click: ",self._query_all_neighbours(row, column)]

                    elif ground[row,column] == 8:
                        return ["flag: ",self._flag_all_neighbours(row, column)]

                    else:
                        if self._get_bomb(row, column) == ground[row, column]:
                            return ["click: ",self._query_all_neighbours(row, column)]
                        elif self._get_unexplored(row, column) == ground[row, column]:
                            return ["flag: ",self._flag_all_neighbours(row, column)]

    def _query_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1] and (not self.flags[row + i, column + j])
                        and np.isnan(self.gameMap[row + i, column + j])):
                            return [row + i, column + j]
                            #self.env.click_square(row + i, column + j)
                            #self.env.render_env()

    def _flag_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1] and (not self.flags[row + i, column + j])
                        and np.isnan(self.gameMap[row + i, column + j])):
                        return [row + i, column + j]
                        #self.env.add_mine_flag(row + i, column + j)
                        #self.env.render_env()

    def _get_bomb(self, row, column):
        bomb_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1] and self.flags[row + i, column + j]):
                        bomb_count = bomb_count + 1
        return bomb_count

    def _get_unexplored(self, row, column):
        unexplored_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1] and np.isnan(self.gameMap[row + i, column + j])):
                        unexplored_count = unexplored_count + 1
        return unexplored_count

    
    def nextMove(self):
        return self._basic_solver()
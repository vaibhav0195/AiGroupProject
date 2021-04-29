import numpy as np
import random


class BaseAgent:

    def __init__(self, gameObject):
        self.gameObject = gameObject
        self.flags = np.zeros(shape=(10,10))
        self.discovered = np.zeros(shape=(10,10))
        self.gameMap = self.gameObject.get_info_map()
        self.movemade = False


    def _basic_solver(self):
        ground = self.gameObject.get_info_map()
        ##print(ground)
        countermove = 0
        #print(self.gameObject.get_board())
        #print(self.gameObject.get_mine_map())
        while not self.gameObject.isGameOver():
            self.movemade = False
            for row in range(ground.shape[0]):
                for column in range(ground.shape[1]):
                    if ground[row, column] == 11 or self.flags[row, column]:
                        #print("in")
                        continue
                    else:
                        if ground[row, column] == 0:
                            #print("in4")
                            self._query_all_neighbours(row, column)
                            if(self.gameObject.isGameOver()):
                                break
                            '''if coordss is None:
                                continue
                            #return ["click",coordss[0],coordss[1]]
                            self.gameObject.play_move("click",coordss[0],coordss[1])
                            print("Click move made at:")
                            print(coordss[0])
                            print(coordss[1])'''

                        elif ground[row,column] == 8:
                            #print("in3")
                           self._flag_all_neighbours(row, column)
                           if(self.gameObject.isGameOver()):
                            break
                            '''if coordss is None:
                                continue
                            #return ["flag",coordss[0],coordss[1]]
                            self.gameObject.play_move("flag",coordss[0],coordss[1])
                            self.flags[coordss[0], coordss[1]] = True
                            print("Flag move made at:")
                            print(coordss[0])
                            print(coordss[1])'''

                        else:
                            #print("in2")
                            #print(ground[row, column])
                            if self._get_bomb(row, column) == ground[row, column]:
                                self._query_all_neighbours(row, column)
                                if(self.gameObject.isGameOver()):
                                    break
                                #print("get bomb")
                                '''if coordss is None:
                                    continue
                                #return ["click",coordss[0],coordss[1]]
                                self.gameObject.play_move("click",coordss[0],coordss[1])
                                print("Click move made at:")
                                print(coordss[0])
                                print(coordss[1])'''
                            elif self._get_unexplored(row, column) == ground[row, column]:
                                self._flag_all_neighbours(row, column)
                                if(self.gameObject.isGameOver()):
                                    break
                                #print("get undiscovered")
                                '''if coordss is None:
                                    continue
                                #return ["flag",coordss[0],coordss[1]]
                                self.gameObject.play_move("flag",coordss[0],coordss[1])
                                self.flags[coordss[0], coordss[1]] = True
                                print("Flag move made at:")
                                print(coordss[0])
                                print(coordss[1])'''
                countermove = countermove + 1

            
            #return ["click",random.randint(0,10),random.randint(0,10)]
            if not self.movemade and not self.gameObject.isGameOver():
                psx = random.randint(0,ground.shape[0]-1)
                psy = random.randint(0,ground.shape[1]-1)
                while not (self.gameMap[psx, psy]) == 11:
                    psx = random.randint(0,ground.shape[0]-1)
                    psy = random.randint(0,ground.shape[1]-1)
                ##print("Random move made at:")
                ##print(psx)
                ##print(psy)
                self.gameObject.play_move("click",psy,psx)
                self.gameMap = self.gameObject.get_info_map()
                ##print(self.gameMap)
                if(self.gameObject.isGameOver()):
                    break
            #if(countermove > 3):
                #print(self.gameMap)

                    

    def _query_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    #print("row and col")
                    #print(row)
                    #print(column)
                    continue
                if (row + i >= 0 and column + j >= 0):
                    #print(i)
                    #print(j)
                    if(row + i < self.gameMap.shape[0] and column + j < self.gameMap.shape[1] and (not self.flags[row + i, column + j])):
                        #print("here")
                        #print(row + i)
                        #print(column + j)
                        #print(self.gameMap[row + i, column + j])
                        #print("end")
                        if((self.gameMap[row + i, column + j]) == 11):
                            #print("qry")
                            ##if(self.gameObject.IsActionValid(row + i,column + j)):
                                ##print(self.gameObject.check_move("click",row + i,column + j))
                            #self.gameObject.play_move("click",row + i,column + j)
                            self.gameObject.play_move("click",column + j,row + i)
                            ##print(self.gameObject.getGameState())
                            self.movemade = True
                            ##print("Click move made at:")
                            ##print(row + i)
                            ##print(column + j)
                            ##print(self.gameMap[row + i, column + j])
                            self.gameMap = self.gameObject.get_info_map()
                            ##print(self.gameMap)
                            if(self.gameObject.isGameOver()):
                                break
                            #return [row + i, column + j]
                            #self.env.click_square(row + i, column + j)
                            #self.env.render_env()

    def _flag_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1] and (not self.flags[row + i, column + j])
                        and self.gameMap[row + i, column + j] == 11):
                        self.gameObject.play_move("flag",row + i,column + j)
                        self.movemade = True
                        self.flags[row + i, column + j] = True
                        ##print("Flag move made at:")
                        ##print(row + i)
                        ##print(column + j)
                        self.gameMap = self.gameObject.get_info_map()
                        ##print(self.gameMap)
                        if(self.gameObject.isGameOver()):
                                break
                        #return [row + i, column + j]
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
        #print("bomb count")
        #print (bomb_count)
        return bomb_count

    def _get_unexplored(self, row, column):
        unexplored_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.gameMap.shape[0]
                        and column + j < self.gameMap.shape[1]):
                        #print("unn")
                        #print(self.gameMap[row + i, column + j])
                        if(self.gameMap[row + i, column + j] == 11):
                            unexplored_count = unexplored_count + 1
        #print("unexpected")
        #print (unexplored_count)
        return unexplored_count

    
    def nextMove(self):
        return self._basic_solver()
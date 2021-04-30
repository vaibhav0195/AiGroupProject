from minesweeper.msgame import MSGame
import numpy as np
from sklearn.linear_model import Ridge
import pickle

class QLearningAgentAI:

    def __init__(self,discountFactor,epsilonProb,memorySize,alphaRidge,savePath,gameObject=MSGame(10, 10, 5)):

        self.counterMem = 0
        self.counterWins = 0
        self.counterUpdates = 0
        self._discountFactor = discountFactor
        self._epsilonProb = epsilonProb
        self._memorySize = memorySize
        self._alphaRidge = alphaRidge
        self._savepath = savePath
        self.gameObject = gameObject
        self.actionsId = np.arange(self.gameObject.board_width * self.gameObject.board_height)
        self.rng = np.random.RandomState(123)
        self.W = self.rng.uniform(low=-1e-5, high=1e-5,
                                  size=[self.gameObject.board_width * self.gameObject.board_height,
                                        self.gameObject.board_width * self.gameObject.board_height * self.gameObject.cellsStateCount])
        self.b = np.zeros([self.gameObject.board_width * self.gameObject.board_height])
        cells = np.asarray(self.gameObject.getGameState()).reshape(-1)
        self.currentState = np.eye(self.gameObject.cellsStateCount)[np.asarray(cells, 'int')].reshape([-1])

        self.lstState = np.zeros([self._memorySize, self.currentState.shape[0]])
        self.lstAction = np.zeros([self._memorySize])
        self.lstTarget = np.zeros([self._memorySize])

    def moveToNextState(self):
        """
        Move to the next state from the current
        This returns if there was explosion or not in order to reset the game from the controller.
        """
        self.lstState[self.counterMem,:] = self.currentState
        #Choose action and play it
        result,selectedAction = self.selectActionUsingEpsilonGreedy(self.currentState)
        # print(selectedAction)
        self.lstAction[self.counterMem] = selectedAction
        #Get the new state
        cells2 = np.reshape(np.asarray(self.gameObject.getGameState()),-1)
        # print(self.gameObject.getGameState())
        # cells2[np.isnan(cells2.astype(float))]=11
        if result.explosion:
            self.lstTarget[self.counterMem] = result.reward
        else:
            self.currentState = np.reshape(np.eye(self.gameObject.cellsStateCount)[np.asarray(cells2,'int')],[-1])
            maxQ = self.qFunction(self.currentState)
            self.lstTarget[self.counterMem] = result.reward + self._discountFactor * maxQ
        self.counterMem += 1
        if self.counterMem==self._memorySize:
            # print(self.COUNTERMEM)
            self.updateParams()
            #reset memory (**MIGHT KEEP SOME OF THE VALUES LATER**)
            # self.lstTarget=[]
            # self.lstAction=[]
            # self.lstState =[]
            self.counterMem = 0
        return result.explosion

    def getGameState(self):
        return self.gameObject.getGameState()

    def getValidAction(self, Q, maxAction):
        expo = np.reshape(np.asarray(self.gameObject.getExposed()).T, -1)
        # print(expo)
        tmp = np.asarray(np.logical_not(expo), 'float')
        # print(tmp)
        tmp[tmp == 0] = -np.inf
        Q[expo] = np.abs(Q[expo])
        if maxAction:
            validActionsQ = tmp * Q
            # pdb.set_trace()
            return np.argmax(validActionsQ)
        else:
            indices = np.arange(len(self.actionsId))
            self.rng.shuffle(indices)
            counter = 0
            while tmp[indices[counter]] == -np.inf:
                counter += 1
            # pdb.set_trace()
            return indices[counter]

    def qFunction(self, currentState):
        """
        Get The max Q Value using the best action
        """

        Q = np.dot(self.W, currentState) + self.b
        expo = np.reshape(np.asarray(self.gameObject.getExposed()).T, -1)
        tmp = np.asarray(np.logical_not(expo), 'float')
        tmp[tmp == 0] = -np.inf
        Q[expo] = np.abs(Q[expo])
        validActionsQ = tmp * Q
        return np.max(validActionsQ)

    def selectActionUsingEpsilonGreedy(self, currentState):
        Q = np.dot(self.W, currentState) + self.b

        # zipped = list(zip(Q,self.actionsId))
        # zipped.sort(key = lambda t: t[0],reverse=True)
        # q,aIds = zip(*zipped)
        takeMaxAction = self.rng.binomial(n=1, p=1 - self._epsilonProb, size=1)[0]
        # print(takeMaxAction)
        selectedActionId = self.getValidAction(Q, takeMaxAction)
        # pdb.set_trace()
        # print(selectedActionId)
        coords = int(selectedActionId / self.gameObject.board_width), int(selectedActionId % self.gameObject.board_height)
        # print(coords)
        result = self.gameObject.play_move("click",*coords)

        return result, selectedActionId

    def updateParams(self):
        selectedActions = np.asarray(self.lstAction)
        for k in range(len(self.actionsId)):
            select = selectedActions == k
            A = self.lstState[select]
            b = self.lstTarget[select]

            if A.shape[0] > 0:
                clf = Ridge(alpha=self._alphaRidge)
                try:
                    # pdb.set_trace()
                    res = clf.fit(A, b.flatten())
                    self.W[k, :] = res.coef_
                    self.b[k] = res.intercept_
                except Exception as e:
                    print(e)
        # pdb.set_trace()
        self.SaveParams()
        self.counterUpdates += 1
        self._epsilonProb = np.maximum(0, self._epsilonProb - 0.02)
        print(self.counterWins)
        self.counterWins = 0

    def next(self,):
        cells = np.asarray(self.gameObject.getGameState()).reshape(-1)
        # cells[np.isnan(cells.astype(float))] = 9
        currentState = np.eye(self.gameObject.cellsStateCount)[np.asarray(cells, 'int')].reshape([-1])
        counter = 0
        Q = np.dot(self.W, currentState) + self.b
        zipped = list(zip(Q, self.actionsId))
        zipped.sort(key=lambda t: t[0], reverse=True)
        q, aIds = zip(*zipped)
        row = int(aIds[counter] / self.gameObject.board_height)
        col = int(aIds[counter] % self.gameObject.board_width)
        while self.gameObject.IsActionValid(col, row) == False:
            counter += 1
            row = int(aIds[counter] / self.gameObject.board_height)
            col = int(aIds[counter] % self.gameObject.board_width)
        return row, col

    def resetAgentState(self):
        self.gameObject.reset_game()
        cells = np.asarray(self.gameObject.getGameState()).reshape(-1)
        self.currentState = np.eye(self.gameObject.cellsStateCount)[np.asarray(cells, 'int')].reshape([-1])

    def SaveParams(self):
        pickle.dump([[self.W,self.b],
                      [self.gameObject]  ],open(self._savepath+str(self.counterWins),'wb' ))
    def loadParams(self,params):
        self.W = params[0]
        self.b = params[1]

    def isGameOver(self):
        return self.gameObject.isGameOver()

def LoadModel(path):
    gameObject = MSGame(10, 10, 12)
    dictGame = {
        'discountFactor': 0.9,
        'memorySize': 500000,
        'alphaRidge': 0.001,
        'epsilonProb': 0.2,
        'savePath': "model.pkl1878",
        'gameObject': gameObject
    }
    params, extraParams = pickle.load(open(path,'rb'))
    agent = QLearningAgentAI(**dictGame)
    agent.loadParams(params)
    return agent
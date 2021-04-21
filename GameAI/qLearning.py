from minesweeper.msgame import MSGame

class QLearningAgentAI:
    def __init__(self,gameObject=MSGame(10, 10, 5)):
        self.gameObject = gameObject

    def getGameState(self):
        return self.gameObject.getGameState()
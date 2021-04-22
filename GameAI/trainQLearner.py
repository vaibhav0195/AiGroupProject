from GameAI.qLearning import QLearningAgentAI
from minesweeper.msgame import MSGame
from minesweeper.util import GameResult
import numpy as np
from tqdm import tqdm

def testGames(num_games,game, ai, viz=None):
    results = []
    for x in tqdm(range(num_games)):
        # game = Game(config)
        if viz: print("HUHUHUHUH")
        while not game.isGameOver():
            # pdb.set_trace()
            coords = ai.next()
            result = game.play_move("click",*coords)
            print(result)
            if result is None:
                continue
            # print(np.asarray(game.getGameState()))
            # pdb.set_trace()

        if result.explosion:
            print("EXPLOOOOOOOOOSION")
        else:
            print("Game won")
            # pdb.set_trace()
        results.append(GameResult(not game.explosion, game.num_moves))
    return results

def trainAi(ai,iterationCount):
    # winCounter = 0
    for x in range(iterationCount):
        print("Running iteration {} number of wins {}".format(x,ai.counterWins))
        isExplosion = ai.moveToNextState()
        if isExplosion:
            # print("GAME LOST AFTER "+str(ai.gameObject.num_moves)+" . Iteration: "+str(x))
            ai.resetAgentState()
            pass

        else:
            if ai.gameObject.game_status ==1:
                # print("GAME Won AFTER " + str(ai.gameObject.num_moves) + " . Iteration: " + str(x))
                ai.counterWins += 1
        # if np.sum(np.isnan(np.asarray(game.get_state()).astype(float)))== MINES_COUNT:
    # print("*********** WELL DONE ***************")
    # pdb.set_trace()

if __name__ == '__main__':
    gameObject = MSGame(10, 10, 12)
    dictGame = {
        'discountFactor': 0.9,
        'memorySize': 1000000,
        'alphaRidge': 0.001,
        'epsilonProb': 0.2,
        'savePath': "model.pkl",
        'gameObject' : gameObject
    }
    gameAgent = QLearningAgentAI(**dictGame)
    trainAi(gameAgent,int(2e7))
    # testGames(1000,gameObject,gameAgent)
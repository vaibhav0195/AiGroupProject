from GameAI.qLearning import QLearningAgentAI,LoadModel
from minesweeper.msgame import MSGame
from minesweeper.util import GameResult
import numpy as np
from tqdm import tqdm

def testGames(num_games, ai, viz=None):
    results = []

    for x in tqdm(range(num_games)):
        # game = Game(config)
        ai.resetAgentState()
        # game.init_new_game()
        # print("playing game {}".format(x))
        if viz: print("HUHUHUHUH")
        while not ai.isGameOver():
            # pdb.set_trace()
            coords = ai.next()
            # print(coords)
            result = ai.gameObject.play_move("click",*coords)
            # print(result)
            if result is None:
                continue
            # print(np.asarray(game.getGameState()))
            # pdb.set_trace()

        if result.explosion:
            pass
            # print("EXPLOOOOOOOOOSION")
        else:
            print("Game won")
            # pdb.set_trace()
        results.append(GameResult(not ai.gameObject.explosion, ai.gameObject.num_moves))
    numWins = 0
    for gameRes in results:
        if gameRes.success:
            numWins +=1

    print ("won {}games out of {}".format(numWins,num_games))

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
    phase = "test"
    gameObject = MSGame(10, 10, 12)
    dictGame = {
        'discountFactor': 0.9,
        'memorySize': 500000,
        'alphaRidge': 0.001,
        'epsilonProb': 0.2,
        'savePath': "GameAI/model.pkl",
        'gameObject' : gameObject
    }
    if phase == "train":
        gameAgent = QLearningAgentAI(**dictGame)
        # trainAi(gameAgent,int(2e7))
    else:
        gameAgent = LoadModel("GameAI/model.pkl1878")
        testGames(2000,gameAgent)
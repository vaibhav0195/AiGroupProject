from GameAI.BasicAgent import BaseAgent
from minesweeper.msgame import MSGame
from minesweeper.util import GameResult
import numpy as np
from tqdm import tqdm

def testBaseAgent(num_games,game, ai):
    results = []
    game.play_move("click",0,0)
    for x in tqdm(range(num_games)):
        # game = Game(config)
        while not game.isGameOver():
            # pdb.set_trace()
            coords = ai.nextMove()
            print(coords)
            
            #print("in game")
            if coords[1] is None:
                continue
            result = game.play_move(coords[0],coords[1],coords[2])
            print(result)
            # print(np.asarray(game.getGameState()))
            # pdb.set_trace()

        if result.explosion:
            print("EXPLOOOOOOOOOSION")
        else:
            print("Game won")
            # pdb.set_trace()
        results.append(GameResult(not game.explosion, game.num_moves))
    return results


if __name__ == '__main__':
    numWin = 0
    maxWin = 0
    for j in range(10):
        numWin = 0
        for i in range(200):
            gameObject = MSGame(10, 10, 12)
            gameAgent = BaseAgent(gameObject)
            gameAgent.nextMove()
            if(gameObject.game_status == 1):
                numWin = numWin +1
        if(maxWin < numWin):
            maxWin = numWin
    print(maxWin)
    #testBaseAgent(10,gameObject,gameAgent)
    # testGames(1000,gameObject,gameAgent)
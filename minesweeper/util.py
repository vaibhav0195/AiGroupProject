class MoveResult(object):
    def __init__(self, explosion, new_squares=[],reward=0):
        self.explosion = explosion
        self.new_squares = new_squares
        self.reward = reward

    def __str__(self):
        return "{}:{}".format(self.explosion,self.reward)

    def __eq__(self, other):
        if self.explosion != other.explosion:
            return False
        return set(self.new_squares) == set(other.new_squares)

class GameResult(object):
    def __init__(self, success, num_moves):
        self.success = success
        self.num_moves = num_moves
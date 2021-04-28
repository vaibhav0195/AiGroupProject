from minesweeper.msgame import MSGame
import random
import copy
from enum import Enum, auto

class Variable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.constraints = set()
    
    def add_constraint(self, x, y):
        self.constraints.add((x, y))

class Constraint:
    def __init__(self, x, y, sum):
        self.x = x
        self.y = y
        self.variables = set()
        self.sum = sum
        
        if sum < 0:
            raise Exception("Constraint sum can not be less than 0")
    
    def add_variable(self, x, y):
        self.variables.add((x, y))        

class ConstraintGraph:
    def __init__(self, board):
        self.constraints = {}
        self.variables = {}
        self.board = board
    
    def create_constraint_graph(self):
        # Get board shape
        height, width = self.board.shape
        
        # Iterate board and register constraints
        for x in range(height):
            for y in range(width):
                # Check if it is a constraint
                if 0 < self.board[x, y] < 9:
                    # Register constraint
                    self.register_constraint(x, y)
    
    def register_constraint(self, x, y):
        # Find unsolved constraint variables
        constraint_variables, flagged_mines = self.find_constraint_variables(x, y)
        # Check if there is any
        if constraint_variables:
            # Create constraint
            new_constraint = Constraint(x, y, self.board[x, y] - flagged_mines)
            self.constraints[(x, y)] = new_constraint
            # Register variables
            for variable_position in constraint_variables:
                # Get or create
                variable = self.variables.setdefault(variable_position, Variable(*variable_position))
                # if variable_position in self.variables.keys():
                    # variable = self.variables[variable_position]
                # else:
                    # variable = Variable(*variable_position)
                    # self.variables[variable_position] = variable
                
                # Add constraint and variable
                variable.add_constraint(x, y)
                new_constraint.add_variable(*variable_position)
    
    def find_constraint_variables(self, x, y):
        position_list = (
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1))
        
        max_x, max_y = self.board.shape
        
        constraint_variables = []
        flagged_mines = 0
        
        # Get neighboring undiscovered variables
        for vx, vy in position_list:
            if vx < 0 or vy < 0 or vx >= max_x or vy >= max_y:
                continue
            else:
                if self.board[vx, vy] == 11:
                    constraint_variables.append((vx, vy))
                elif self.board[vx, vy] == 9:
                    flagged_mines += 1
        
        return constraint_variables, flagged_mines
    
    def solve_trivial_constraints(self):
        solved_constraints = []
        for constraint in self.constraints.values():
            if constraint.sum == 0:
                for variable in constraint.variables:
                    solved_constraints.append(("click", variable))
            elif constraint.sum == len(constraint.variables):
                for variable in constraint.variables:
                    solved_constraints.append(("flag", variable))
        
        return solved_constraints
    
    def attempt_simplify_constraints(self):
        constraints_simplified = False
        for a in self.constraints.values():
            for b in self.constraints.values():
                if not a is b:
                    if a.variables > b.variables:
                        a.variables -= b.variables
                        a.sum -= b.sum
                        constraints_simplified = True
        
        return constraints_simplified
        
    def search_solution(self):
        def recursive_search(possible_solutions, variable_values, current_variables, current_constraints):
            # Check if all the variables have been solved
            if not current_variables:
                possible_solutions.append(variable_values)
                return
            
            # Else pick a variable and check its possible values
            variable = min(current_variables.values(), key=lambda x: len(x.constraints))
            values = tuple()
        
            # Test for 1
            for constraint in variable.constraints:
                if current_constraints[constraint].sum == 0:
                    break
            else:
                values += (1,)
                
            # Test for 0
            for constraint in variable.constraints:
                if len(current_constraints[constraint].variables) == current_constraints[constraint].sum:
                    break
            else:
                values += (0,)
                
            # Then, if there are possible values, probe them
            
            if values:               
                # Remove current variable
                del current_variables[(variable.x, variable.y)]
                for constraint in variable.constraints:
                    current_constraints[constraint].variables.remove((variable.x, variable.y))
                
                if 0 in values:
                    current_value = (((variable.x, variable.y), 0),)
                    recursive_search(possible_solutions, variable_values + current_value, current_variables, current_constraints)
                
                if 1 in values:
                    current_value = (((variable.x, variable.y), 1),)
                    for constraint in variable.constraints:
                        current_constraints[constraint].sum -= 1
                    recursive_search(possible_solutions, variable_values + current_value, current_variables, current_constraints)
                    # Restore constraints
                    for constraint in variable.constraints:
                        current_constraints[constraint].sum += 1
                
                # Restore variable
                current_variables[(variable.x, variable.y)] = variable
                for constraint in variable.constraints:
                    current_constraints[constraint].variables.add((variable.x, variable.y))
        # END recursive_search
        
        variable_values = tuple()
        current_variables = self.variables
        current_constraints = self.constraints
        possible_solutions = []
        
        # Perform recursive search
        recursive_search(possible_solutions, variable_values, current_variables, current_constraints)
        
        # Count mines and return those variables whose value is the same in all the configurations
        # If no value found, guess the variable with less chances of being a mine
        mine_counter = {}
        for configuration in possible_solutions:
            for key, value in configuration:
                mine_counter[key] = mine_counter.setdefault(key, 0) + value
        
        values_found = [("flag" if v else "click", k) for k, v in mine_counter.items() if v == len(possible_solutions) or v == 0]
        
        if values_found:
            return True, values_found
        else:
            return False, [("click", min(mine_counter))]

def apply_actions_to_game(game, actions):
    for action in actions:
        type, (x, y) = action
        game.play_move(type, y, x)

class GameResult(Enum):
    VICTORY = auto()
    VICTORY_W_RANDOM = auto()
    LOSE = auto()
    LOSE_ON_START = auto()
    LOSE_ON_RANDOM = auto()

def solve_minesweeper_csp(ms):
    had_to_use_random = False

    # Loop while game is still going
    while ms.game_status == 2:
        # Generate constraint graph
        csp = ConstraintGraph(ms.get_info_map())
        csp.create_constraint_graph()
        
        # Check if it is the first move
        if len(csp.constraints) == 0:
            # Random initial move
            x = random.choice(range(ms.board_height))
            y = random.choice(range(ms.board_width))
            ms.play_move("click", y, x)
            if ms.game_status == 0:
                # Lost on first move
                return GameResult.LOSE_ON_START
            continue
        
        # Attempt to solve trivial constraints
        trivial_constraints = csp.solve_trivial_constraints()
        if trivial_constraints:
            apply_actions_to_game(ms, trivial_constraints)
            continue
        
        # Attempt to simplify and then solve trivial constraints
        while True:
            if not csp.attempt_simplify_constraints():
                break
        trivial_constraints = csp.solve_trivial_constraints()
        if trivial_constraints:
            apply_actions_to_game(ms, trivial_constraints)
            continue
        
        # Search for possible solutions
        csp = ConstraintGraph(ms.get_info_map()) # Regenerate constraint graph
        csp.create_constraint_graph()
        values_found, search_solutions = csp.search_solution()
        if not values_found:
            had_to_use_random = True
            apply_actions_to_game(ms, search_solutions)
            if ms.game_status == 0:
                # Lost on random choice
                return GameResult.LOSE_ON_RANDOM
        apply_actions_to_game(ms, search_solutions)
    if ms.game_status == 1:
        print("Board solved")
        return GameResult.VICTORY if not had_to_use_random else GameResult.VICTORY_W_RANDOM
    else:
        print("Board failed")
        return GameResult.LOSE

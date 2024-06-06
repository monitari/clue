import random

class Dice():
    def __init__(self, num_side, condition):
        self.num_side = num_side # number of sides
        self.condition = condition # condition for the dice
    def roll(self): # roll the dice
        score = random.randrange(self.num_side) + 1 # 1 ~ num_side
        if not self.condition(score): # if condition is not satisfied,
            raise Exception("Condition not satisfied") # raise exception
        return score # return score

execute_count = 0 # count of executions
even_dice = Dice(6, lambda x: True) # all numbers dice
total_score = 0 # total score
win_count = 0 # count of wins
num_iterations = 1000000 # number of iterations
all_2 = 0 # count of all 2

for _ in range(num_iterations):
    try: # try to roll the dice
        a = even_dice.roll() # roll the dice
        b = even_dice.roll() # roll the dice
        c = even_dice.roll() # roll the dice
        total_score = a + b + c # calculate total score
        if a == 2 and b == 2 and c == 2:
            all_2 += 1 # increment all 2 count
        if total_score == 6: # if total score is 6
            win_count += 1 # increment win count
    except: # if exception is raised
        total_score = 0 # reset total score
        execute_count += 1 # increment execute count

print("Win count:", win_count, "all 2 count:", all_2, "total iterations:", num_iterations)
probability = all_2 / win_count * 100 # calculate probability
print("Probability of first line being 'Win!' when total score is 6:", probability if win_count > 0 else 0, "%")
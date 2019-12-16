import snake
import random
import numpy as np
import pickle
from Arena import Arena
import argparse
from input import *
import matplotlib.pyplot as plt
import time


# used to show the progress bar
def progress_bar(curr, total, length):
    frac = curr/total
    filled_bar = round(frac*length)
    print('\r', '#'*filled_bar + '-'*(length - filled_bar), '[{:>7.2%}]'.format(frac), end='')


# to run all the snakes of a population
def run(snakes, arena):
    i = 1
    # count1 = [0 for _ in range(300)]
    # count2 = [0 for _ in range(300)]
    win1 = 0
    win2 = 0
    snakes_killed = 0
    # making new seed for each generation so that fittest of one generation may not be fittest in another
    # and we get a global optimum
    env_seed = random.random()
    for i in range(population_size):
        s1 = snakes[0][i];
        s2 = snakes[1][i];
        start_time = time.time()
        # no need to check loop because the length of snake grow automatically
        # checkloop = False
        progress_bar(i, population_size, 30)
        random.seed(env_seed)  # so that each snake of the population faces the same environment
        nextFood = arena.newFood(s1.list + s2.list)
        s1.Brain.setNextFood(nextFood)
        s2.Brain.setNextFood(nextFood)
        while s1.isAlive() and s2.isAlive():
            result = s1.Brain.decision_from_nn(s1.head_x, s1.head_y, s1.list, s2.list, s1.direction)
            alive =  s1.move(result, s2)
            if not alive:
                # s1.list = []
                s1.score -= s1.Brain.giveSecondChance
                s2.score -= s2.Brain.giveSecondChance
                s1.score *= 0.7;
                break
            # # to check if continuous loop formed by snake and then killing that snake
            # if s1.steps_taken > 250:
            #     if not checkloop:
            #         checkloop = True
            #         any_point_of_loop = (s1.head_x, s1.head_y)
            #         times = 0
            #     elif (s1.head_x, s1.head_y) == any_point_of_loop:
            #         times += 1
            #     if times > 2:
            #         s1.crash_wall = True
            #         s1.crash_body = True
            #         snakes_killed += 1
            # else:
            #     checkloop = False
            # # forcefully killing if loop not caught
            # if time.time() - start_time > 0.5:
            #     s1.crash_wall = True
            #     s1.crash_body = True
            #     snakes_killed += 1
            # if food eaten by snake
            if (s1.head_x, s1.head_y) == arena.food:
                s1.steps_taken = 0
                s1.toIncrease = True
                s1.score += 10
                start_time = time.time()
                nextFood = arena.newFood(s1.list + s2.list)
                s1.Brain.setNextFood(nextFood)
                s2.Brain.setNextFood(nextFood) 

            # s2's turn
            result = s2.Brain.decision_from_nn(s2.head_x, s2.head_y, s2.list, s1.list, s2.direction)
            alive =  s2.move(result, s1)
            if not alive:
                # s2.list = []
                s1.score -= s1.Brain.giveSecondChance
                s2.score -= s2.Brain.giveSecondChance
                s2.score *= 0.7
                break
            # # to check if continuous loop formed by snake and then killing that snake
            # if s2.steps_taken > 250:
            #     if not checkloop:
            #         checkloop = True
            #         any_point_of_loop = (s2.head_x, s2.head_y)
            #         times = 0
            #     elif (s2.head_x, s2.head_y) == any_point_of_loop:
            #         times += 1
            #     if times > 2:
            #         s2.crash_wall = True
            #         s2.crash_body = True
            #         snakes_killed += 1
            # else:
            #     checkloop = False
            # # forcefully killing if loop not caught
            # if time.time() - start_time > 0.5:
            #     s2.crash_wall = True
            #     s2.crash_body = True
            #     snakes_killed += 1
            # if food eaten by snake
            if (s2.head_x, s2.head_y) == arena.food:
                s2.steps_taken = 0
                s2.toIncrease = True
                s2.score += 10
                start_time = time.time()
                nextFood = arena.newFood(s2.list + s1.list)
                s1.Brain.setNextFood(nextFood)
                s2.Brain.setNextFood(nextFood) 
        random.seed()
        # count1[len(s1.list)] += 1
        # count2[len(s1.list)] += 1
        if s1.score>s2.score:
            win1 += 1
        else:
            win2 += 1
        # i += 1
    # print('\nsnakes distribution with index as score : Snake1: ',count1[0:15],' Snake2: ', count2[0:15], 'snakes killed', snakes_killed)
    print('\nSnake[1] wins', win1, 'times. Snake[2] wins', win2, 'times.')


# to print the top five snakes info
def print_top_5(five_snakes):
    i = 0
    for snake in five_snakes:
        i += 1
        print('snake :', i, ', score :', snake.score, ', length :', len(snake.list), end='\t')
        if snake.crash_body and snake.crash_wall:
            print('crashed repetition')
        elif snake.crash_wall and not snake.crash_body:
            print('crashed wall')
        elif snake.crash_snake:
            print('crashed snake')
        else:
            print('crashed body')


# to save the snake
def save_top_snakes(snakes,  filename):
    f = open(filename, 'wb')
    pickle.dump(snakes, f)
    f.close()


# used to create the popultion for next generation
def create_new_population(snakes):
    # choosing the top x% of the population and breeding them to create new population
    # the top x% and bottom y% is also included in new population
    parents = [[],[]]
    top_old_parents = int(population_size * per_of_best_old_pop / 100)
    bottom_old_parents = int(population_size * per_of_worst_old_pop / 100)
    for i in range(top_old_parents):
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i * 2].Brain.weights
        parent.Brain.bases = snakes[i * 2].Brain.bases
        parents[0].append(parent)
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i*2+1].Brain.weights
        parent.Brain.bases = snakes[i*2+1].Brain.bases
        parents[1].append(parent)
    for i in range(population_size - 1, population_size - bottom_old_parents - 1, -1):
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i*2].Brain.weights
        parent.Brain.bases = snakes[i*2].Brain.bases
        parents[0].append(parent)
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i*2+1].Brain.weights
        parent.Brain.bases = snakes[i*2+1].Brain.bases
        parents[1].append(parent)
    # generating children of top x% and bottom y%
    children = generate_children(parents[0], population_size - (top_old_parents + bottom_old_parents))
    # mutating children
    children = mutate_children(children)
    # joining parents and children to make new population
    parents[0].extend(children)
    # generating children of top x% and bottom y%
    children = generate_children(parents[1], population_size - (top_old_parents + bottom_old_parents))
    # mutating children
    children = mutate_children(children)
    # joining parents and children to make new population
    parents[1].extend(children)
    return parents


# mutating the children
def mutate_children(children):
    for child in children:
        for weight in child.Brain.weights:
            for ele in range(int(weight.shape[0]*weight.shape[1]*mutation_percent/100)):
                row = random.randint(0, weight.shape[0]-1)
                col = random.randint(0, weight.shape[1]-1)
                weight[row, col] += random.uniform(-mutation_intensity, mutation_intensity)
    return children


# generating children based on the parents passed
def generate_children(parents, no_of_children):
    all_children = []
    l = len(parents)
    for count in range(no_of_children):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = snake.snake(width, height, brainLayer, block_length)
        for i in range(len(parent1.Brain.weights)):
            for j in range(parent1.Brain.weights[i].shape[0]):
                for k in range(parent1.Brain.weights[i].shape[1]):
                    child.Brain.weights[i][j, k] = random.choice(
                        [parent1.Brain.weights[i][j, k], parent2.Brain.weights[i][j, k]])
            for j in range(parent1.Brain.bases[i].shape[1]):
                child.Brain.bases[i][0, j] = random.choice(
                    [parent1.Brain.bases[i][0, j], parent2.Brain.bases[i][0, j]])
        all_children.append(child)
    return all_children


def main():
    # command line argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--output', required=True, help='relative path to save the snakes')
    args = vars(ap.parse_args())
    snakes = [[snake.snake(width, height, brainLayer, block_length) for _ in range(population_size)],
            [snake.snake(width, height, brainLayer, block_length, head_x=width-30, head_y=height-30) for _ in range(population_size)]]
    arena = Arena(width, height, block_length)
    top_snakes = []
    top_5_score = []
    for i in range(no_of_generations):
        print('generation : ', i+1, ',', end='\n')
        run(snakes, arena)
        # sorting the population wrt length of snake and steps taken
        mergedSnakes = snakes[0]+snakes[1]
        mergedSnakes.sort(key=lambda x: (x.score), reverse=True)
        print_top_5(mergedSnakes[0:5]) 
        sum_5 = 0
        for s in mergedSnakes[0:5]:
            sum_5 += s.score
        top_5_score.append(sum_5/5.0)
        # generalising the whole population
        print('saving the snake')
        top_snakes.append(mergedSnakes[0])
        # saving top snakes list as pickle
        save_top_snakes(top_snakes, args['output'])
        snakes = create_new_population(mergedSnakes)
    plt.plot(top_5_score)
    plt.show()


if __name__ == "__main__":
    main()

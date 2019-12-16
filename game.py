import pygame
import colors as col
import pickle
from Arena import *
from snake import *
import time
import argparse
from input import *

if __name__ == "__main__":
    # command line argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True, help='relative path of the saved pickle file')
    ap.add_argument('-s', '--start', type=int, help='relative start of the saved snakes')
    ap.add_argument('-v', '--vsAI', action="store_true", help='Play with AI')
    ap.add_argument('-f', '--fool', action="store_true", help='Use baseline opponent')
    ap.add_argument('-t', '--test', action="store_true", help='Test mode')
    args = vars(ap.parse_args())
    # loading the saved snakes
    if args['test']:
        file = open(args['input'], 'rb')
        snakes = pickle.load(file)
        generation = 0
        start = 0;
        if args['start'] is not None:
            start = args['start']
            generation += start
        file.close()
        # pygame initialization
        pygame.init()
        pygame.font.init()
        myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
        screen = pygame.display.set_mode((width, height))
        # seed generated so that each snake sees same set of foods for performance comparison
        arena = Arena(width, height, block_length)

        win1 = 0
        win2 = 0 
        for i in range(100):
            text = 'Generation : '+('fool' if args['fool'] else str(generation))+' vs '+str(generation+1)
            pygame.display.set_caption(text)
            seed = random.random()
            print('---- Snake[1]: Generation:', 'fool' if args['fool'] else generation,' vs  Snake[2]: Generation:', generation+1,'----')
            t_snake = snake(width, height, brainLayer, block_length,
                            random_weights=False, random_bases=False)
            t_snake.Brain.weights = snakes[start].Brain.weights
            t_snake.Brain.bases = snakes[start].Brain.bases
            t_snake2 = snake(width, height, brainLayer, block_length, head_x=width-30, head_y=height-30,
                            random_weights=False, random_bases=False)
            t_snake2.Brain.weights = snakes[start].Brain.weights
            t_snake2.Brain.bases = snakes[start].Brain.bases
            random.seed(seed)
            nextFood = arena.newFood(t_snake.list)
            t_snake.Brain.setNextFood(nextFood)
            t_snake2.Brain.setNextFood(nextFood)
            screen = arena.setup(screen, col.bg, col.gray)
            screen = arena.drawFood(screen, col.food)
            screen = t_snake.draw(screen, col.snake1)
            screen = t_snake2.draw(screen, col.snake2)
            pygame.display.update()
            # checkloop = False
            while t_snake.isAlive() and t_snake2.isAlive():
                # checking for key presses and close button presses and pause-continue funcionality
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pressed = True
                        while pressed:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                                    pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        t_snake.crash_wall = True
                        t_snake.crash_body = True
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                # getting result from the neural network
                if not args['fool']:
                    result = t_snake.Brain.decision_from_nn(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake2.list, t_snake.direction)
                else:
                    result = t_snake.Brain.decision_from_fool(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake2.list, t_snake.direction)
                # moving the snake
                # print(result)
                alive = t_snake.move(result, t_snake2)
                if not alive:
                    t_snake.score *= 0.7
                    if t_snake.crash_wall and t_snake.crash_body:
                        print('killed.  Score : Snake[1]', t_snake.score,':',t_snake2.score,'Snake[2]')
                    elif t_snake.crash_wall and not t_snake.crash_body:
                        print('Snake[1] crashed on wall,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    elif t_snake.crash_snake:
                        print('Snake[1] crashed on Snake[1],', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    else:
                        print('Snake[1] crashed on body,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    time.sleep(2)
                    break
                if (t_snake.head_x, t_snake.head_y) == arena.food:
                    t_snake.steps_taken = 0
                    t_snake.toIncrease = True
                    t_snake.score += 10
                    nextFood =  arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                    t_snake2.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()

                # getting result from the neural network
                result = t_snake2.Brain.decision_from_nn(
                    t_snake2.head_x, t_snake2.head_y, t_snake2.list, t_snake.list, t_snake2.direction)
                # moving the snake
                # print(result)
                alive = t_snake2.move(result, t_snake)
                if not alive:
                    t_snake2.score *= 0.7
                    if t_snake2.crash_wall and t_snake2.crash_body:
                        print('killed.  Score : Snake[1]', t_snake.score,':',t_snake2.score,'Snake[2]')
                    elif t_snake2.crash_wall and not t_snake2.crash_body:
                        print('Snake[2] crashed on wall,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    elif t_snake2.crash_snake:
                        print('Snake[2] crashed on Snake[1],', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    else:
                        print('Snake[2] crashed on body,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    time.sleep(2)
                    break
                if (t_snake2.head_x, t_snake2.head_y) == arena.food:
                    t_snake2.steps_taken = 0
                    t_snake2.toIncrease = True
                    t_snake2.score += 10
                    nextFood =  arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                    t_snake2.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()

            if t_snake.score<t_snake2.score:
                win2+=1
            else:
                win1+=1
        print("Baseline wins", win1, "AI wins", win2)
        pygame.quit()
        quit()
    elif not args['vsAI']:
        file = open(args['input'], 'rb')
        snakes = pickle.load(file)
        generation = 0
        if args['start'] is not None:
            start = args['start']
            snakes = snakes[start:]
            generation += start
        file.close()
        # pygame initialization
        pygame.init()
        pygame.font.init()
        myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
        screen = pygame.display.set_mode((width, height))
        # seed generated so that each snake sees same set of foods for performance comparison
        seed = random.random()
        arena = Arena(width, height, block_length)

        for i in range(len(snakes)-1):
            text = 'Generation : '+('fool' if args['fool'] else str(generation))+' vs '+str(generation+1)
            pygame.display.set_caption(text)
            print('---- Snake[1]: Generation:', 'fool' if args['fool'] else generation,' vs  Snake[2]: Generation:', generation+1,'----')
            t_snake = snake(width, height, brainLayer, block_length,
                            random_weights=False, random_bases=False)
            t_snake.Brain.weights = snakes[i].Brain.weights
            t_snake.Brain.bases = snakes[i].Brain.bases
            t_snake2 = snake(width, height, brainLayer, block_length, head_x=width-30, head_y=height-30,
                            random_weights=False, random_bases=False)
            t_snake2.Brain.weights = snakes[i+1].Brain.weights
            t_snake2.Brain.bases = snakes[i+1].Brain.bases
            random.seed(seed)
            nextFood = arena.newFood(t_snake.list)
            t_snake.Brain.setNextFood(nextFood)
            t_snake2.Brain.setNextFood(nextFood)
            screen = arena.setup(screen, col.bg, col.gray)
            screen = arena.drawFood(screen, col.food)
            screen = t_snake.draw(screen, col.snake1)
            screen = t_snake2.draw(screen, col.snake2)
            pygame.display.update()
            # checkloop = False
            while t_snake.isAlive() and t_snake2.isAlive():
                # checking for key presses and close button presses and pause-continue funcionality
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pressed = True
                        while pressed:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                                    pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        t_snake.crash_wall = True
                        t_snake.crash_body = True
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                # getting result from the neural network
                if not args['fool']:
                    result = t_snake.Brain.decision_from_nn(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake2.list, t_snake.direction)
                else:
                    result = t_snake.Brain.decision_from_fool(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake2.list, t_snake.direction)
                # moving the snake
                # print(result)
                alive = t_snake.move(result, t_snake2)
                # # checking for loops made by snake
                # if t_snake.steps_taken > (len(t_snake.list)/5*100):
                #     if not checkloop:
                #         checkloop = True
                #         any_point = (t_snake.head_x, t_snake.head_y)
                #         times = 0
                #     if (t_snake.head_x, t_snake.head_y) == any_point:
                #         times += 1
                #     if times > 4:
                #         t_snake.crash_wall = True
                #         t_snake.crash_body = True
                #         alive = False
                # else:
                #     checkloop = False
                if not alive:
                    t_snake.score *= 0.7
                    if t_snake.crash_wall and t_snake.crash_body:
                        print('killed.  Score : Snake[1]', t_snake.score,':',t_snake2.score,'Snake[2]')
                    elif t_snake.crash_wall and not t_snake.crash_body:
                        print('Snake[1] crashed on wall,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    elif t_snake.crash_snake:
                        print('Snake[1] crashed on Snake[1],', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    else:
                        print('Snake[1] crashed on body,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    time.sleep(2)
                    break
                if (t_snake.head_x, t_snake.head_y) == arena.food:
                    t_snake.steps_taken = 0
                    t_snake.toIncrease = True
                    t_snake.score += 10
                    nextFood =  arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                    t_snake2.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()

                # getting result from the neural network
                result = t_snake2.Brain.decision_from_nn(
                    t_snake2.head_x, t_snake2.head_y, t_snake2.list, t_snake.list, t_snake2.direction)
                # moving the snake
                # print(result)
                alive = t_snake2.move(result, t_snake)
                # # checking for loops made by snake
                # if t_snake2.steps_taken > (len(t_snake2.list)/5*100):
                #     if not checkloop:
                #         checkloop = True
                #         any_point = (t_snake2.head_x, t_snake2.head_y)
                #         times = 0
                #     if (t_snake2.head_x, t_snake2.head_y) == any_point:
                #         times += 1
                #     if times > 4:
                #         t_snake2.crash_wall = True
                #         t_snake2.crash_body = True
                #         alive = False
                # else:
                #     checkloop = False
                if not alive:
                    t_snake2.score *= 0.7
                    if t_snake2.crash_wall and t_snake2.crash_body:
                        print('killed.  Score : Snake[1]', t_snake.score,':',t_snake2.score,'Snake[2]')
                    elif t_snake2.crash_wall and not t_snake2.crash_body:
                        print('Snake[2] crashed on wall,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    elif t_snake2.crash_snake:
                        print('Snake[2] crashed on Snake[1],', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    else:
                        print('Snake[2] crashed on body,', 'Score : Snake[1]', int(t_snake.score),':',int(t_snake2.score),'Snake[2]')
                    time.sleep(2)
                    break
                if (t_snake2.head_x, t_snake2.head_y) == arena.food:
                    t_snake2.steps_taken = 0
                    t_snake2.toIncrease = True
                    t_snake2.score += 10
                    nextFood =  arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                    t_snake2.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()

                time.sleep(0.03)
            generation += 1
        pygame.quit()
        quit()
    else:
        file = open(args['input'], 'rb')
        snakes = pickle.load(file)
        generation = 0
        if args['start'] is not None:
            start = args['start']
            generation += start
        file.close()
        # pygame initialization
        pygame.init()
        pygame.font.init()
        myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
        screen = pygame.display.set_mode((width, height))
        life = 1
        arena = Arena(width, height, block_length)

        while True:
            text = 'YOU  vs  Generation: '+str(generation+1)
            pygame.display.set_caption(text)
            seed = random.random()
            t_snake = snake(width, height, brainLayer, block_length, head_x=width-30, head_y=height-30,
                            random_weights=False, random_bases=False)
            t_snake.Brain.weights = snakes[generation].Brain.weights
            t_snake.Brain.bases = snakes[generation].Brain.bases
            t_snake2 = snake(width, height, brainLayer, block_length,
                            random_weights=False, random_bases=False)
            random.seed(seed)
            nextFood = arena.newFood(t_snake.list + t_snake2.list)
            t_snake.Brain.setNextFood(nextFood)
            screen = arena.setup(screen, col.bg, col.gray)
            screen = arena.drawFood(screen, col.food)
            screen = t_snake.draw(screen, col.snake1)
            screen = t_snake2.draw(screen, col.snake2)
            pygame.display.update()
            checkloop = False
            while t_snake.isAlive() and t_snake2.isAlive():
                # getting result from the neural network
                result = t_snake.Brain.decision_from_nn(
                    t_snake.head_x, t_snake.head_y, t_snake.list, t_snake2.list, t_snake.direction)
                # moving the snake
                # print(result)
                alive = t_snake.move(result, t_snake2)
                # checking for loops made by snake
                if t_snake.steps_taken > (len(t_snake.list)/5*100):
                    if not checkloop:
                        checkloop = True
                        any_point = (t_snake.head_x, t_snake.head_y)
                        times = 0
                    if (t_snake.head_x, t_snake.head_y) == any_point:
                        times += 1
                    if times > 4:
                        t_snake.crash_wall = True
                        t_snake.crash_body = True
                        alive = False
                else:
                    checkloop = False
                if not alive:
                    t_snake.score *= 0.7
                    if t_snake.crash_wall and t_snake.crash_body:
                        print('killed.  Score : YOU', t_snake2.score,':',t_snake.score,'AI')
                    elif t_snake.crash_wall and not t_snake.crash_body:
                        print('AI crashed on wall,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    elif t_snake.crash_snake:
                        print('AI crashed on YOU,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    else:
                        print('AI crashed on body,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    time.sleep(2)
                    break
                if (t_snake.head_x, t_snake.head_y) == arena.food:
                    t_snake.score += 10
                    t_snake.steps_taken = 0
                    t_snake.toIncrease = True
                    nextFood =  arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()
                pygame.display.update()


                # checking for key presses and close button presses and pause-continue funcionality
                # checking for key presses and close button presses and pause-continue funcionality
                result = 1
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pressed = True
                        while pressed:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                                    pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        t_snake.crash_wall = True
                        t_snake.crash_body = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        result = t_snake2.dirToRes('north');
                        pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        result = t_snake2.dirToRes('south');
                        pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        result = t_snake2.dirToRes('west');
                        pressed = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        result = t_snake2.dirToRes('east');
                        pressed = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()


                alive = t_snake2.move(result, t_snake)
                # checking for loops made by snake
                if t_snake2.steps_taken > (len(t_snake2.list)/5*100):
                    if not checkloop:
                        checkloop = True
                        any_point = (t_snake2.head_x, t_snake2.head_y)
                        times = 0
                    if (t_snake2.head_x, t_snake2.head_y) == any_point:
                        times += 1
                    if times > 4:
                        t_snake2.crash_wall = True
                        t_snake2.crash_body = True
                        alive = False
                else:
                    checkloop = False
                if not alive:
                    t_snake2.score *= 0.7
                    if t_snake2.crash_wall and t_snake2.crash_body:
                        print('killed.  Score : YOU', t_snake2.score,':',t_snake.score,'AI')
                    elif t_snake2.crash_wall and not t_snake2.crash_body:
                        print('YOU crashed on wall,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    elif t_snake2.crash_snake:
                        print('YOU crashed on AI,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    else:
                        print('YOU crashed on body,', 'Score : YOU', int(t_snake2.score),':',int(t_snake.score),'AI')
                    time.sleep(2)
                    break
                if (t_snake2.head_x, t_snake2.head_y) == arena.food:
                    t_snake2.score += 10
                    t_snake2.steps_taken = 0
                    t_snake2.toIncrease = True
                    nextFood = arena.newFood(t_snake.list + t_snake2.list)
                    t_snake.Brain.setNextFood(nextFood)
                screen = arena.setup(screen, col.bg, col.gray)
                screen = arena.drawFood(screen, col.food)
                screen = t_snake.draw(screen, col.snake1)
                screen = t_snake2.draw(screen, col.snake2)
                pygame.display.update()
                pygame.display.update()
                time.sleep(0.1)
            life += 1
        pygame.quit()
        quit()

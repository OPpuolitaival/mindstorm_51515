from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

start_again = True

def wite_situation(hub, worm, apple):
    for x in range(0,5):
        for y in range(0,5):
            if (x,y) in worm:
                hub.light_matrix.set_pixel(x, y, 100)
            elif (x,y) == apple:
                hub.light_matrix.set_pixel(x, y, 90)
            else:
                hub.light_matrix.set_pixel(x, y, 0)

def get_direction(hub, direction):
    if hub.left_button.was_pressed():
        return (direction-1) % 4
    if hub.right_button.was_pressed():
        return (direction+1) % 4
    return direction

def move_worm(hub, worm, direction, apple):
    worm_head = worm[-1]
    direction = get_direction(hub, direction)
    next_step = -1
    if direction == UP:
        next_step = (worm_head[0], worm_head[1]-1)
    if direction == DOWN:
        next_step = (worm_head[0], worm_head[1]+1)
    if direction == LEFT:
        next_step = (worm_head[0]-1, worm_head[1])
    if direction == RIGHT:
        next_step = (worm_head[0]+1, worm_head[1])
    if min(next_step) < 0 or max(next_step) > 5 or next_step in worm:
        return None, None, None
    if next_step == apple:
        apple = create_apple(worm)
    else:
        worm = worm[1:]
    worm.append(next_step)
    return worm, direction, apple


def create_apple(worm):
    while True:
        x = random.randint(0,4)
        y = random.randint(0,4)
        if (x,y) not in worm:
            return (x,y)

# The game loop
hub = MSHub()


while start_again == True:
    hub.status_light.on('green')
    direction = UP
    # (x,y) [last, first]
    worm = [(2,4), (2,3), (2,2)]

    apple = create_apple(worm)
    while True:
        wite_situation(hub, worm, apple)
        wait_for_seconds(0.5)
        worm, direction, apple = move_worm(hub, worm, direction, apple)
        if worm is None:
            break

    hub.status_light.on('red')

    # Waiting if user want to play again
    start_again = False
    index = 0
    while index < 30:
        if hub.left_button.was_pressed() or hub.right_button.was_pressed():
            start_again = True
            break
        index += 1
        wait_for_seconds(0.5)

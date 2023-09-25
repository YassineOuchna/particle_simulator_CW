import pygame
import random
import pymunk
import matplotlib.pyplot as plt
import numpy as np
pygame.init()
height = 500
width = 2100
num_of_balls = 10000
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
Fps = 120

particle_size = 1
space = pymunk.Space()
pusher_run_time = 100
pusher_start_time = 100
# uninfected space 1 to num_of_balls
# infected space num_of_balls+1 to 2*num_of_balls
# recover space 2*num_of_balls+1 to 3*num_of_balls


class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        # 100 in velocity means 100 frames per sec
        # random float nunber
        self.body.velocity = random.uniform(-100,
                                            100), random.uniform(-500, 500)
        self.shape = pymunk.Circle(self.body, particle_size)
        self.shape.density = 1
        self.shape.elasticity = 1

        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position

        pygame.draw.circle(display, (255, 255, 255),
                           (int(x), int(y)), particle_size)


class Satistic_Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # I don't quite understand it here
        self.shape = pymunk.Segment(self.body, p1, p2, 20)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)


class Kinematic_Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 15)
        self.shape.body.velocity = (0, 0)
        self.shape.elasticity = 1
        self.time = 0
        space.add(self.shape, self.body)

    def stop(self):
        self.time = self.time+1
        if self.time < pusher_start_time:
            self.shape.body.velocity = (0, 0)
        elif self.time > pusher_run_time+pusher_start_time:
            self.shape.body.velocity = (0, 0)
        else:
            self.shape.body.velocity = (500, 0)


def game(width, height):
    balls = [Ball(random.randint(0, width), random.randint(0, height))
             for i in range(num_of_balls)]
    # collision handler

    pushers = [Kinematic_Wall((0, 0), (0, height))]

    walls = [Satistic_Wall((0, 0), (width, 0)),
             Satistic_Wall((width, 0), (width, height)),
             Satistic_Wall((0, height), (width, height))
             ]

    run = True

    while run:  # one while loop equals one frame

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False  # when click x make sure it close
                break
        display.fill((0, 0, 0))

        for ball in balls:
            ball.draw()
        pushers[0].stop()

        clock.tick(Fps)
        pygame.display.update()
        space.step(1/Fps)
    pygame.quit()


if __name__ == '__main__':
    game(width, height)

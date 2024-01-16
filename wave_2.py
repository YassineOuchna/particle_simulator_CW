import pygame
import pymunk
import random
import time

'''--- INITIALIZING ENVIRONEMENT & GLOBAL CONSTANTS ---'''

pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = int(
    0.9*pygame.display.Info().current_w), int(0.9*pygame.display.Info().current_h)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
w_slider = int(0.25*WIDTH)
h_slider = int(0.035*HEIGHT)


'''--- GUI ELEMENTS ---'''


class Slider():
    def __init__(self, title, min, max, x, y):
        self.title = title
        self.x = x            # Position of the topleft of the slider
        self.y = y
        self.min = min
        self.max = max
        self.cy = y             # Position of the topleft of the slider handle
        self.cx = x
        self.value = round(100*(self.min+(self.max-self.min) *
                                (self.cx-self.x+0.1*w_slider/2)/(w_slider)))/100

    def render(self):
        box = pygame.draw.rect(screen, (134, 136, 138),
                               (self.x, self.y, w_slider, h_slider))
        # UPDATING CURSOR POSITION
        self.value = round(100*(self.min+(self.max-self.min) *
                                (self.cx-self.x+0.1*w_slider/2)/(w_slider)))/100
        cursor = pygame.draw.rect(
            screen, (202, 204, 206), (self.cx, self.cy, int(0.1*w_slider), h_slider))

        font = pygame.font.Font(None, 36)
        title = font.render(self.title, True, (255, 255, 255))
        value = font.render(str(self.value), True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.x-125, self.y+h_slider//2))
        value_rect = value.get_rect(
            center=(self.cx+0.1*w_slider//2, self.cy-h_slider//2))
        screen.blit(title, title_rect)
        screen.blit(value, value_rect)
        return cursor


l = Slider("TEST", 0, 5, WIDTH//2, HEIGHT//2)

'''--- SIMULATION ELEMENTS ---

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        # 100 in velocity means 100 frames per sec
        # random float nunber
        self.body.velocity = random.uniform(-speed_limit,
                                            speed_limit), random.uniform(-speed_limit, speed_limit)
        self.shape = pymunk.Circle(self.body, particle_size)
        self.shape.density = 1
        self.shape.elasticity = elasticity

        space.add(self.body, self.shape)

class Satistic_Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # I don't quite understand it here
        self.shape = pymunk.Segment(self.body, p1, p2, 3)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)

class Kinematic_Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 3)
        self.shape.body.velocity = (0, 0)
        self.shape.elasticity = pusher_elasticity
        self.time = 0
        space.add(self.shape, self.body)

    def stop(self):
        self.time = self.time+1
        if self.time < pusher_start_time:
            self.shape.body.velocity = (0, 0)
        elif self.time > pusher_run_time+pusher_start_time:
            self.shape.body.velocity = (0, 0)
        else:
            self.shape.body.velocity = (pusher_speed, 0)'''


if __name__ == "__main__":
    running = True
    dragging = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:     # Left mouse click
                    mx, my = pygame.mouse.get_pos()
                    if l.render().collidepoint(mx, my):
                        # l.cx = mx-0.1*w_slider//2
                        dragging = True
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    if l.cx + event.rel[0] >= l.x and l.cx + event.rel[0] <= l.x+w_slider:
                        l.cx += event.rel[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
        screen.fill((0, 0, 0))
        l.render()
        pygame.display.update()
    pygame.quit()

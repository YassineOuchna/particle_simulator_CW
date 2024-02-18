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

# Height and width of the whole slider
w_slider = int(0.25*WIDTH)
h_slider = int(0.035*HEIGHT)


'''--- GUI ELEMENTS ---'''


class Slider():
    def __init__(self, title: str, min: int, max: int, x: float, y: float, discrete=False):
        self.title = title
        self.discrete=discrete
        self.x = x            # Position of the topleft of the slider
        self.y = y
        self.min = min
        self.max = max
        self.cy = y             # Position of the topleft of the slider handle
        self.cx = x
        if self.discrete:
            self.value = round(round(100*(self.min+(self.max-self.min) *
                                (self.cx-self.x)/(0.9*w_slider)))/100)
        else:
            self.value = round(100*(self.min+(self.max-self.min) *
                                (self.cx-self.x)/(0.9*w_slider)))/100

    def render(self)-> tuple:
        box = pygame.draw.rect(screen, (134, 136, 138),
                               (self.x, self.y, w_slider, h_slider))
        # UPDATING CURSOR POSITION
        self.value = round(100*(self.min+(self.max-self.min) *
                                (self.cx-self.x)/(0.9*w_slider)))/100
        if self.discrete:
            self.value = round(self.value)
            # Length between two consecutive integer values in pixels
            partition_length = (0.9*w_slider)/(self.max-self.min)
            draw_x=self.x+(self.value-self.min)*partition_length
        cursor = pygame.draw.rect(
            screen, (202, 204, 206), (draw_x, self.cy, int(0.1*w_slider), h_slider))


        font = pygame.font.Font(None, 36)
        title = font.render(self.title, True, (255, 255, 255))
        value = font.render(str(self.value), True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.x-125, self.y+h_slider//2))
        value_rect = value.get_rect(
            center=(draw_x+0.1*w_slider//2, self.cy-h_slider//2))
        screen.blit(title, title_rect)
        screen.blit(value, value_rect)
        return cursor, box


c = Slider("TEST", 0, 5, WIDTH//2, HEIGHT//2)
d = Slider("TEST2", 0, 10, WIDTH//2, HEIGHT//2+h_slider+5, discrete=True)
sliders=[d]

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
            
            for l in sliders:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:     # Left mouse click
                        mx, my = pygame.mouse.get_pos()
                        if l.render()[0].collidepoint(mx, my):
                            dragging = True
                        elif l.render()[1].collidepoint(mx, my):
                            dragging = True
                            if mx-0.1*w_slider//2 >= l.x:
                                l.cx = min(mx-0.1*w_slider//2, l.x+0.9*w_slider)
                            elif mx-0.1*w_slider//2 <= l.x+0.9*w_slider:
                                l.cx = max(mx-0.1*w_slider//2, l.x)
                if event.type == pygame.MOUSEMOTION:
                    if dragging:
                        if l.cx + event.rel[0] >= l.x and l.cx + event.rel[0] <= l.x+0.9*w_slider:
                            l.cx += event.rel[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
        screen.fill((0, 0, 0))
        for l in sliders:
            l.render()
        pygame.display.update()
    pygame.quit()

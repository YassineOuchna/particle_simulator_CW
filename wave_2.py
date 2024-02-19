import pygame
import pymunk
import random
import time

'''--- INITIALIZING ENVIRONEMENT & GLOBAL CONSTANTS ---'''

pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = int(
    0.95*pygame.display.Info().current_w), int(0.95*pygame.display.Info().current_h)
FONT_SIZE = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Height and width of the whole slider
w_slider = int(0.2*WIDTH)
h_slider = int(0.03*HEIGHT)


'''--- GUI ELEMENTS ---'''

class Button():
    def __init__(self,title: str,x: int,y: int):
        self.title=title
        self.x=x
        self.y=y
    
    def render(self):
        # x and y denote the center of the button
        h=35
        w=250
        b = pygame.draw.rect(screen, (10, 0, 255),
                            (self.x-w//2, self.y-h//2, w, h))
        font = pygame.font.Font(None, 36)
        text = font.render(self.title, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        return b

class Slider():
    def __init__(self, title: str, min: int, max: int, x: float, y: float, discrete=True):
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
        else:
            draw_x=self.cx
        cursor = pygame.draw.rect(
            screen, (202, 204, 206), (draw_x, self.cy, int(0.1*w_slider), h_slider))


        font = pygame.font.Font(None, FONT_SIZE)
        title = font.render(self.title, True, (255, 255, 255))
        value = font.render(str(self.value), True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.x-85, self.y+h_slider//2))
        value_rect = value.get_rect(
            center=(draw_x+0.1*w_slider//2, self.cy-h_slider//2))
        screen.blit(title, title_rect)
        screen.blit(value, value_rect)
        return box

def static_menu():
    # Slicing the screen
    purple=(255, 0, 246)
    pygame.draw.line(screen, purple,(int(WIDTH*2/3),0), (int(WIDTH*2/3),HEIGHT))
    pygame.draw.line(screen, purple,(0,HEIGHT//2), (int(WIDTH*2/3),HEIGHT//2))
    pygame.draw.circle(screen, purple,(WIDTH//2,HEIGHT//2), radius=2)
    # Rendering title
    title_font = pygame.font.Font(None, 50)
    text = title_font.render('Control Panel', True, (255, 255, 255))
    text_rect = text.get_rect(center=(int(WIDTH*5/6),int(0.07*HEIGHT)))
    screen.blit(text, text_rect)


# Setting up sliders
x0=int(WIDTH*5/6-w_slider*0.25)
y0=int(0.2*HEIGHT)
sep=h_slider+50
sliders={
    "Particle size": Slider("Particle size", 0.1, 5, x0, y0, discrete=False),
    "Inital speed": Slider("Inital speed", 0, 500, x0, y0+sep),
    "Elasticity": Slider("Elasticity", 0, 1, x0, y0+2*sep, discrete=False),
    "Pistion speed": Slider("Pistion speed", 1, 200, x0, y0+3*sep),
    "Compression rate": Slider("Compression (%)", 0, 100, x0, y0+4*sep),
    "Number of particles": Slider("N° of particles", 1, 2000, x0, y0+5*sep),
}
StartButton=Button("Start", int(WIDTH*5/6), int(HEIGHT*0.75))
GraphButton=Button("Density graph", int(WIDTH*5/6), int(HEIGHT*0.75)+sep)
buttons=[StartButton, GraphButton]


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
    dragged_slider = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            for slider_name in sliders:
                slider=sliders[slider_name]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:     # Left mouse click
                        mx, my = pygame.mouse.get_pos()
                        if slider.render().collidepoint(mx, my):
                            dragged_slider = slider
                            if mx-0.1*w_slider//2 >= slider.x:
                                slider.cx = min(mx-0.1*w_slider//2, slider.x+0.9*w_slider)
                            elif mx-0.1*w_slider//2 <= slider.x+0.9*w_slider:
                                slider.cx = max(mx-0.1*w_slider//2, slider.x)
                if event.type == pygame.MOUSEMOTION:
                    # Prevents updating the dragged slider more than once
                    # in the for loop on the sliders
                    if dragged_slider==slider:
                        if dragged_slider.cx + event.rel[0] >= dragged_slider.x and dragged_slider.cx + event.rel[0] <= dragged_slider.x+0.9*w_slider:
                            dragged_slider.cx += event.rel[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragged_slider = None

        # Wiping off the screen
        screen.fill((0, 0, 0))

        # Re-drawing elements
        for slider_name in sliders:
            sliders[slider_name].render()
        
        for button in buttons:
            button.render()
        static_menu()
        pygame.display.update()
    pygame.quit()

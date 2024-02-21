import pygame
import pymunk
import random
import time

'''--- INITIALIZING ENVIRONEMENT & GLOBAL CONSTANTS ---'''

clock = pygame.time.Clock()
FPS=180
compression_start_time=60
pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = int(
    0.95*pygame.display.Info().current_w), int(0.95*pygame.display.Info().current_h)
FONT_SIZE = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Height and width of certain elements
w_slider = int(0.2*WIDTH)
h_slider = int(0.03*HEIGHT)

w_wave= int(WIDTH*2/3)
h_wave= int(HEIGHT/2)


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


# Initializing up sliders
x0=int(WIDTH*5/6-w_slider*0.25)
y0=int(0.2*HEIGHT)
sep=h_slider+50
sliders={
    "Particle size": Slider("Particle size", 0.1, 5, x0, y0),
    "Inital speed": Slider("Inital speed", 0, 500, x0, y0+sep),
    "Elasticity": Slider("Elasticity", 0, 1, x0, y0+2*sep, discrete=False),
    "Piston speed": Slider("Piston speed", 1, 200, x0, y0+3*sep),
    "Compression rate": Slider("Compression (%)", 0, 100, x0, y0+4*sep),
    "Number of particles": Slider("N° of particles", 1, 500, x0, y0+5*sep),
}
StartButton=Button("Start", int(WIDTH*5/6), int(HEIGHT*0.75))
GraphButton=Button("Density graph", int(WIDTH*5/6), int(HEIGHT*0.75)+sep)
buttons=[StartButton, GraphButton]


'''--- SIMULATION ELEMENTS ---'''


class Ball():
    def __init__(self, x, y, speed_limit, particle_size, elasticity):
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
        self.shape = pymunk.Segment(self.body, p1, p2, 3)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)

class Kinematic_Wall():
    def __init__(self, p1, p2, pusher_speed, compression):
        self.speed=pusher_speed
        # Multiplying by frame rate because units 
        self.run_time=FPS*(w_wave*compression/(100*pusher_speed))
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 10)
        self.shape.body.velocity = (0, 0)
        self.shape.elasticity = 1
        self.time = 0
        space.add(self.shape, self.body)

    def stop(self):
        self.time = self.time+1
        if self.time < compression_start_time:
            self.shape.body.velocity = (0, 0)
        elif self.time > self.run_time+compression_start_time:
            self.shape.body.velocity = (0, 0)
        else:
            self.shape.body.velocity = (self.speed, 0)

def start_wave():
    # Removing old shapes
    for shape in space.shapes:
        space.remove(shape)
    for body in space.bodies:
        space.remove(body)

    # Fetching sliders' values 
    particle_size=sliders["Particle size"].value
    speed_limit=sliders["Inital speed"].value
    elasticity=sliders["Elasticity"].value
    pusher_speed=sliders["Piston speed"].value
    compression=sliders["Compression rate"].value
    num_of_balls=sliders["Number of particles"].value

    # Creating physical objects
    balls = [Ball(random.randint(0, w_wave), random.randint(0, h_wave), 
                  speed_limit, particle_size,elasticity) for i in range(num_of_balls)]
    piston = Kinematic_Wall((0, 0), (0, h_wave), pusher_speed, compression)
    Satistic_Wall((0, 0), (w_wave, 0)),
    Satistic_Wall((w_wave, 0), (w_wave, h_wave)),
    Satistic_Wall((0, h_wave), (w_wave, h_wave))

    return balls, piston


if __name__ == "__main__":
    WAVE= False
    running = True
    dragged = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: 
                    mx, my = pygame.mouse.get_pos()

                    # Slider logic
                    for slider_name in sliders:
                        slider=sliders[slider_name]
                        if slider.render().collidepoint(mx, my):
                            # Slider presumed dragged
                            dragged = slider_name
                            if mx-0.1*w_slider//2 >= slider.x:
                                slider.cx = min(mx-0.1*w_slider//2, slider.x+0.9*w_slider)
                            elif mx-0.1*w_slider//2 <= slider.x+0.9*w_slider:
                                slider.cx = max(mx-0.1*w_slider//2, slider.x)
                        
                    # Button logic
                    if StartButton.render().collidepoint(mx,my):
                        WAVE=True
                        balls, piston=start_wave()
                    if GraphButton.render().collidepoint(mx,my):
                        pass
            
            # Mouse movement
            if event.type == pygame.MOUSEMOTION:
                # Only update the dragged slider
                if dragged:
                    if sliders[dragged].cx + event.rel[0] >= sliders[dragged].x and sliders[dragged].cx + event.rel[0] <= sliders[dragged].x+0.9*w_slider:
                        sliders[dragged].cx += event.rel[0]
                
            # Left un-click
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragged = None

        # Wiping off the screen
        screen.fill((0, 0, 0))

        # Re-drawing elements
        for slider_name in sliders:
            sliders[slider_name].render()
        
        for button in buttons:
            button.render()
        if WAVE:
            ball_size=balls[0].shape.radius
            for ball in balls:
                x, y = ball.body.position
                pygame.draw.circle(screen, (255, 255, 255),
                                    (int(x), int(y)), ball_size)
            px,py=(piston.body.position[0],piston.shape.center_of_gravity[1])
            pygame.draw.rect(screen, (202, 204, 206),(int(px-5),0,10, h_wave))
            piston.stop()
            clock.tick(FPS)
            space.step(1/FPS)
        

        static_menu()
        pygame.display.update()
    pygame.quit()

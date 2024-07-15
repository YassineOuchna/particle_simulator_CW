import pygame
import pymunk
import random
import time
from numpy import sqrt

# --- INITIALIZING ENVIRONEMENT & GLOBAL CONSTANTS ---

clock = pygame.time.Clock()
FPS=120
compression_start_time=60
pygame.init()
space = pymunk.Space()
WIDTH, HEIGHT = int(
    pygame.display.Info().current_w), int(pygame.display.Info().current_h)
FONT_SIZE = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Height and width of certain elements
w_slider = int(0.2*WIDTH)
h_slider = int(0.03*HEIGHT)

# Coords of the top left of wave sim
x_wave=30
y_wave=30
# Coords of the bottom right of wave sim
w_wave= int(WIDTH*2/3) - x_wave
h_wave= int(HEIGHT/2) - y_wave


# --- GUI ELEMENTS ---

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
        
        # Drawing slider handle
        pygame.draw.rect(
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

    def click_update(self, mx):
        # Updates position to that of the mouse
        if mx-0.1*w_slider//2 >= self.x:
            self.cx = min(mx-0.1*w_slider//2, self.x+0.9*w_slider)
        elif mx-0.1*w_slider//2 <= self.x+0.9*w_slider:
            self.cx = max(mx-0.1*w_slider//2, self.x)


def draw_menu(sliders : dict[str : Slider], buttons : list[Button]):
    
    # Slicing the screen
    purple=(255, 0, 246)
    pygame.draw.line(screen, purple,(int(WIDTH*2/3),0), (int(WIDTH*2/3),HEIGHT))
    pygame.draw.line(screen, purple,(0,HEIGHT//2), (int(WIDTH*2/3),HEIGHT//2))
    pygame.draw.circle(screen, purple,(WIDTH//2,HEIGHT//2), radius=2)
    
    # Drawing the simulation box
    pygame.draw.line(screen, (255,255,255),(x_wave, y_wave), (w_wave, y_wave))
    pygame.draw.line(screen, (255,255,255),(w_wave, y_wave), (w_wave, h_wave))
    pygame.draw.line(screen, (255,255,255),(x_wave, h_wave), (w_wave, h_wave))
    pygame.draw.line(screen, (255,255,255),(x_wave, y_wave), (x_wave, h_wave))

    # Rendering title
    title_font = pygame.font.Font(None, 50)
    text = title_font.render('Control Panel', True, (255, 255, 255))
    text_rect = text.get_rect(center=(int(WIDTH*5/6),int(0.07*HEIGHT)))
    screen.blit(text, text_rect)

    # Rendering UI elements 
    for slider_name in sliders:
        sliders[slider_name].render()
    
    for button in buttons:
        button.render()

def inside_box(x : int,y : int)-> bool:
    ''' Takes the coordinates of 
    a ball and returns True 
    if it is inside the sim box :
    surrounded by the piston and sim walls
    '''
    # Pistion's x-position
    px = piston.body.position[0]
    return x >= x_wave + int(px+10) and x <= w_wave and y >= y_wave and y <= h_wave

# Initializing sliders
x0=int(WIDTH*5/6-w_slider*0.25)
y0=int(0.2*HEIGHT)
sep=h_slider+50
sliders={
    "Particle size": Slider("Particle size", 1, 10, x0, y0),
    "Inital speed": Slider("Inital speed", 0, 200, x0, y0+sep),
    "Elasticity": Slider("Elasticity", 0, 1, x0, y0+2*sep, discrete=False),
    "Piston speed": Slider("Piston speed", 1, 400, x0, y0+3*sep),
    "Compression rate": Slider("Compression (%)", 0, 100, x0, y0+4*sep),
    "Number of particles": Slider("N° of particles", 1, 1000, x0, y0+5*sep),
}
StartButton=Button("Start", int(WIDTH*5/6), int(HEIGHT*0.75))
QuitButton=Button("Quit", int(WIDTH*5/6), int(HEIGHT*0.75)+sep)
buttons=[StartButton, QuitButton]


# --- SIMULATION ELEMENTS ---


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
        self.run_time=FPS*((w_wave-x_wave)*compression/(100*pusher_speed))
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
    balls = set()
    for i in range(num_of_balls):
        balls.add(Ball(random.randint(x_wave, w_wave), random.randint(y_wave, h_wave), 
                  speed_limit, particle_size,elasticity))

    piston = Kinematic_Wall((x_wave, y_wave), (x_wave, h_wave), pusher_speed, compression)
    Satistic_Wall((x_wave, y_wave), (w_wave, y_wave))
    Satistic_Wall((w_wave, y_wave), (w_wave, h_wave))
    Satistic_Wall((x_wave, h_wave), (w_wave, h_wave))

    return balls, piston

def draw_wave(balls : set[Ball], piston : Kinematic_Wall):
    for ball in balls:
        ball_size=ball.shape.radius
        break

    pygame.draw.circle(screen, (255, 0, 0),(x_wave, y_wave), ball_size)
    pygame.draw.circle(screen, (255, 0, 0),(w_wave, h_wave), ball_size)
    
    # List of balls that are out of bounds
    outOfBounds = []
    for ball in balls:
        x, y = ball.body.position
        # Assuring the ball is in the box
        if inside_box(int(x),int(y)):
            pygame.draw.circle(screen, (255, 255, 255),(int(x), int(y)), ball_size)
        else:
            outOfBounds.append(ball)
    
    # Removing balls
    for ball in outOfBounds:
        balls.discard(ball)

    px=piston.body.position[0]
    pygame.draw.rect(screen, (202, 204, 206),(int(px+x_wave),y_wave,10, h_wave-y_wave))
    pygame.draw.rect(screen, (202, 204, 206),(x_wave,(h_wave+y_wave)//2-5,int(px), 10))
    piston.stop()

def graph_wave(balls : set[Ball]):
    ArrowSize=10
    nbrSplits=50

    # x and y axis
    pygame.draw.line(screen, (255,255,255),(x_wave,HEIGHT-y_wave), (w_wave,HEIGHT-y_wave))
    pygame.draw.line(screen, (255,255,255),(x_wave,HEIGHT-y_wave), (x_wave,HEIGHT//2+y_wave))
    pygame.draw.polygon(screen, (255,255,255), 
                        points=[(int(w_wave-ArrowSize/sqrt(2)),int(HEIGHT-y_wave-ArrowSize/sqrt(2))), 
                                (w_wave,HEIGHT-y_wave), (int(w_wave-ArrowSize/sqrt(2)),int(HEIGHT-y_wave+ArrowSize/sqrt(2)))])
    pygame.draw.polygon(screen, (255,255,255), 
                        points=[(int(x_wave+ArrowSize/sqrt(2)),int(HEIGHT//2+y_wave+ArrowSize/sqrt(2))), 
                                (x_wave,HEIGHT//2+y_wave), (int(x_wave-ArrowSize/sqrt(2)),int(HEIGHT//2+y_wave+ArrowSize/sqrt(2)))])
                        
    xScale=int((w_wave-x_wave)/nbrSplits)
    bins=[0]*(nbrSplits+1)
    avg=0
    for ball in balls:
        x =ball.body.position[0]
        binIndex=min(int((x-x_wave)/xScale),nbrSplits)
        binIndex=max(binIndex,0)
        bins[binIndex]+=1

    max_val=max(bins)
    yScale=int(0.85*(h_wave-y_wave)/max_val)
    # Drawing maximum density for reference
    pygame.draw.line(screen, (255,255,255),(x_wave,HEIGHT-y_wave-max_val*yScale), (int(x_wave*1.2),HEIGHT-y_wave-max_val*yScale))
    y_font = pygame.font.Font(None, 20)
    ytext = y_font.render(f"{max_val}", True, (255, 255, 255))
    ytext_rect = ytext.get_rect(center=(x_wave//3,HEIGHT-y_wave-max_val*yScale))
    screen.blit(ytext, ytext_rect)
    for i in range(len(bins)):
        pygame.draw.rect(screen, (38,247,253),(i*xScale+x_wave-xScale//2,HEIGHT-y_wave-bins[i]*yScale,xScale, bins[i]*yScale))
        pygame.draw.line(screen, (255,255,255),(i*xScale+x_wave,HEIGHT-y_wave), (i*xScale+x_wave,HEIGHT-int(y_wave*4/5)))
    
    pygame.draw.lines(screen, (255, 165, 0), closed=False, points=[(i*xScale+x_wave, HEIGHT-y_wave-bins[i]*yScale) for i in range(len(bins))])

    
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
                            slider.click_update(mx)
                        
                    # Button logic
                    if StartButton.render().collidepoint(mx,my):
                        WAVE=True
                        balls, piston=start_wave()
                    if QuitButton.render().collidepoint(mx,my):
                        running=False
            
            # Mouse movement
            if event.type == pygame.MOUSEMOTION:
                # Only update the dragged slider
                if dragged:
                    s=sliders[dragged]
                    if s.cx + event.rel[0] >= s.x and s.cx + event.rel[0] <= s.x+0.9*w_slider:
                        s.cx += event.rel[0]
                
            # Left un-click
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragged = None

        # Wiping off the screen
        screen.fill((15,23,42))

        # Re-drawing elements
        draw_menu(sliders, buttons)

        if WAVE:
            graph_wave(balls)
            draw_wave(balls, piston)
            clock.tick(FPS)
            space.step(1/FPS)

        pygame.display.update()
    pygame.quit()

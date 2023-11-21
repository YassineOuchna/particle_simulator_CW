from tkinter import *
from tkinter import font
import pygame
import random
import pymunk
import os
# create the window
window = Tk()
window.title('Piston simulator')

# getting width and height of display
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d" % (w, h))
# creation label des parametres
label_par = Label(window, text="Control panel")
label_par['font'] = font.Font(size=20)
label_par.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.1)
# Labels
size = 12
l_par_size = Label(window, text="Particle size")
l_par_size['font'] = font.Font(size=size)
l_v0 = Label(window, text="Max speed")
l_v0['font'] = font.Font(size=size)
l_ela = Label(window, text="Elasticity")
l_ela['font'] = font.Font(size=size)
l_p_s = Label(window, text="Pusher speed")
l_p_s['font'] = font.Font(size=size)
l_p_t = Label(window, text="Distance travelled")
l_p_t['font'] = font.Font(size=size)
num_par = Label(window, text="Number of particles")
num_par['font'] = font.Font(size=size)
# emplacement des labels
l_par_size.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.1)
l_v0.place(relx=0.7, rely=0.2, relwidth=0.1, relheight=0.1)
l_ela.place(relx=0.7, rely=0.3, relwidth=0.1, relheight=0.1)
l_p_s.place(relx=0.7, rely=0.4, relwidth=0.1, relheight=0.1)
l_p_t.place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.1)
num_par.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.1)
# Parameters input
slider_particle_size = Scale(window, from_=0, to=5, orient=HORIZONTAL)
slider_particle_size.set(1)

slider_speed_limit = Scale(window, from_=0, to=500, orient=HORIZONTAL)
slider_speed_limit.set(100)

slider_elasticity = Scale(window, from_=0, to=1,
                          digits=3, resolution=0.1, orient=HORIZONTAL)
slider_elasticity.set(1)

slider_pusher_speed = Scale(window, from_=0, to=200,
                            orient=HORIZONTAL)
slider_pusher_speed.set(100)

slider_pusher_distance = Scale(
    window, from_=0, to=w/2, orient=HORIZONTAL)
slider_pusher_distance.set(100)

slider_num_particles = Scale(window, from_=0, to=2500, orient=HORIZONTAL)
slider_num_particles.set(1000)


# Entry placement
slider_particle_size.place(relx=0.8, rely=0.12, relwidth=0.2, relheight=0.1)
slider_speed_limit.place(relx=0.8, rely=0.22, relwidth=0.2, relheight=0.1)
slider_elasticity.place(relx=0.8, rely=0.32, relwidth=0.2, relheight=0.1)
slider_pusher_speed.place(relx=0.8, rely=0.42, relwidth=0.2, relheight=0.1)
slider_pusher_distance.place(relx=0.8, rely=0.52, relwidth=0.2, relheight=0.1)
slider_num_particles.place(relx=0.8, rely=0.62, relwidth=0.2, relheight=0.1)
# getting parameters


def getting_parameters():
    global particle_size
    particle_size = slider_particle_size.get()
    global speed_limit
    speed_limit = slider_speed_limit.get()
    global elasticity
    elasticity = slider_elasticity.get()
    global pusher_run_time
    pusher_run_time = (slider_pusher_distance.get() /
                       slider_pusher_speed.get())*Fps
    global pusher_elasticity
    pusher_elasticity = 1
    global pusher_speed
    pusher_speed = slider_pusher_speed.get()
    global num_of_balls
    num_of_balls = slider_num_particles.get()


# Importing simulation objects
height = 1*h/3
width = 2*w/3
pusher_start_time = 150
Fps = 180

# Importing the code for the simulation


def start():
    x = 10
    y = 50
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    clock = pygame.time.Clock()
    space = pymunk.Space()
    getting_parameters()
    pygame.init()
    display = pygame.display.set_mode((width, height))

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
                self.shape.body.velocity = (pusher_speed, 0)

    balls = [Ball(random.randint(0, width), random.randint(0, height))
             for i in range(num_of_balls)]
    # collision handler

    pushers = [Kinematic_Wall((0, 0), (0, height))]

    walls = [Satistic_Wall((0, 0), (width, 0)),
             Satistic_Wall((width, 0), (width, height)),
             Satistic_Wall((0, height), (width, height))
             ]
    global run
    run = True

    while run:  # one while loop equals one frame

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False  # when click x make sure it close
                break
        display.fill((0, 0, 0))

        for ball in balls:
            x, y = ball.body.position
            pygame.draw.circle(display, (255, 255, 255),
                               (int(x), int(y)), particle_size)
        pushers[0].stop()

        clock.tick(Fps)
        pygame.display.update()
        window.update()
        space.step(1/Fps)
    pygame.quit()


def stop():
    global run
    run = False


# buttons
start_button = Button(window, text='Start', fg='green', command=start)
start_button.place(relx=0.8, rely=0.72, relwidth=0.15)
stop_button = Button(window, text='stop', fg='red', command=stop)
stop_button.place(relx=0.8, rely=0.82, relwidth=0.15)
mainloop()

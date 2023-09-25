from tkinter import *
from tkinter import font
import matplotlib.pyplot as plt
import pygame
import pymunk
import os
import demo_second_mode_refactored
import os
# create the window
window = Tk()
window.title('Piston simulator')

# getting width and height of display
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d" % (int(0.25*w), int(h-50)) +
                '+' + str(int(0.75*w)) + '+' + '0')
# creation label des parametres
label_par = Label(window, text="Control panel")
label_par['font'] = font.Font(size=20)
label_par.place(relx=0, rely=0, relwidth=1, relheight=0.1)
# Labels
size = 12
l_par_size1 = Label(window, text="Particle size 1")
l_par_size1['font'] = font.Font(size=size)
l_v1 = Label(window, text="Max speed 1")
l_v1['font'] = font.Font(size=size)
l_ela = Label(window, text="Elasticity")
l_ela['font'] = font.Font(size=size)
l_par_size2 = Label(window, text="Particle size 2")
l_par_size2['font'] = font.Font(size=size)
num_par1 = Label(window, text="N1")
num_par1['font'] = font.Font(size=size)
num_par2 = Label(window, text="N2")
num_par2['font'] = font.Font(size=size)
l_v2 = Label(window, text="Max speed 2")
l_v2['font'] = font.Font(size=size)
# emplacement des labels
l_par_size1.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.1)
l_par_size2.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.1)
l_v1.place(relx=0, rely=0.3, relwidth=0.5, relheight=0.1)
l_v2.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.1)
l_ela.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.1)
num_par1.place(relx=0, rely=0.6, relwidth=0.5, relheight=0.1)
num_par2.place(relx=0, rely=0.7, relwidth=0.5, relheight=0.1)
# Parameters input
slider_particle_size1 = Scale(window, from_=0, to=5, orient=HORIZONTAL)
slider_particle_size1.set(1)

slider_speed_1 = Scale(window, from_=0, to=500, orient=HORIZONTAL)
slider_speed_1.set(100)

slider_speed_2 = Scale(window, from_=0, to=500, orient=HORIZONTAL)
slider_speed_2.set(100)

slider_elasticity = Scale(window, from_=0, to=1,
                          digits=3, resolution=0.1, orient=HORIZONTAL)
slider_elasticity.set(1)

slider_particle_size2 = Scale(window, from_=0, to=5,
                              orient=HORIZONTAL)
slider_particle_size2.set(1)

slider_num_particles1 = Scale(window, from_=0, to=2500, orient=HORIZONTAL)
slider_num_particles1.set(1000)

slider_num_particles2 = Scale(window, from_=0, to=2500, orient=HORIZONTAL)
slider_num_particles2.set(1000)


# Entry placement
slider_particle_size1.place(relx=0.5, rely=0.12, relwidth=0.5, relheight=0.1)
slider_particle_size2.place(relx=0.5, rely=0.22, relwidth=0.5, relheight=0.1)
slider_speed_1.place(relx=0.5, rely=0.32, relwidth=0.5, relheight=0.1)
slider_speed_2.place(relx=0.5, rely=0.42, relwidth=0.5, relheight=0.1)
slider_elasticity.place(relx=0.5, rely=0.52, relwidth=0.5, relheight=0.1)
slider_num_particles1.place(relx=0.5, rely=0.62, relwidth=0.5, relheight=0.1)
slider_num_particles2.place(relx=0.5, rely=0.72, relwidth=0.5, relheight=0.1)
# getting parameters


def getting_parameters():
    global particle_size1
    particle_size1 = slider_particle_size1.get()
    global speed_limit1
    speed_limit1 = slider_speed_1.get()
    global speed_limit2
    speed_limit2 = slider_speed_2.get()
    global elasticity
    elasticity = slider_elasticity.get()
    global particle_size2
    particle_size2 = slider_particle_size2.get()
    global num_par1
    num_par1 = slider_num_particles1.get()
    global num_par2
    num_par2 = slider_num_particles2.get()


# Importing simulation objects
height = int(1*h/3)
width = int(0.75*w)

# Importing the code for the simulation


def start():
    plt.close()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
    demo_second_mode_refactored.window = window
    demo_second_mode_refactored.display = pygame.display.set_mode(
        (width, height))
    demo_second_mode_refactored.clock = pygame.time.Clock()
    demo_second_mode_refactored.space = pymunk.Space()
    pygame.init()
    getting_parameters()
    demo_second_mode_refactored.num_of_balls_1 = num_par1
    demo_second_mode_refactored.num_of_balls_2 = num_par2
    demo_second_mode_refactored.el = elasticity
    demo_second_mode_refactored.speed_limit1 = speed_limit1
    demo_second_mode_refactored.speed_limit2 = speed_limit2
    demo_second_mode_refactored.particle_size1 = particle_size1
    demo_second_mode_refactored.particle_size2 = particle_size2
    demo_second_mode_refactored.game(width, height)


def poof():
    demo_second_mode_refactored.poof_wall.delete()


def graphing():
    demo_second_mode_refactored.nerd_mode = True


def stop():
    demo_second_mode_refactored.run = False


# buttons
start_button = Button(window, text='Start', fg='green', command=start)
start_button.place(relx=0.25, rely=0.78, relwidth=0.5)
poof_button = Button(window, text='Wall Poof', fg='purple', command=poof)
poof_button.place(relx=0.25, rely=0.83, relwidth=0.5)
graph_button = Button(window, text='Graphing density',
                      fg='black', command=graphing)
graph_button.place(relx=0.25, rely=0.88, relwidth=0.5)
stop_button = Button(window, text='Stop', fg='red', command=stop)
stop_button.place(relx=0.25, rely=0.93, relwidth=0.5)
mainloop()

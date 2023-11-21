# The Particles Collision Simulator

## Description
This project aims to use pygame and pymunk to simulate the behaviour of gas/fluid particles. The simulation is done in 2D (as pymunk is a 2D physics engine) and the particles are idealized as **rigid body balls** with varying size, elasticity, friction and so on.

Due to the limitation of the game engine and cpu performance, we only simulate the behaviour of around 10000 particles, which is quiet different from real world situation. Because of the deviation from the real world, we are more than exited to see how the paritcles behave compared to the real world situation.
### **Features**
The simulator consists of two modes : *diffusion mode* and *wave mode*, each mode allows users to alter the number of particles, size of the particles, initial speed distribution, elasticity and friction via a Graphic interface. 

## Wave mode 

By running the file *wave_mode.py*, you are presented with an interface to change different parameters in an experiment simulating a piston wall pushing on particles.

*Preview of the wave mode* 

<img src='./demos/wave.gif?raw=true'/>


## Diffusion mode 

By running the file *diffusion_mode.py*, you are presented with an
 interface to change different parameters as well as a button to graph 
particle density in real time (although quite laggy). The simulation
to show the diffusion of two types of particles in two initially seperated compartiments that are fused into one compartiment
by deleting the wall sperating them. 

*Preview of the diffusion mode*

<img src='./demos/diffusion.gif?raw=true'/>


## Installation
The simulator requires the following python packages:

tkinter

pymunk

pygame

matplotlib

numpy


## Roadmap
We could improve the simulator by first fusing the two modes into a single interface and optimizing performance while graphing and simulating at the same time.



## Authors and acknowledgment
This project is made for the Codingweek of CentraleSupelec. And It is made by team physiX(Group 17). 
Its members including:

Alae Taoudi

Bastien Li

Bowen Zhu

Lezhi Pu

Mohamed Taha Afif

Yassine Ouchna








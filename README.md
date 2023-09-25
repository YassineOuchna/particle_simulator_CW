# The Particles Collision Simulator





***

# README







## Description
This project aims to use pygame and pymunk to simulate the behaviour of gas/fluid particles. The simulation is done in 2D (as pymunk is a 2D physics engine) and the particles is idealized as **rigid body balls** with varing size, elasticity, fiction and so on.

Due to the limitation of the game engine and cpu performance, we only simulate the behaviour of around 10000 particles, which is quiet different from real world situation. Because of the deviation from the real world, we are more than exited to see how the paritcles behave compared to the real world situation.
### **Features**
The simulator should allow user to alter the number of particles, size of the particles, initial speed distribution, elasticity and friction via a Graphic interface. 
***
The simulator should allow user to switch between different simulation modes. 

For example: *wave measurement mode* would give the particle a small pertubation and simulate the propagation of wave.

In *diffusion mode*, there will be no boundary walls, thus one can diffusion of particles
***
The simulation should give the distribution of pariticle velocity at real time. In different simulation mode, the simulator should give out different simulation satistics.

For example, in *wave measurement mode*, the simulator should give out the 1D particle distribution with respect to the coordinate.

In *diffusion mode*, the simulator should give out the diffusion rate.





## Visuals
Update 12/11/2022

![Wave like behaviour of particles](https://media.giphy.com/media/fj0YZa5EkzHrQioMew/giphy-downsized-large.gif) 

## Installation
The simulator requires the following python packages:

pymunk

pygame

matplotlib

numpy



## Support
If you have any problem with the simulator. 

Please contact Bowen.zhu@student-cs.fr

## Roadmap
Planning for the future. Additional playground mode may be released where you can place obstacles to see the behaviour of the particles.



## Authors and acknowledgment
This project is made for the Codingweek of CentraleSupelec. And It is made by team physiX(Group 17). 
Its members including:

Alae Taoudi

Bastien Li

Bowen Zhu

Lezhi Pu

Mohamed Taha Afif

Yassine Ouchna








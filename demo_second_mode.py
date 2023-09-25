import pygame
import random
import pymunk


pygame.init()
height=500
width=2100
num_of_balls_1=5000
num_of_balls_2=5000
display = pygame.display.set_mode((width,height))
clock=pygame.time.Clock()
Fps=120
fat=20
particle_size= 1
space=pymunk.Space()
num_ball_difused1=[]
num_ball_difused2=[]
Poof_time=60

class Ball():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.body=pymunk.Body()
        self.body.position=x,y
        #100 in velocity means 100 frames per sec
        self.body.velocity=random.uniform(-100,100),random.uniform(-500,500) #random float nunber
        self.shape = pymunk.Circle(self.body,particle_size)
        self.shape.density=1
        self.shape.elasticity =1
        space.add(self.body,self.shape)
   
    def draw1(self):
        x,y=self.body.position
        pygame.draw.circle(display,(255,0,100),(int(x),int(y)),particle_size)
    def draw2(self):
        x,y=self.body.position
        pygame.draw.circle(display,(0,100,255),(int(x),int(y)),particle_size)

class Satistic_Wall():
    def __init__(self,p1,p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1 ,p2, 20) # I don't quite understand it here
        self.shape.elasticity = 1
        space.add(self.shape, self.body)

class Poof_Wall():
    def __init__(self,p1,p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1 ,p2, fat)
        self.shape.elasticity = 1
        space.add(self.shape, self.body)


def game(width,height):
    balls_1 = [Ball(random.randint(0,width/2-fat),random.randint(0,height)) for i in range(num_of_balls_1)]
    balls_2 = [Ball(random.randint(width/2+fat,width),random.randint(0,height)) for i in range(num_of_balls_2)]
    
  
    walls= [Satistic_Wall((0,0),(width,0)),
            Satistic_Wall((width,0),(width,height)),
            Satistic_Wall((0,height),(width,height)),
            Satistic_Wall((0,0),(0,height))
            ]
    poof_wall=Poof_Wall((width/2,0),(width/2,height))

    run= True
    time=0

    while run: 
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #x Button closes the file
                break
        display.fill((0,0,0))
        ball_difused1=[]
        ball_difused2=[]

        for ball in balls_1:
            ball.draw1()
            if ball.body.position[0]>width/2 and time%50==0:
                ball_difused1.append(ball)
        for ball in balls_2:
            ball.draw2()
            if ball.body.position[0]<width/2 and time%50==0:
                ball_difused2.append(ball)
        if time%50==0:
            num_ball_difused1.append(len(ball_difused1))
            num_ball_difused2.append(len(ball_difused2))
            print(len(ball_difused1),len(ball_difused2))
        time+=1
        if time==Poof_time:
            space.remove(poof_wall.shape,poof_wall.body)

        clock.tick(Fps)
        pygame.display.update()
        space.step(1/Fps)
    pygame.quit()
 

if __name__=='__main__':
    game(width,height)
    

# Coding Handbook

## Use proper variable name

Use variable name with proper meaning and do not be afraid of the length of the variable

E.g.

    NUMBER_OF_BALLS= 50

## Do not hard coding number

Use variables instead of implicit numbers

E.g.

    for i in range(50): #WRONG

    NUMBER_OF_BALLS=50  #RIGHT
    for i in range(NUMBER_OF_BALLS):

## Code commenting

Comment code frequently

E.g.

    while run: # one while loop equals one frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # when click x make sure it close
                break

## Use classes

When defining a centain type of object, use class. Classes make the code more modular and it is easy to pass values in a class.

E.g.

    class Kinematic_Wall():
        def __init__(self,p1,p2):
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            self.shape = pymunk.Segment(self.body, p1 ,p2, 15)
            self.shape.body.velocity = (0, 0)
            self.shape.elasticity = 1
            self.time=0
            space.add(self.shape, self.body)
        def stop(self):
            self.time=self.time+1
            if self.time<pusher_start_time:
                self.shape.body.velocity = (0, 0)
            elif self.time>pusher_run_time+pusher_start_time:
                self.shape.body.velocity = (0, 0)
            else:
                self.shape.body.velocity = (500, 0) 

## Do not write super long sentence in one line
Try to split it

E.g.

    walls= [Satistic_Wall((0,0),(width,0)),
            Satistic_Wall((width,0),(width,height)),
            Satistic_Wall((0,height),(width,height))
            ]

## Indicate which part of the code you have changed

Indicate change compare to the main branch

When adding, use this marker below:

    ### Created on Nov 10 11:21:23 2022
    my_file_divide_filter.run()
    ### end here

When deleting(do not easily delete others' code), comment the original code:

    #my_file_divide_filter.run() ### Deleted on Nov 10 11:21:23 2022
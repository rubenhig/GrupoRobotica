"""Display_emoticonos controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor

from random import random, seed, randint
from controller import Robot,Display,Supervisor
from math import pi, sin

# intanciar el robot.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# insertar display:
disp= robot.getDevice("display_emoticonos")

# png con emoticonos
emotiArbeloas = disp.imageLoad("emoticons.png")

# Main loop:
contador = 0
EMOTICON_WIDTH = 14
EMOTICON_HEIGHT = 14
EMOTICONS_NUMBER_X = 5
EMOTICONS_NUMBER_Y = 11
seed(1)
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    contador = contador + 1
    if(contador % 30 == 1):
      
       x = -EMOTICON_WIDTH * (randint(0, 10000) % EMOTICONS_NUMBER_X)
       y = -EMOTICON_HEIGHT * (randint(0, 10000) % EMOTICONS_NUMBER_Y)
       disp.imagePaste(emotiArbeloas,x,y,True)
       
pass

# Enter here exit cleanup code.

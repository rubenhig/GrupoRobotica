"""controlador_belt controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
motor = robot.getDevice('linear motor')

# Main loop:
# - perform simulation steps until Webots is stopping the controller
p = 0.0

while robot.step(timestep) != -1:
    p += 0.007
    
    motor.setPosition(p)
    pass

# Enter here exit cleanup code.

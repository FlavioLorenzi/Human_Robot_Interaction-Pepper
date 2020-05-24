import os, sys

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin() # connect to robot/simulator with IP in PEPPER_IP env variable

#print(pepper_cmd.robot.getPosture())

pepper_cmd.robot.setAlive(True)
pepper_cmd.robot.startFaceDetection()


p = pepper_cmd.robot.getState()
headyaw = p[0]
#if you move, the head of the robot will move with you si p[0] will change

if headyaw == 0:
	pepper_cmd.robot.say('I am tracking your face')

if headyaw > 0:
	pepper_cmd.robot.raiseArm('R')
	print('alzo la mano destra')

if headyaw < 0:
	pepper_cmd.robot.raiseArm('L')



pepper_cmd.robot.stopFaceDetection()
pepper_cmd.robot.setAlive(False)


end()
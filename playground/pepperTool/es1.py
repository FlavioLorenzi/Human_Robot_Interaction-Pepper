import os, sys

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin() # connect to robot/simulator with IP in PEPPER_IP env variable

#Request A
frontsonar = pepper_cmd.robot.sensorvalue('frontsonar')

if frontsonar != 0.0:
	pepper_cmd.robot.say("Hello. How are you?")
	print("GENERAL KENOBI!")

else:
	print("No one there?")
		

#Request B
rearsonar = pepper_cmd.robot.sensorvalue('rearsonar')
handRtouch = pepper_cmd.robot.sensorvalue('righthandtouch')
handLtouch =  pepper_cmd.robot.sensorvalue('lefthandtouch')
headTouch =  pepper_cmd.robot.sensorvalue('headtouch')

if frontsonar != 0.0:
	if handRtouch != 0.0:
		#yaw is no #pitch is yes #tm is time
		pepper_cmd.robot.headPose(3,0,2)
		print(pepper_cmd.robot.headPose(yaw,pitch,2))

	elif handLtouch != 0.0:
		pepper_cmd.robot.headPose(-3,0,2)


elif rearsonar != 0.0:
	if headTouch != 0.0:
		pepper_cmd.robot.say("Who is behind me?")


#Request C
if frontsonar != 0.0:
	pepper_cmd.robot.wait()
	pepper_cmd.robot.say("Hello there")

elif rearsonar != 0.0:
	pepper_cmd.robot.wait()
	pepper_cmd.robot.say("Who is behind me?")


end()



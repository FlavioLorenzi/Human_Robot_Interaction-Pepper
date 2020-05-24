import os, sys

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin() # connect to robot/simulator with IP in PEPPER_IP env variable

#Request B
pepper_cmd.robot.raiseArm('R')  #HoW can i access to the joint values?
pepper_cmd.robot.raiseArm('L')


pepper_cmd.robot.say('Which hand hides a candy?')

pepper_cmd.robot.wait()

if pepper_cmd.robot.asr('left'):
	pepper_cmd.robot.raiseArm('L')

if pepper_cmd.robot.asr('right'):
	pepper_cmd.robot.raiseArm('R')

end()
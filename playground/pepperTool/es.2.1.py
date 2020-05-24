'''esercizio in cui pepper vede una persona entro un range e gli suona musica
e gli chiede se gli è piaciuta'''

import os, sys

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin() # connect to robot/simulator with IP in PEPPER_IP env variable

pepper_cmd.robot.startSensorMonitor()
#Request A
sonar = pepper_cmd.robot.sensorvalue()
frontsonar = sonar[1]
print('rilevo distanza di',frontsonar)

if frontsonar >0.9 and frontsonar <1.6:

#Per avere un riscontro andare su src/peppertools/sonar sonar_sim.py e digitare 
#--sonar SonarFront o SonarBack  + --value xxx + --duration 60


	print('Ti vedo e suonero per te')
	pepper_cmd.robot.wait() #non penso serva, il tempo va settato dal sim
	pepper_cmd.robot.sax()
	

	pepper_cmd.robot.say('Did you like my performance?')


	#Per avere un riscontro andare su src/peppertools/asr  human_say.py e digitare --sentence yes/no
	#yes e no sono le answers umane
	if pepper_cmd.robot.asr('yes'): 
		pepper_cmd.robot.say('Thanks, I love you!')

	if pepper_cmd.robot.asr('no'): 
		pepper_cmd.robot.say('Ah ok, so I will stop with the music, sigh sigh, forever')

pepper_cmd.robot.stopSensorMonitor()
end()
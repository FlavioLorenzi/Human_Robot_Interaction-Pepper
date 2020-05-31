import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *


#metodo che permette al robot di girare per l'ospedale: se trova un paziente fuori dal letto reagisce di conseguenza
#dipende da cosa questo ha bisogno: xes if sta male dagli medicina o chiama medico; if ha mal di testa digli prendi aspirina
#robot da anche consigli ecc..

#NB: a differenza di infopoint questo script usa le action! ! ! 

def supervisor():
    im.init()
    im.robot.startSensorMonitor()
    a = True

    sonar = im.robot.sensorvalue()
    frontsonar = sonar[1]
    print('Rilevo distanza di',frontsonar)      #qui aggiungere il face recognition per ''non parlare con i muri'' TODO

    #if frontsonar >0.1 and frontsonar <3:
    if a == True:


        im.display.loadUrl('supervisor.html')

        time.sleep(1)

        # Setting HTML element of the web page

        im.executeModality('TEXT_title','ALT')
        im.executeModality('TEXT_default','Eih you, STOP')
        #im.executeModality('TTS','Welcome to the Sacred Heart Hospital')
        #im.executeModality('IMAGE','img/welcomeH.jpg')
     
        im.robot.raiseArm('R') #alt fermati con la mano

        time.sleep(2)

        #im.robot.normalPosture()

        # Using TTS service of the robot to SPEAK 
        #im.executeModality('TTS','I am Pepper and like my fellow doctors, I am here to help people')

        im.executeModality('TEXT_default','What are you doing ? Its night!')

        time.sleep(3)







if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    mws.run_interaction(supervisor) # blocking

 
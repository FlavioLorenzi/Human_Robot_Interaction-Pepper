import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *






# Definition of interaction functions
#se rileva qualcuno nel range allora dice benvenuto con tablet e voce

def e1():
    im.init()
    im.robot.startSensorMonitor()

    sonar = im.robot.sensorvalue()
    frontsonar = sonar[1]
    print('rilevo distanza di',frontsonar)

    if frontsonar >0.1 and frontsonar <3:


        
        im.display.loadUrl('layout.html')

        time.sleep(2)

        # Setting HTML element of the web page
        im.executeModality('TEXT_title','HRI 2020')
        im.executeModality('TEXT_default','Hello there!')
        im.executeModality('IMAGE','img/benvenuto.png')
        #gesture mancante

        # Using TTS service of the robot to SPEAK 
        im.executeModality('TTS','Hello there, Welcome my friend')


#chiede se ti sei perso e reagisce di conseguenza

def e2():

    im.executeModality('TEXT_default','Are you lost?')

    #im.executeModality('ASR',['yes','no'])
    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

    # wait for answer
    a = im.ask(actionname=None, timeout=10)

    if a=='yes':
        im.executeModality('TEXT_default','Ok I am calling help')
        #im.robot.dance() #qualcosa da pepper tool function
        im.robot.say("Heeelp")
        im.executeModality('IMAGE','img/callhelp.png')
    else:
        im.executeModality('IMAGE','img/rainbow.jpg')
        im.executeModality('TEXT_default','OK. Have a nice day')

    time.sleep(2)
    im.executeModality('TEXT_default','Bye bye')

# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    #due metodi per welcome e domanda e risposta
        
    mws.run_interaction(e1) # blocking

    mws.run_interaction(e2) # blocking

    





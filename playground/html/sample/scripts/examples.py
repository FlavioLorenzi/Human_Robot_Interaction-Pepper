import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')

from ws_client import *
import ws_client

# Definition of interaction functions

def e31():
    im.init()
    im.display.loadUrl('layout.html')

    time.sleep(2)

    # Setting HTML element of the web page
    im.executeModality('TEXT_title','HRI 2020')
    im.executeModality('TEXT_default','Hello!')
    im.executeModality('IMAGE','img/dolphin.jpg')

    # Using TTS service of the robot to speak
    im.executeModality('TTS','Congratulations for your first MODIM program')


def e32():

    im.executeModality('TEXT_default','Do you like animals?')

    # show buttons
    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

    # set ASR
    im.executeModality('ASR',['yes','no'])

    # wait for answer
    a = im.ask(actionname=None, timeout=15)

    if a=='timeout':
        s = "No answer"
    else:
        s = "Your answer has been: "+a

    # display reply
    im.executeModality('TEXT_default',s)


def e33():

    im.execute('a1')
    a = im.ask('a2')

    if a=='timeout':
        s = "No answer"
    else:
        s = "Your answer has been: "+a

    # display reply
    im.executeModality('TEXT_default',s)

    if a=='yes':
        r = im.askUntilCorrect('a3', timeout=15)
        im.executeModality('TEXT_default',r)


def e34():
    im.executeModality('TEXT_default','Do you want me to dance?')

    im.executeModality('ASR',['yes','no'])

    # wait for answer
    a = im.ask(actionname=None, timeout=15)

    if a=='yes':
        im.executeModality('TEXT_default','!!! Dancing !!!')
        im.robot.dance()
    else:
        im.executeModality('TEXT_default','OK. No dancing')

    time.sleep(2)
    im.executeModality('TEXT_default','Bye bye')


# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    # run interaction functions

    #mws.run_interaction(e31) # blocking

    #mws.run_interaction(e32) 

    mws.run_interaction(e33)

    mws.run_interaction(e34) 




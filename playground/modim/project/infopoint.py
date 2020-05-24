import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *



# Definition of interaction functions
#se rileva qualcuno nel range allora dice benvenuto con tablet e voce

def hellothere():
    im.init()
    im.robot.startSensorMonitor()

    sonar = im.robot.sensorvalue()
    frontsonar = sonar[1]
    print('Rilevo distanza di',frontsonar)

    if frontsonar >0.1 and frontsonar <3:


        im.display.loadUrl('layout.html')

        time.sleep(1)

        # Setting HTML element of the web page
        im.executeModality('TEXT_title','Hello there')
        im.executeModality('TEXT_default','Welcome to the Sacred Heart Hospital')

        im.executeModality('IMAGE','img/welcomeH.jpg')

        time.sleep(2)

        #gesture mancante #TODO saluto con il braccio

        # Using TTS service of the robot to SPEAK 
        im.executeModality('TTS','Hi I am Pepper and like my fellow doctors, I am here to help people')

        im.executeModality('TEXT_default','Hi I am Pepper and like my fellow doctors, I am here to help people')

        time.sleep(3)


#chiede se ti serve aiuto e reagisce di conseguenza

def infopoint():

    im.executeModality('TEXT_title','I am Pepper and I am here for you')

    im.executeModality('TEXT_default','Do you need some help?')
    im.executeModality('IMAGE','img/infopoint.jpg')
    im.executeModality('ASR',['yes','no'])
    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

    # wait for answer
    a = im.ask(actionname=None, timeout=10)

    if a=='yes':

        im.executeModality('TEXT_default','Ok, what do you need?')
        im.robot.say("Do you need general informations? Or are you looking for a patient?")
        im.executeModality('IMAGE','img/quest.gif')
        im.executeModality('BUTTONS',[['informations','Informations'],['patients','Patients'],['doctors','Doctors']])

        # wait for touching buttons
        b = im.ask(actionname=None, timeout=10)

        if b == 'informations':
            im.executeModality('IMAGE','img/hospital.jpg')

            im.executeModality('TEXT_default','Ground Floor : first aid')
            im.executeModality('TTS','Ground Floor : first aid ')
            time.sleep(2)
            im.executeModality('TEXT_default','First Floor : cardiology department')
            im.executeModality('TTS','First Floor : cardiology department ')
            time.sleep(2)
            im.executeModality('TEXT_default','Second Floor : urology department')
            im.executeModality('TTS','Second Floor : urology department ')
            time.sleep(2)
            im.executeModality('TEXT_default','Third Floor : psychiatry department')
            im.executeModality('TTS','Second Floor : urology department ')
            time.sleep(2)

            im.executeModality('TEXT_default','Thats all, thank you')
            im.executeModality('TTS','Thats all, thank you')
            

        if b == 'patients':
            im.executeModality('TEXT_default','Who are you looking for?')
            im.executeModality('TTS','Who are you looking for?')
            #im.executeModality('ASR',['yes','no'])
            im.executeModality('BUTTONS',[['flavio','Flavio'],['nicolo','Nicolo'],['josh','Josh']])
            im.executeModality('IMAGE','img/medrob.jpeg')

            # wait for patient name 
            c = im.ask(actionname=None, timeout=10)


            #capire come fare asr con nomi

            if c == 'flavio':

                im.executeModality('TEXT_default','Flavio is in psychiatry')    #digitare yes asr
                im.executeModality('TTS','Flavio bla bla ')
                time.sleep(2)

            if c == 'nicolo':

                im.executeModality('TEXT_default','Nicolo is in cardiology')    #digitare no asr
                im.executeModality('TTS','Nicolo bla bla ')
                time.sleep(2)

            if c == 'josh':

                im.executeModality('TEXT_default','Sorry but Josh is not our patient')    
                im.executeModality('TTS','josh bla bla ')
                time.sleep(2)

            im.executeModality('IMAGE','img/pepperr.jpg')

            im.executeModality('TEXT_default','Thats all, thank you')
            im.executeModality('TTS','Thats all, thank you')




        if b == 'doctors':
            im.executeModality('TEXT_default','Who are you looking for?')
            im.executeModality('TTS','Who are you looking for?')
            #im.executeModality('ASR',['yes','no'])
            im.executeModality('BUTTONS',[['burioni','Burioni'],['house','House']])
            im.executeModality('IMAGE','img/madrob.jpg')

            # wait for patient name 
            c = im.ask(actionname=None, timeout=10)

            if c == 'burioni':
                im.executeModality('TEXT_default','Covid is here, I am calling him')  
                im.executeModality('IMAGE','img/callhelp.png')  
                im.executeModality('TTS','josh bla bla ')
                time.sleep(3)

            if c == 'house':
                im.executeModality('TEXT_default','Thisi is not a tv show!')  
                im.executeModality('IMAGE','img/drhouse.jpg')  
                im.executeModality('TTS','josh bla bla ')
                time.sleep(3)



            im.executeModality('IMAGE','img/pepperr.jpg')
            im.executeModality('TEXT_default','Thats all, thank you')
            im.executeModality('TTS','Thats all, thank you')


        #TRANSPARENCY
        time.sleep(3)
        im.executeModality('TEXT_title','Aah, just a question')
        im.executeModality('TEXT_default','Sorry, are you satisfied with this informations?')
        im.executeModality('TTS','Are you satisfied with this informations?')
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

        d = im.ask(actionname=None, timeout=10)

        if d == 'yes':
            im.executeModality('TEXT_default','Thanks, I do my best')
        if d == 'no':
            im.executeModality('TEXT_default','What else you need?')


    if a == 'no':
        im.executeModality('IMAGE','img/pepperr.jpg')
        im.executeModality('TEXT_default','OK. Have a nice day')
        im.executeModality('TTS','I will be around here')


    time.sleep(2)
    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Bye bye, happy to help you')
    im.executeModality('TTS','Bye bye, happy to help you')

# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    #time = True

    #while(time):
    #trovare il modo per rimandare in loop questi metodi, solo se l'utente vuole altre info
    #in TRansparency section magari si pu fare qualcosa
        
    mws.run_interaction(hellothere) # blocking

    

    mws.run_interaction(infopoint) # blocking

    





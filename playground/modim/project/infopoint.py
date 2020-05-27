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
    print('Rilevo distanza di',frontsonar)      #qui aggiungere il face recognition per ''non parlare con i muri'' TODO

    if frontsonar >0.1 and frontsonar <3:


        im.display.loadUrl('layout.html')

        time.sleep(1)

        # Setting HTML element of the web page
        im.executeModality('TEXT_title','Hello there')
        im.executeModality('TEXT_default','Welcome to the Sacred Heart Hospital')
        im.executeModality('TTS','Welcome to the Sacred Heart Hospital')
        im.executeModality('IMAGE','img/welcomeH.jpg')
     
        im.robot.raiseArm('R')

        time.sleep(3)

        im.robot.normalPosture()

        # Using TTS service of the robot to SPEAK 
        im.executeModality('TTS','I am Pepper and like my fellow doctors, I am here to help people')

        im.executeModality('TEXT_default','I am Pepper and like my fellow doctors, I am here to help people')

        time.sleep(3)


#chiede se ti serve aiuto e reagisce di conseguenza

def infopoint():
    t = True

    while(t):

        #funzioni base modim usate sempre in questo script, quasi tutte

        im.executeModality('TEXT_title','I am Pepper and I am here for you')    #frase importante su tablet
        im.executeModality('TTS','Do you need some help?')                      #parlare
        im.executeModality('TEXT_default','Do you need some help?')             #frasi sul tablet
        im.executeModality('IMAGE','img/infopoint.jpg')                         #img centrale
        #due modi per rispondere:
        im.executeModality('ASR',['yes','no'])
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

        # wait for answer
        a = im.ask(actionname=None, timeout=10)

        if a=='yes':

            im.executeModality('TEXT_default','Ok, what do you need?')
            #credo che la voce funziona anche cosi, con questa pepper tool implementation: non per forza con im.exe(TTS)
            im.robot.say("Do you need general informations? Or are you looking for a patient?")
            im.executeModality('IMAGE','img/quest.gif')
            im.executeModality('BUTTONS',[['informations','General informations about hospital'],['patients','Look for a patient'],['doctors','Look for a doctor'],['fun','Fun with me'],['pepepr','About me']])

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

                #names are not on button for privacy reasons
                #im.executeModality('BUTTONS',[['flavio','Flavio'],['nicolo','Nicolo'],['jack','Jack']])

                im.executeModality('ASR',['flavio','nicolo','jack'])
                im.executeModality('IMAGE','img/medrob.jpeg')

                # wait for patient name 
                c = im.ask(actionname=None, timeout=10)

                #NB: nel nostro caso non importa, ma in genere pepper usa lo speech recognition sistem di google senza traduzione ita eng
                # che signifa che i nomi in italiano possono non essere ben interpretati dal robot
                

                if c == 'flavio':

                    #Enter password for flavio   #privacy NICO TODO! ! !

                    im.executeModality('TEXT_default','Flavio is in psychiatry')    
                    im.executeModality('TTS','Flavio bla bla ')
                    time.sleep(2)

                if c == 'nicolo':

                    #Enter password for  Nicolo

                    im.executeModality('TEXT_default','Nicolo is in cardiology')   
                    im.executeModality('TTS','Nicolo bla bla ')
                    time.sleep(2)

                if c == 'jack':

                    im.executeModality('TEXT_default','Sorry but Jack is not our patient')    
                    im.executeModality('TTS','josh bla bla ')
                    time.sleep(2)


                im.executeModality('IMAGE','img/pepperr.jpg')

                im.executeModality('TEXT_default','Thats all, thank you')
                im.executeModality('TTS','Thats all, thank you')




            if b == 'doctors':
                im.executeModality('TEXT_default','Who are you looking for?')
                im.executeModality('TTS','Who are you looking for?')
                #im.executeModality('ASR',['yes','no'])
                im.executeModality('BUTTONS',[['doctor burioni','Doctor Burioni'],['doctor house','Doctor House'],['doctor dolittle','Doctor Dolittle']])
                im.executeModality('IMAGE','img/madrob.jpg')

                # wait for patient name 
                c = im.ask(actionname=None, timeout=10)

                if c == 'doctor burioni':
                    im.executeModality('TEXT_default','Wait here, I am calling him right away')  
                    im.executeModality('IMAGE','img/callhelp.png')  
                    im.executeModality('TTS','josh bla bla ')
                    time.sleep(3)

                if c == 'doctor house':
                    im.executeModality('TEXT_default','This is not a tv show!')  
                    im.executeModality('IMAGE','img/drhouse.jpg')  
                    im.executeModality('TTS','josh bla bla ')
                    time.sleep(3)

                if c == 'doctor dolittle':
                    im.executeModality('TEXT_default','Do you talk with animals? Maybe you are not well, I ll call him right now')  
                    im.executeModality('IMAGE','img/callhelp.png')  
                    im.executeModality('TTS','josh bla bla ')
                    time.sleep(3)


                im.executeModality('IMAGE','img/pepperr.jpg')
                im.executeModality('TEXT_default','Thats all, thank you')
                im.executeModality('TTS','Thats all, thank you')



            #GAME TODO

            if b == 'fun':
                #todo ciclo while(g == True) che mi chiede al game over se voglio giocare ancora (if no allora g == False )

                t = True #vai direttamente ai saluti appena finisci il quiz

                im.executeModality('TEXT_default','Are you boring? Lets do a quiz ;)')  #mettere link con uno o piu giochi
                im.executeModality('TTS','Are you boring? Lets do a quiz')
                im.executeModality('IMAGE','img/quiz.jpg')
                time.sleep(2)
                im.executeModality('TEXT_default','Frist question:')
                im.executeModality('BUTTONS',[['yes','Todo'],['no','Todo2']])
                

                # wait for answer
                #c = im.ask(actionname=None, timeout=10)
                '''
                if c == '':
                    im.executeModality('TEXT_default','bla')  
                    im.executeModality('TTS','bla bla ')
                    time.sleep(3)
                '''
                im.executeModality('TEXT_default','GAME OVER : Wanna play again?')
                im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                g = False

                #if no --> g = True


            #Other informations
            if b == 'pepper':

                im.executeModality('TEXT_default','I am Pepper, a... ')
                im.executeModality('TEXT_title','Here can you read my story')
                im.executeModality('TTS','Here can you read my story')
                im.executeModality('IMAGE','img/softbank.jpg')
                time.sleep(2)
                #TODO

            

            #TRANSPARENCY
            time.sleep(3)
            im.executeModality('TEXT_title','Aah, just a question')
            im.executeModality('TEXT_default','Sorry, are you satisfied with this informations?')
            im.executeModality('TTS','Are you satisfied with this informations?')
            im.executeModality('IMAGE','img/robot.gif')
            im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

            d = im.ask(actionname=None, timeout=10)

            if d == 'yes':
                im.executeModality('TEXT_default','Thanks, I do my best')
                t = False
            if d == 'no':
                im.executeModality('TEXT_default','Keep calm, my knowledge is at your disposal')
                time.sleep(3)


        if a == 'no':
            t = False
            im.executeModality('IMAGE','img/pepperr.jpg')
            im.executeModality('TEXT_default','OK. Have a nice day')
            im.executeModality('TTS','I will be around here')


    time.sleep(2)
    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Bye bye, happy to help you')
    im.executeModality('TTS','Bye bye, happy to help you')


def questionnaire():

    time.sleep(1)

    # Setting HTML element of the web page for the questionnaire
    im.executeModality('IMAGE','img/que.gif')
    im.executeModality('TEXT_title','Could you help me to improve myself?')
    im.executeModality('TEXT_default','Can I ask you a favor? It will take a few minutes...')
    im.executeModality('TTS','Can I ask you a favor? It will take a few minutes...')


    time.sleep(2)

    #gesture mancante #TODO indicare il tablet con il braccio

    # Using TTS service of the robot to SPEAK 
    im.executeModality('TEXT_title','Please, fill in a short questionnaire about me')
    im.executeModality('TTS','To improve my behaviour with people, I need an evaluation')
    im.executeModality('TEXT_default','To improve my behaviour with people, I need your evaluation')

    time.sleep(3)
    
    im.executeModality('TTS','Choose between this range: One means LITTLE, Five means A LOT')
    im.executeModality('TEXT_default','Choose between this range: 1 means LITTLE, 5 means A LOT')

    time.sleep(3)

    im.executeModality('TTS','How comfortable did you feel?')
    im.executeModality('TEXT_default','How comfortable did you feel?')
    im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])

    time.sleep(3)
    
    im.executeModality('TTS','Did I seem friendly to you?')
    im.executeModality('TEXT_default','Did I seem friendly to you?')
    im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])

    time.sleep(3)

    im.executeModality('TTS','Did I seem rielable to you?')
    im.executeModality('TEXT_default','Did I seem rielable to you?')
    im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])

    time.sleep(3)

    im.executeModality('TTS','So, how much you trust me?')
    im.executeModality('TEXT_default','So, how much you trust me? ')
    im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])





    #TODO

# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    mws.run_interaction(hellothere) # blocking

    mws.run_interaction(infopoint) # blocking

    #mws.run_interaction(questionnaire) #blocking

    





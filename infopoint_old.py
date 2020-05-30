import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *



######################################################
# LAYOUT PAGES, PATIENTS (PSW), LAYOUT QUESTIONNAIRE #
######################################################

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
        DATABASE_DICT = {"flavio":"urology","nicolo":"psychiatry","gabriele":"cardiology","roberto":"urology","john":"psychiatry","jack":"cardiology","murphy":"psychiatry"}
        DATABASE = ["flavio","gabriele","nicolo"]

        DATABASE__DICT_PSW = {"flavio":"FL95","nicolo":"NM95","gabriele":"GN95","roberto":"urology","john":"psychiatry","jack":"cardiology","murphy":"psychiatry"}
        DATABASE_PSW = ["FL95","NM95","GN95"]

        #t = True   
        #funzioni base modim usate sempre in questo script, quasi tutte

        im.executeModality('TEXT_title','I am Pepper and I am here for you')    #frase importante su tablet
        im.executeModality('TTS','Do you need some help?')                      #parlare
        im.executeModality('TEXT_default','Do you need some help?')             #frasi sul tablet
        im.executeModality('IMAGE','img/infopoint.jpg')                         #img centrale
        #due modi per rispondere:
        im.executeModality('ASR',['yes','no'])
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        # wait for answer
        a = im.ask(actionname=None, timeout=20)

        if a=='yes':

            im.executeModality('TEXT_default','Ok, what do you need?')
            im.executeModality('IMAGE','img/quest.gif')
            im.executeModality('BUTTONS',[['informations','General informations about hospital'],['patients','Look for a patient'],['doctors','Look for a doctor'],['fun','Fun with me'],['pepper','About me']])

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
                im.executeModality('TTS','Second Floor : psychiatry department ')
                time.sleep(2)

                im.executeModality('TEXT_default','Thats all, thank you')
                im.executeModality('TTS','Thats all, thank you')
                

            if b == 'patients':
                
                loop = True
                #____TODO: 
                #It would be perfect if the robot will look at the face of the person detected
                #but  unfortunately we have no real people.
                im.executeModality('IMAGE','img/medrob.jpeg')
                im.executeModality('TEXT_default','You decided to visit somebody then. It would be for sure a pleasure for him!')
                time.sleep(5)
                #im.executeModality('TTS','You decided to visit somebody then. It would be for sure a pleasure for him.')
                
                    
                while loop:
                    im.executeModality('IMAGE','img/medrob.jpeg')
                    im.executeModality('TEXT_default','Can you please tell me his or her full name?')
                    im.executeModality('ASR',DATABASE)
                    name_person = im.ask(actionname=None, timeout=10)                   
                    
                    if name_person != 'timeout':                                                  
                        ##############################################################
                        ####  Just another check to be sure about che correctness ####
                        ##############################################################
                            
                        im.executeModality('TEXT_default','Are you looking for '+name_person.upper()+'. Is it correct?')
                        #im.executeModality('TTS','Are you looking for'+name_person+'. Is it correct?')
                        im.executeModality('ASR',{'correct':['yes','si'], 'wrong':['no','not','not at all']})
                        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                        correct_answer = im.ask(actionname=None, timeout=10)
                          
                        if (correct_answer == 'yes') and (name_person in DATABASE_DICT):
                            
                            #_______ In order to see people, there is a PASSWORD given for each person in the hospital (PRIVACY ISSUES)________#
                            while True:
                                im.executeModality('IMAGE','img/medrob.jpeg')
                                im.executeModality('TEXT_default','Actually I can tell you the room only if you know the PASSWORD')
                                time.sleep(5)
                                im.executeModality('TEXT_default','I\'m sorry for this issue but we have added a new safety protocol. What\'s the PSW?')
                                im.executeModality('ASR',DATABASE_PSW)
                                psw = im.ask(actionname=None,timeout=15)

                                if psw in DATABASE_PSW:
                                    where_is = DATABASE_DICT[name_person] 
                                    im.executeModality('TEXT_default','It\'s the correct one! '+name_person.upper()+' is in '+where_is)
                                    time.sleep(7)
                                    im.executeModality('TEXT_default','Do you need to know other patient\'s location?')
                                    #im.executeModality('TTS','Do you need to know other patient\'s location?')
                                    im.executeModality('ASR',{'correct':['yes','si'], 'wrong':['no','not']})
                                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                                    answer = im.ask(actionname=None,timeout=15)
                                    if answer=='yes':
                                        break
                                    else:
                                        im.executeModality('TEXT_default','I hope I have been of help')
                                        loop = False
                                        break
                                else:
                                    im.executeModality('IMAGE','img/x.png')        
                                    im.executeModality('TEXT_default','The PASSWORD that you\'ve inserted is wrong. HINT: THe PSW is case sensitive. Do you want to try it again?')
                                    #im.executeModality('ASR',{'correct':['yes','si'], 'wrong':['no','not']})
                                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                                    again = im.ask(actionname=None,timeout=15)
                                    if again=='yes':
                                        continue
                                    else:
                                        loop = False
                                        break



                            
                        elif (correct_answer == 'yes') and not (name_person in DATABASE_DICT):
                            im.executeModality('IMAGE','img/x.png')
                            #im.executeModality('TTS','I\'m sorry but the person you\'re looking for is not in this hospital')
                            im.executeModality('TEXT_default','I\'m sorry but the person you\'re looking for is not in this hospital')
                            time.sleep(5)
                            break    

                        # Here PEPPER misunderstood the name of the person
                        else:
                            time.sleep(5)
                            im.executeModality('TEXT_default','I apologize sorry for the misunderstanding')
                            #im.executeModality('TTS','I\'m sorry for the misunderstanding')
                            continue
                                
                    else:
                        im.executeModality('IMAGE','img/x.png')
                        #im.executeModality('TTS','I\'m sorry but the person you\'re looking for is not in this hospital')
                        im.executeModality('TEXT_default','I\'m sorry but the person you\'re looking for is not in this hospital')
                        time.sleep(5)
                        im.executeModality('TEXT_default','Can I help you anyway?')
                        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                        answer = im.ask(actionname=None,timeout=15)
                        if answer=='yes':
                            continue
                        else:
                            break

                


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

                im.executeModality('TEXT_title','Here you can read my story  ')
                im.executeModality('TEXT_default','I am Pepper, one of the first social humanoid robots able to recognize faces and basic human emotions. I am optimized for human interactions and to engage with people through conversations and my touch screen')
                im.executeModality('TTS','Here can you read my story')
                im.executeModality('IMAGE','img/softbank.jpg')
                time.sleep(4)

                im.executeModality('TEXT_default','In this hospital I have several important roles: for example in this area I try to clarify every doubt of people, playing an info point role ')


                time.sleep(4)
                im.executeModality('TEXT_default','Did you like my story?')


            

            #TRANSPARENCY
            time.sleep(5)
            im.executeModality('TEXT_title','Aah, just a question')
            im.executeModality('TEXT_default','Sorry, are you satisfied with this informations?')
            im.executeModality('TTS','Are you satisfied with this informations?')
            im.executeModality('IMAGE','img/robot.gif')
            im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
            d = im.ask(actionname=None, timeout=10)
            if d == 'yes':
                im.executeModality('TEXT_default','Thanks, I do my best')
                
            if d == 'no':
                im.executeModality('TEXT_default','Keep calm, my knowledge is at your disposal')
                time.sleep(3)


        else:
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

        
    #mws.run_interaction(hellothere) # blocking

    mws.run_interaction(infopoint) # blocking

    #mws.run_interaction(questionnaire) #blocking

    





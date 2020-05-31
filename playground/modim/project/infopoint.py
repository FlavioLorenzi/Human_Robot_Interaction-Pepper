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

        time.sleep(2)

        #im.robot.normalPosture()

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
            im.executeModality('BUTTONS',[['informations','General informations about hospital'],['patients','Look for a patient'],['doctors','Look for a doctor'],['fun','Fun with me'],['pepper','About me']])

            # wait for touching buttons
            b = im.ask(actionname=None, timeout=10)



            #General info about hospital
            if b == 'informations':
                im.executeModality('IMAGE','img/hospital.jpg')

                im.executeModality('TEXT_default','Ground Floor : First aid ')
                im.executeModality('TTS','Ground Floor : first aid ')
                time.sleep(2)
                im.executeModality('TEXT_default','First Floor : Cardiology department')
                im.executeModality('TTS','First Floor : cardiology department ')
                time.sleep(2)
                im.executeModality('TEXT_default','Second Floor : Urology department')
                im.executeModality('TTS','Second Floor : urology department ')
                time.sleep(2)
                im.executeModality('TEXT_default','Third Floor : Psychiatry department')
                im.executeModality('TTS','Third Floor : Psychiatry department ')
                time.sleep(2)
                im.executeModality('TEXT_default','Fourth Floor : Blood test withdrawal')
                im.executeModality('TTS','Fourth Floor : Blood test withdrawal ')
                time.sleep(2)
                im.executeModality('IMAGE','img/tips.jpg')
                im.executeModality('TEXT_default','Remember some useful tips to deal with this particular period')
                im.executeModality('TTS','Pay attention')
                time.sleep(5)

                im.executeModality('TEXT_default','Thats all, thank you')
                im.executeModality('TTS','Thats all, thank you')
  



            #sezione pazienti 
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



            #sezione in cui puoi chiedere di 3 dottori in particolare, ma uno non fa parte dello stuff!
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
                    im.executeModality('TTS','How do you feel? ')
                    time.sleep(3)

                if c == 'doctor house':
                    im.executeModality('TEXT_default','This is not a tv show!')  
                    im.executeModality('IMAGE','img/drhouse.jpg')  
                    im.executeModality('TTS','Go away please ')
                    time.sleep(3)

                if c == 'doctor dolittle':
                    im.executeModality('TEXT_default','Do you talk with animals? Maybe you are not well, I ll call him right now')  
                    im.executeModality('IMAGE','img/callhelp.png')  
                    im.executeModality('TTS','How do you feel? ')
                    time.sleep(3)


                im.executeModality('IMAGE','img/pepperr.jpg')
                im.executeModality('TEXT_default','Thats all, thank you')
                im.executeModality('TTS','Thats all, thank you')



            #GAME 
            #breve quiz di tre domande: se le indovini tutte e tre esce fuori la scritta sei un master
            #inoltre in questo caso ti chiede se vuoi una foto per immortalare il momento: rispondere con asr

            if b == 'fun':
                
                g = True
                im.executeModality('TEXT_default','Are you boring? Lets do a quiz ;)')  
                im.executeModality('TTS','Are you boring? Lets do a quiz')

                while(g):

                    im.executeModality('TEXT_title','Pepper Quiz') 
                    im.executeModality('TEXT_default','Initializing . . .') 
                    im.executeModality('IMAGE','img/quiz.jpg') 
                    time.sleep(2)
                                      
                    score = 0
                    im.executeModality('IMAGE','img/berlin.png')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about history')
                    #write on the tablet
                    im.executeModality('TEXT_default','In which year the Berlin Wall fall?')
                    im.executeModality('BUTTONS',[['1989','1989'],['1999','1999'],['1960','1960']])
                
                    c = im.ask(actionname=None, timeout=15)
                    if c=='1989':
                        im.executeModality('TEXT_default','Very good')
                        score = score +1
                    else:
                        im.executeModality('TEXT_default','Not good')

                    time.sleep(3)

                    im.executeModality('IMAGE','img/serieA.png')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about sport')
                    #write on the tablet        
                    im.executeModality('TEXT_default','Which team won serie A in 2001?')
                    im.executeModality('BUTTONS',[['roma','Roma'],['lazio','Lazio'],['juve','Juve']])

                    d = im.ask(actionname=None, timeout=15)

                    if d == 'roma':
                        im.executeModality('TEXT_default','Very good')
                        score = score +1
                    else:
                        im.executeModality('TEXT_default','Not good')
                        

                    time.sleep(3)

                    im.executeModality('IMAGE','img/pinkfloyd.jpg')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about music')
                    #write on the tablet
                    im.executeModality('TEXT_default','How many members did pinkfloyd have?')
                    im.executeModality('BUTTONS',[['4','4'],['5','5'],['3','3']])

                    e = im.ask(actionname=None, timeout=10)
                    if e=='4':
                        im.executeModality('TEXT_default','Very good')
                        score = score +1
                    else:
                        im.executeModality('TEXT_default','Not good')         

                    time.sleep(2)

                    #final score
                    if score == 3:
                        im.executeModality('IMAGE','img/master.jpg')
                        im.executeModality('TEXT_default','You are a master')
                        time.sleep(3)
                        im.robot.say("Lets shoot a picture to the champion, ok?:")
                        im.executeModality('ASR',['ok','no'])
                        f = im.ask(actionname=None, timeout=15)

                        if f == 'ok pepper':
                            im.executeModality('TEXT_default','Taking the picture, say cheese')
                            im.robot.say("Say cheeeeese")
                            time.sleep(3)
                            im.robot.takephoto()

                    else:
                        im.executeModality('IMAGE','img/sad.png')
                        im.executeModality('TEXT_default','You have to improve yourself')
                        time.sleep(3)
                    

                    im.executeModality('TEXT_default','GAME OVER: Play again?')
                    im.executeModality('IMAGE','img/gameover.jpg')
                    time.sleep(3)
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                    

                    c = im.ask(actionname=None, timeout=10)

                    if c == 'yes':
                        g = True
                        im.executeModality('TEXT_default','Ok, restart the game')
                        time.sleep(3)

                    if c == 'no':
                        g = False
                        im.executeModality('TEXT_default','Exit . . .')
                        time.sleep(3)
                        t = False #vai direttamente ai saluti appena finisci il quiz
                        
                    



            #Basic informations about Pepper
            if b == 'pepper':

                im.executeModality('TEXT_title','Here you can read my story  ')
                im.executeModality('TEXT_default','I am Pepper, one of the first social humanoid robots able to recognize faces and basic human emotions. I am optimized for human interactions and to engage with people through conversations and my touch screen')
                im.executeModality('TTS','Here can you read my story')
                im.executeModality('IMAGE','img/softbank.jpg')
                time.sleep(8)
                im.executeModality('TEXT_default','In this hospital I have several important roles: for example in this area I try to clarify every doubt of people, playing an info point role. I can be very useful, I know a lot of things')
                time.sleep(10)
                im.executeModality('TEXT_default','Then, during the night I am also on the first floor, where I am employed as assistant and supervisor for patients: I can call the medical stuff if there is some problem')
                time.sleep(10)

                im.executeModality('TEXT_default','Other informations about me and my usage in healtcare environment??')
                im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

                c = im.ask(actionname=None, timeout=10)

                if c == 'yes':
                    im.executeModality('TEXT_default',' Ok, I am glad to show you')
                    time.sleep(4)
                    im.executeModality('IMAGE','img/healtcare.png')
                    im.executeModality('TEXT_default',' In this particular period softbank robotics has started a Covid-19 initiative to support hospitals and clinics ')
                    time.sleep(15)
                    im.executeModality('TEXT_default',' Do you want more informations? Visit our site, but then I will need a restart')
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

                    d = im.ask(actionname=None, timeout=10)

                    if d == 'yes':

                        im.display.loadUrl('site.html')     #lo lasciamo? se vai su un altra pagina non torni indietro
                        time.sleep(10)
                        break
                       
                    if d == 'no':
                        im.executeModality('TEXT_default','Ok, I am always here, if you want')            


                if c == 'no':
                    im.executeModality('TEXT_default','Ok, I am always here, if you want')

            

            #TRANSPARENCY section: alla fine di ogni pulsante dell info point chiede se sei soddisfatto: se no return
            if t == True:

                time.sleep(3)
                im.executeModality('TEXT_title','Just a question')
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




        #do you need help? NO
        if a == 'no':
            t = False
            im.executeModality('IMAGE','img/pepperr.jpg')
            im.executeModality('TEXT_default','OK. Have a nice day')
            im.executeModality('TTS','I will be around here')


    #saluti finali
    time.sleep(2)
    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Bye bye, happy to help you')
    im.executeModality('TTS','Bye bye, happy to help you')

def questionnaire():

    #TODO NEW LOAD URL HTML PAGE ___ 
    # bottoni diversi, magari con numeri grandi
    # ecc...




    time.sleep(2)

    # Setting HTML element of the web page for the questionnaire
    im.robot.bip(1)
    im.robot.blue_eyes()
    im.executeModality('IMAGE','img/que.gif')
    im.executeModality('TEXT_title','Could you help me to improve myself?')
    im.executeModality('TEXT_default','Can I ask you a favor? It will take a few minutes...')
    im.executeModality('TTS','Can I ask you a favor? It will take a few minutes...')

    time.sleep(2)


    

    # Using TTS service of the robot to SPEAK 
    im.executeModality('TEXT_title','Please, fill in a short questionnaire about me')
    im.executeModality('TTS','To improve my behaviour with people, I need an evaluation')
    im.executeModality('TEXT_default','To improve my behaviour with people, I need your evaluation')

    time.sleep(3)
    im.executeModality('TEXT_default','Click Ok to accept')
    im.executeModality('BUTTONS',[['ok','Ok'],['no','Maybe later']])

    a = im.ask(actionname=None, timeout=10)

    if a == 'ok':

        im.robot.green_eyes()
        #im.robot.headPose(0,25,0) #il robot abbassa la testa verso il tablet

        time.sleep(1)
        
        im.executeModality('TTS','Choose in this range: One means LITTLE, Five means A LOT')
        im.executeModality('TEXT_default','Choose in this range: 1 means LITTLE, 5 means A LOT')

        time.sleep(3)

        judge = 0 #giudizio persona

        im.executeModality('TTS','How comfortable did you feel?')
        im.executeModality('TEXT_default','How comfortable did you feel?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        b = im.ask(actionname=None, timeout=10)
        if b == '1':
            judge =judge-2
        if b == '3' or b == '4':           
            judge =judge+ 1
        if b == '5':
            judge =judge+ 2

        time.sleep(3)
        
        im.executeModality('TTS','Did I seem friendly to you?')
        im.executeModality('TEXT_default','Did I seem friendly to you?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        c = im.ask(actionname=None, timeout=10)
        if c == '1':
            judge =judge-2
        if c == '3' or c == '4':           
            judge =judge+ 1
        if c == '5':
            judge =judge+ 2

        time.sleep(3)

        im.executeModality('TTS','Did I seem enough rielable?')
        im.executeModality('TEXT_default','Did I seem rielable to you?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        d = im.ask(actionname=None, timeout=10)
        if d == '1':
            judge =judge-2
        if d == '3' or d == '4':           
            judge =judge+ 1
        if d == '5':
            judge =judge+ 2

        time.sleep(3)

        im.executeModality('TTS','So, how much you trust me?')
        im.executeModality('TEXT_default','So, how much you trust me? ')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        e = im.ask(actionname=None, timeout=10)
        if e == '1':
            judge =judge-2
        if e == '3' or e == '4':           
            judge =judge+ 1
        if e == '5':
            judge =judge+ 2

        time.sleep(3)

        im.executeModality('TTS','Would you recommend me to others?')
        im.executeModality('TEXT_default','Would you recommend me to others?')
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        f = im.ask(actionname=None, timeout=10)
        if f == 'yes':
            judge =judge+ 2
        if f == 'no':
            judge =judge- 2

        

        if judge > 5:
            im.executeModality('TEXT_title','Your opinion is important')
            im.executeModality('IMAGE','img/happy.jpg')         
            im.executeModality('TTS','Your judgment was positive, thank you')
            im.executeModality('TEXT_default','Your judgment was positive, thank you')
            time.sleep(3)
        if judge < 5:
            im.executeModality('IMAGE','img/rocky.jpg')
            im.executeModality('TTS','Your judgment was not good, I will improve myself, I promise')
            im.executeModality('TEXT_default','Your judgment was not good... I will improve myself, I promise')
            time.sleep(3)
    


    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Bye bye, I hope to see you soon')
    im.executeModality('TTS','Bye bye')




    

# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    #mws.run_interaction(hellothere) # blocking

    #mws.run_interaction(infopoint) # blocking

    mws.run_interaction(questionnaire) #blocking

    





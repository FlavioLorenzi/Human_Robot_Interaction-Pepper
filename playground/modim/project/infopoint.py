import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *

# Definition of interaction functions
# If someone is in the range, he's welcomed by a predefined action

def hellothere():
    im.init()
    im.display.loadUrl('layout_infopoint.html')
    im.robot.startSensorMonitor()

    sensors = im.robot.sensorvalue()
    frontSonar = sensors[1]
    rearSonar = sensors[2]
    headTouch = sensors[3]

    if (frontSonar > 0.1 and frontSonar < 3) or (rearSonar > 0.1 and rearSonar < 3) or headTouch:


        #im.display.loadUrl('layout_infopoint.html')

        time.sleep(1)

        # Perform action
        im.execute('welcome')   #hello, welcome to the hospital with Eih gesture

        time.sleep(3)

        # Using TTS service of the robot to SPEAK 
        im.executeModality('TTS','I am Pepper and like my fellow doctors, I am here to help people')

        im.executeModality('TEXT_default','I am Pepper and like my fellow doctors, I am here to help people')

        time.sleep(3)



def infopoint():
    DATABASE_WHERE = {"lorenzi":"urology","mantovani":"psychiatry","nicosanti":"cardiology","roberto":"urology","john":"psychiatry","jack":"cardiology","murphy":"psychiatry"}
    DATABASE_GET_TO_PLACE = {"urology":"If you don't know how to get urology pavillion, just get out of where you entered. Then turn left and on the left you will se a big blue building. That building is urology.",
                             "psychiatry":"If you don't know how to get psychiatry,  just get out of where you entered. Then turn right and you will see it in front of you. It's a red building.",
                             "cardiology":"If you don't know how to get cardiology pavillion, just get out of where you entered. Then turn left and walk until you can turn left again. You will see cardiology in front of you. It's a yellow building.",
    }

    DATABASE_SURNAME = ["lorenzi","nicosanti","mantovani"]
    DATABASE_SURNAME_NAME = {"lorenzi":'Flavio', "mantovani":"Nicolo", "nicosanti":"Gabriele"}

    DATABASE_PSW = ["nm95","fl95","gn95"]

    t = True

    while(t):

        im.executeModality('TEXT_title','I am Pepper and I am here for you')    
        im.executeModality('TTS','Do you need some help?')                      
        im.executeModality('TEXT_default','Do you need some help?')             
        im.executeModality('IMAGE','img/infopoint.jpg')                         
        im.executeModality('ASR',['yes','no'])
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        a = im.ask(actionname=None, timeout=40)

        # If the sensed person need some kind of help
        if a=='yes':

            im.executeModality('TEXT_default','Ok, what do you need?')
            im.robot.say("Do you need general informations? Or are you looking for a patient?")
            im.executeModality('IMAGE','img/quest.gif')
            im.executeModality('BUTTONS',[['patients','Look for a patient'],['doctors','Look for a doctor'],['fun','Fun with me'],['pepper','About me'],['hospital_info','About hospital']])
            b = im.ask(actionname=None, timeout=40)

            ###################################
            #   General info about hospital   #
            ##################################
            if b == 'hospital_info':
                while True:
                    im.executeModality('IMAGE','img/hospital_2_modified.jpg')
                    im.executeModality('TEXT_default','You are in the offices (the red point). The offices are near the entrance.')
                    im.robot.say("You are in the offices (the red point). The offices are near the entrance.")
                    time.sleep(10)
                    im.executeModality('TEXT_default','Violet pavillion: First aid \n First pavillion (green): ostetrics \n Second pavillion (blue): urology \n Third pavillion (yellow): cardiology \n Specialty pavillion (orange): specialities \n Central clinics (red): psychiatry')
                    im.robot.say('Violet pavillion: First aid \n First pavillion (green): ostetrics \n Second pavillion (blue): urology \n Third pavillion (yellow): cardiology \n Specialty pavillion (orange): specialities \n Central clinics (red): psychiatry')
                    time.sleep(30)
                    im.executeModality('IMAGE','img/tips.jpg')
                    im.executeModality('TEXT_default','Remember some useful tips to deal with this particular period')
                    im.executeModality('TTS','Pay attention')
                    time.sleep(5)

                    im.executeModality('TEXT_default','Do you want to see again the infos about the hospital?')
                    im.robot.say('Wanna see again the informations?')
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                    answer = im.ask(actionname=None,timeout=40)
                    if answer=='yes':
                        continue
                    else:
                        break

            #############################
            #   Looking for a patient   #
            #############################
            elif b == 'patients':
                loop = True
                im.executeModality('IMAGE','img/medrob.jpeg')
                im.executeModality('TEXT_default','You decided to visit somebody then. It would be for sure a pleasure for him!')
                im.robot.say('You decided to visit somebody then')
                time.sleep(5)              
                    
                while loop:
                    im.executeModality('IMAGE','img/medrob.jpeg')
                    im.executeModality('TEXT_default','Can you please tell me his or her surname?')
                    im.executeModality('TTS','Can you please tell me his or her surname?')
                    im.executeModality("ASR",DATABASE_SURNAME)
                    name_person = im.ask(actionname=None, timeout=15)                   

                    ###################################################################################
                    # NB: When we insert a name that is not recognized by the ASR, even if the name   #
                    # is different from 'timeout' the statement will go in the 'else' branch.         #
                    ###################################################################################

                    if name_person != 'timeout':                                                  
                        
                        # Here there is another check, even if it may be redundant: it enters here ONLY when a word 
                        # present in the vocabulary DATABASE_SURNAME is recognized, otherwise goes in the else branch.
                        im.executeModality('TEXT_default','Are you looking for '+ DATABASE_SURNAME_NAME[name_person].upper() +' '+ name_person.upper()+'. Is it correct?')
                        im.executeModality('ASR',{'correct':['yes','si'], 'wrong':['no','not','not at all']})
                        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                        correct_answer = im.ask(actionname=None, timeout=40)
                          
                        if (correct_answer == 'yes') and (name_person in DATABASE_SURNAME):
                            
                            #_______ In order to see people, there is a PASSWORD given for each person in the hospital (PRIVACY ISSUES)________#
                            while True:
                                im.executeModality('IMAGE','img/medrob.jpeg')
                                im.executeModality('TEXT_default','Actually I can tell you the room only if you know the PASSWORD')
                                im.executeModality('TTS','Actually I can tell you the room only if you know the PASSWORD')
                                time.sleep(5)
                                im.executeModality('TTS','we have a new safety protocol')
                                im.executeModality('TEXT_default','I\'m sorry for this issue but we have added a new safety protocol. What\'s the PSW?')
                                im.executeModality('ASR',DATABASE_PSW)
                                psw = im.ask(actionname=None,timeout=15)


                                # The PASSWORD is recognized by Pepper, and thus the location of the patient can be known.
                                if psw != 'timeout':
                                    where_is = DATABASE_WHERE[name_person] 
                                    im.executeModality('TEXT_default','It\'s the correct one! '+ DATABASE_SURNAME_NAME[name_person].upper() +' '+name_person.upper()+' is in '+ where_is)
                                    time.sleep(7)
                                    im.executeModality('TEXT_default',''+ DATABASE_GET_TO_PLACE[where_is])
                                    time.sleep(20)
                                    im.executeModality('TEXT_default','Do you need to know other patient\'s location?')
                                    im.executeModality('TTS','Do you need to know other patient\'s location?')
                                    im.executeModality('ASR',{'correct':['yes','si'], 'wrong':['no','not']})
                                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                                    answer = im.ask(actionname=None,timeout=45)
                                    if answer=='yes':
                                        break
                                    else:
                                        im.executeModality('TEXT_default','I hope I have been of help')
                                        im.executeModality('TTS','I hope I have been of help')
                                        loop = False
                                        break

                                # The password here is wrong.
                                else:
                                    im.executeModality('IMAGE','img/x.png')        
                                    im.executeModality('TEXT_default','The PASSWORD that you\'ve inserted is wrong. Do you want to try it again?')
                                    im.executeModality('TTS','The PASSWORD is wrong')
                                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                                    again = im.ask(actionname=None,timeout=15)
                                    if again=='yes':
                                        continue
                                    else:
                                        loop = False
                                        break
                        # Here PEPPER misunderstood the name of the person
                        else:
                            im.executeModality('TEXT_default','I apologize for the misunderstanding')
                            im.executeModality('TTS','I apologize for the misunderstanding')
                            time.sleep(5)
                            continue
                    
                    # No person is matched in the database
                    else:
                        im.executeModality('IMAGE','img/x.png')
                        im.executeModality('TEXT_default','I\'m sorry but the person you\'re looking for is not in this hospital. Can I help you anyway?')
                        im.executeModality('TTS','I apologize but this person is not in this hospital')
                        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                        answer = im.ask(actionname=None,timeout=45)
                        if answer=='yes':
                            continue
                        else:
                            break

            #############################
            #   Looking for a doctor    #
            #############################
            elif b == 'doctors':
                while True:
                    im.executeModality('TEXT_default','Who are you looking for?')
                    im.executeModality('TTS','Who are you looking for?')
                    im.executeModality('BUTTONS',[['Doctor Burioni','Doctor Burioni'],['Doctor Merlini','Doctor Merlini'],['Doctor Dolittle','Doctor Dolittle']])
                    im.executeModality('IMAGE','img/madrob.jpg') 
                    c = im.ask(actionname=None, timeout=40)

                    if c == 'Doctor Burioni':
                        im.executeModality('TEXT_title','Wait I am calling him right away . . ')
                        im.executeModality('TEXT_default','Go to the room 123, he will arrive soon')  
                        im.executeModality('IMAGE','img/callhelp.png')  
                        im.executeModality('TTS','How do you feel? ')
                        time.sleep(10)

                    elif c == 'Doctor Merlini':
                        im.executeModality('IMAGE','img/hospital_2_modified.jpg')  
                        im.executeModality('TEXT_default','Doctor Merlini is in cardiology, the yellow pavillion.'+DATABASE_GET_TO_PLACE["cardiology"])  
                        time.sleep(20)

                    else:
                        im.executeModality('TEXT_title','Wait here !')
                        im.executeModality('TEXT_default','Do you talk with animals? Maybe you are not well, I will call him right now')  
                        im.executeModality('IMAGE','img/callhelp.png')  
                        im.executeModality('TTS','How do you feel? ')
                        time.sleep(10)

                    im.executeModality('TEXT_default','Do you want to call again a doctor?')
                    im.executeModality('TTS','Do you want to call again a doctor?')
                    im.executeModality('IMAGE','img/madrob.jpg')  
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                    answer = im.ask(actionname=None,timeout=40)

                    if answer == 'yes':
                        continue
                    else:
                        break



            #########################
            #   Fun with Pepper     #
            #########################
            elif b == 'fun':
                
                g = True
                im.executeModality('TEXT_default','Are you boring? Lets do a quiz ;)')  
                im.executeModality('TTS','Are you boring? Lets do a quiz')

                while(g):

                    im.executeModality('TEXT_title','Pepper Quiz') 
                    im.executeModality('TEXT_default','Initializing . . .') 
                    im.executeModality('IMAGE','img/quiz.jpg') 
                    time.sleep(5)
                    im.executeModality('TEXT_default','Remember, you have 10 seconds to answer to each question') 
                    time.sleep(3)
                                      
                    score = 0
                    im.executeModality('IMAGE','img/berlin.png')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about history')
                    im.executeModality('TEXT_title','Lets talk about history')
                    #write on the tablet
                    im.executeModality('TEXT_default','In which year the Berlin Wall fall?')
                    im.executeModality('BUTTONS',[['1989','1989'],['1999','1999'],['1960','1960']])
                
                    c = im.ask(actionname=None, timeout=10)
                    if c=='1989':
                        im.executeModality('TEXT_default','Very good')
                        score = score +1
                    elif c == 'timeout':
                        im.executeModality('TEXT_default','Time is over, not good')
                    else:
                        im.executeModality('TEXT_default','Not good')

                    time.sleep(3)

                    im.executeModality('IMAGE','img/serieA.png')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about sport')
                    im.executeModality('TEXT_title','Lets talk about sport')
                    #write on the tablet        
                    im.executeModality('TEXT_default','Which team won serie A in 2001?')
                    im.executeModality('BUTTONS',[['roma','Roma'],['lazio','Lazio'],['juve','Juve']])

                    d = im.ask(actionname=None, timeout=10)

                    if d == 'roma':
                        im.executeModality('TEXT_default','Very good')
                        score += 1
                    elif d == 'timeout':
                        im.executeModality('TEXT_default','Time is over, not good')
                    else:
                        im.executeModality('TEXT_default','Not good')
                        

                    time.sleep(3)

                    im.executeModality('IMAGE','img/pinkfloyd.jpg')
                    #the robot say this:
                    im.executeModality('TTS','Lets talk about music')
                    im.executeModality('TEXT_title','Lets talk about music')
                    #write on the tablet
                    im.executeModality('TEXT_default','How many members did pinkfloyd have?')
                    im.executeModality('BUTTONS',[['4','4'],['5','5'],['3','3']])

                    e = im.ask(actionname=None, timeout=10)
                    if e=='4':
                        im.executeModality('TEXT_default','Very good')
                        score += 1
                    elif e == 'timeout':
                        im.executeModality('TEXT_default','Time is over, not good')
                    else:
                        im.executeModality('TEXT_default','Not good')         

                    time.sleep(3)

                    im.executeModality('IMAGE','img/odissey.jpg')
                    #the robot say this:
                    im.executeModality('TTS','And now the last question')
                    im.executeModality('TEXT_title','And now the last question...')
                    #write on the tablet
                    im.executeModality('TEXT_default','<<2001: A Space Odissey>> produced and directed by Kubrick was inspired by Arthur Clarke novel The Sentinel')
                    im.executeModality('BUTTONS',[['t','True'],['f','False']])

                    f = im.ask(actionname=None, timeout=10)
                    if f=='t':
                        im.executeModality('TEXT_default','Very good')
                        score += 1
                    elif f == 'timeout':
                        im.executeModality('TEXT_default','Time is over, not good')
                    else:
                        im.executeModality('TEXT_default','Not good')
                    time.sleep(3)


                    #final score
                    if score == 4:
                        im.executeModality('IMAGE','img/master.jpg')
                        im.executeModality('TEXT_default','You are a master')
                        time.sleep(5)
                        #im.robot.say("Lets shoot a picture to the champion, ok?:")
                        im.executeModality('TEXT_default','Lets shoot a picture to the campion: say OK to accept. . .')
                        im.executeModality('ASR',['ok','no'])
                        g = im.ask(actionname=None, timeout=35)

                        if g == 'ok':
                            im.executeModality('TEXT_default','Taking the picture, say cheese')
                            im.robot.say("Say cheeeeese")
                            time.sleep(3)
                            im.robot.takephoto()
                        else:
                            im.executeModality('TEXT_default','Ok, how precius...')
                            time.sleep(3)

                    else:
                        im.executeModality('IMAGE','img/sad.png')
                        im.executeModality('TEXT_default','You have to improve yourself')
                        time.sleep(3)
                    

                    im.executeModality('TEXT_default','GAME OVER: Play again?')
                    im.executeModality('TTS','GAME OVER: Play again?')
                    im.executeModality('IMAGE','img/gameover.jpg')
                    time.sleep(3)
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                    

                    c = im.ask(actionname=None, timeout=40)

                    if c == 'yes':
                        im.executeModality('TEXT_default','Ok, restart the game')
                        im.executeModality('TTS','Ok, restart the game')
                        time.sleep(5)

                    else:
                        g = False
                        im.executeModality('TEXT_default','Exit . . .')
                        im.executeModality('TTS','Exit from the game now')
                        time.sleep(5)
                        t = False 
            #######################################
            #   Basic information about Pepper   #
            #######################################
            else:
                
                while True:
                    im.executeModality('TEXT_title','Here you can read my story  ')
                    im.executeModality('TEXT_default','I am Pepper, one of the first social humanoid robots able to recognize faces and basic human emotions. I am optimized for human interactions and to engage with people through conversations and my touch screen')
                    im.executeModality('TTS','Here can you read my story')
                    im.executeModality('IMAGE','img/softbank.jpg')
                    time.sleep(8)
                    im.executeModality('TEXT_default','In this hospital I have several important roles: for example in this area I try to clarify every doubt of people, playing an info point role. I can be very useful, I know a lot of things')
                    time.sleep(20)
                    im.executeModality('TEXT_default','Then, during the night I am also on the first floor, where I am employed as assistant and supervisor for patients: I can call the medical stuff if there is some problem')
                    time.sleep(20)

                    im.executeModality('TEXT_default','Other informations about me and my usage in healtcare environment?')
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

                    c = im.ask(actionname=None, timeout=40)

                    if c == 'yes':
                        im.executeModality('TEXT_default',' Ok, I am glad to show you')
                        time.sleep(5)
                        im.executeModality('IMAGE','img/healtcare.png')
                        im.executeModality('TEXT_default',' In this particular period softbank robotics has started a Covid-19 initiative to support hospitals and clinics ')
                        time.sleep(15)
                        im.executeModality('TEXT_default',' Do you want more informations?')
                        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                        d = im.ask(actionname=None, timeout=40)

                        if d == 'yes':
                            im.executeModality('TEXT_default','You can have more informations by visiting the following link: "https://www.softbankrobotics.com/emea/en/pepper" !')
                            
                        else:
                            im.executeModality('TEXT_default','Ok, I am always here, if you want')            
                    
                    else:
                        im.executeModality('TEXT_default','Ok, I am always here, if you want')

                    time.sleep(20)
                    im.executeModality('TEXT_default','Do you want to read again the infos about me?')                   
                    im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
                    c = im.ask(actionname=None, timeout=40)
                    if c == 'yes':
                        continue
                    else:
                        break

            
            time.sleep(2.5)
            im.executeModality('TEXT_title','I am Pepper and I am here for you')
            im.executeModality('IMAGE','img/infopoint.jpg') 
            im.executeModality('TEXT_default','Do you need other informations?')
            im.executeModality('TTS','Do you need other informations?')   
            im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
            c = im.ask(actionname=None, timeout=40)
            if c == 'yes':
                continue
            
        
            #TRANSPARENCY section: whenever a buttons is pressed it asks for satisfiability 
            if t == True:

                time.sleep(3)
                im.executeModality('TEXT_title','Just a question')
                im.executeModality('TEXT_default','Sorry, are you satisfied of my services?')
                im.executeModality('TTS','Are you satisfied of my services?')
                im.executeModality('IMAGE','img/robot.gif')
                im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])

                d = im.ask(actionname=None, timeout=40)

                if d == 'yes':
                    im.executeModality('IMAGE','img/happy.jpg')
                    im.executeModality('TEXT_title','Your opinion is important')
                    im.executeModality('TEXT_default','Thanks, I do my best')
                    im.executeModality('TTS','Thanks, I do my best')
                    time.sleep(3)
                else:
                    im.executeModality('TEXT_title','Your opinion is important')
                    im.executeModality('TEXT_default','Help me to optimize my functioning, fill the questionnaire that will open here in a minute')
                    im.executeModality('TTS','Help me to optimize my functioning, fill the questionnaire that will open here in a minute')
                    time.sleep(3)
                t = False			

        # User actually needs NO help
        else:
            t = False
            im.executeModality('IMAGE','img/pepperr.jpg')
            im.executeModality('TEXT_default','OK. bye bye, have a nice day')
            im.executeModality('TTS','I will be around here')


    # Final greetings
    time.sleep(5)
    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Happy to help you !')
    im.executeModality('TTS','Bye bye, happy to help you')


def questionnaire():

    # Just an help function: like a switch in Java
    def switch_questionnaire(i):
        switcher={
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        }
        return switcher[i]

    #Display another html page (specific for the questionnaire part)
    im.display.loadUrl("layout_questionnaire.html")

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

    a = im.ask(actionname=None, timeout=8)

    if a == 'ok':

        im.robot.green_eyes()
        time.sleep(1)
        
        # Explain the questionnaire
        im.executeModality('TTS','Choose in this range: 1 means: ABSOLUTELY NOT 2 means: MORE NO THAN YES 3 means: NEITHER YES OR NOT\n 4 means: MORE YES THAN NO\n 5 means: ABSOLUTELY YES')
        im.executeModality('TEXT_default','Choose in this range: \n 1 : ABSOLUTELY NOT \n 2 : MORE NO THAN YES \n 3 : NEITHER YES OR NOT \n 4 : MORE YES THAN NO \n 5 : ABSOLUTELY YES')
        time.sleep(15)

        # Starting score
        judge = 0 

        im.executeModality('TTS','How comfortable did you feel?')
        im.executeModality('TEXT_default','How comfortable did you feel?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        b = im.ask(actionname=None, timeout=40)
        judge += switch_questionnaire(int(b))

        time.sleep(3)
        
        im.executeModality('TTS','Did I seem friendly to you?')
        im.executeModality('TEXT_default','Did I seem friendly to you?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        c = im.ask(actionname=None, timeout=40)
        judge += switch_questionnaire(int(c))

        time.sleep(3)

        im.executeModality('TTS','Did I seem enough rielable?')
        im.executeModality('TEXT_default','Did I seem rielable to you?')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        d = im.ask(actionname=None, timeout=40)
        judge += switch_questionnaire(int(d))

        time.sleep(3)

        im.executeModality('TTS','So, how much you trust me?')
        im.executeModality('TEXT_default','So, how much do you trust me? ')
        im.executeModality('BUTTONS',[['1','1'],['2','2'],['3','3'],['4','4'],['5','5']])
        e = im.ask(actionname=None, timeout=40)
        judge += switch_questionnaire(int(e))

        time.sleep(3)

        im.executeModality('TTS','Would you recommend me to others?')
        im.executeModality('TEXT_default','Would you recommend me to others?')
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        f = im.ask(actionname=None, timeout=40)
        avg = judge/4

        # We give to the final question a higher weight wrt the other questions
        if f == 'yes':
            avg += 1
        else:
            avg -= 1

        if avg >= 3:
            im.executeModality('TEXT_title','Your opinion is important')
            im.executeModality('IMAGE','img/happy.jpg')         
            im.executeModality('TTS','Your judgment was positive, thank you')
            im.executeModality('TEXT_default','Your judgment was positive, thank you')
            time.sleep(3)
        else:
            im.executeModality('IMAGE','img/rocky.jpg')
            im.executeModality('TTS','Your judgment was not good, I will improve myself, I promise')
            im.executeModality('TEXT_default','Your judgment was not good... I will improve myself, I promise')
            time.sleep(3)
    


    im.executeModality('TEXT_title','Sayonara')
    im.executeModality('IMAGE','img/pepperr.jpg')
    im.executeModality('TEXT_default','Bye bye, I hope to see you soon')
    im.executeModality('TTS','Bye bye')
    

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    mws.run_interaction(hellothere) # blocking

    mws.run_interaction(infopoint) # blocking

    #mws.run_interaction(questionnaire) #blocking

    





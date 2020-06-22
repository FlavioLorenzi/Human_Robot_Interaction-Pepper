import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *

###################################################################################################
#   This is during the night, when Pepper is able to wander inside the wall of the hospital.      #
#   When someone is met, the robot can stop him and interact with him, giving him some advices.   #
###################################################################################################


def supervisor():

    #Future work: algoritmo di random autonomous navigation on obstacle avoidance implementato:
    # (il robot conosce gia la mappa grazie ad uno slam fatto in passato)

    im.init()

    im.display.loadUrl('layout_supervisor.html')

    im.robot.startSensorMonitor()
    time.sleep(1)    
    
    im.executeModality('ASR',["help"])                              # Patients are known to say 'help' in case of emergency
    im.executeModality('BUTTONS',[['nurse','nurse'],['doc','doc']]) # Doctor is called manually
    sonar = im.robot.sensorvalue()
    frontsonar = sonar[1]
    o = im.ask(actionname=None, timeout=200)

    #Either press button or ASR
    if o != 'timeout':
      if o == 'doc':
        im.execute('doc')
      elif:

    if (frontsonar >0.1 and frontsonar <3) or h == "help":
    
        time.sleep(1)

        im.robot.raiseArm('R') # Raise arm to stop 
        im.execute('alt')      # Perform action 'alt'

        grave = False
      
        time.sleep(4)
        im.executeModality('TEXT_title','Whats your problem?')
        #TRANSPARENCY: I don't wanna bother you..
        im.executeModality('TEXT_default','I don\'t want bother you, but why are you standing at this hour of the night?')

        # The patietn has 4 options
        im.executeModality('ASR',["I am sick","I can\'t sleep","I was thirsty"])
        im.executeModality('BUTTONS',[["I am sick","I am sick"],["I can\'t sleep","I can\'t sleep"],["I was thirsty","I was thirsty"],["other","other"]])
        c = im.ask(actionname=None, timeout=20)

        if c == "I am sick":
          im.executeModality('TEXT_default','How bad you feel? ')
          im.executeModality('BUTTONS',[['1','A little'],['5','So-So'],['10','Too much']])
          b = im.ask(actionname=None, timeout=15)

          # It's not very sick
          if b=='1':
              im.executeModality('TEXT_default','Take a moment, or wait untill tomorrow')  
              im.executeModality('IMAGE','img2/moment.jpg')    
              time.sleep(4)

          # Call a nurse
          elif b=='5':
            im.execute('nurse')    
            time.sleep(4)
            grave = True

          # It's better to call a doc
          else:
            im.execute('doc')    
            time.sleep(4)
            grave = True
        
        elif c == "I can\'t sleep":
          im.execute('tips1')    # Take melatonin o valerian
          time.sleep(4)

        elif c == "I was thirsty":
          im.execute('tips2')    # Near your bed there is the water bottle
          time.sleep(4)

        else:
          im.executeModality('TEXT_default','I am sorry but it is beyond my capability')
          time.sleep(4)
          im.execute('nurse')  #call nurse
          time.sleep(4)

        # If the patient is not very sick
        if not grave:
          im.executeModality('TEXT_title','Good night')
          im.executeModality('TEXT_default','Ok, now return in your room and try to rest...')
          im.executeModality('TTS','Ok, now return in your room and try to rest...')
          im.executeModality('IMAGE','img2/gn.gif')
          time.sleep(4)

        else:
          im.executeModality('TEXT_title','Keep calm')
          im.executeModality('TEXT_default','I will be here with you until doctor arrives')
          im.executeModality('TTS','Ok, now return in your room and try to rest...')
          im.executeModality('IMAGE','img2/calm.gif')
          time.sleep(4)
    

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    #mws.run_interaction(supervisor) # blocking

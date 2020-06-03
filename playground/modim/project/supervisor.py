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

    #Future work: algoritmo di random autonomous navigation on obstacle avoidance implementato:
    # (il robot conosce gia la mappa grazie ad uno slam fatto in passato)

    im.init()
    im.robot.startSensorMonitor()

    time.sleep(1)
    im.display.loadUrl('supervisor.html')


    # TODO bisogna trovare il modo per renderli fissi: qui danno fastidio all ASR

    '''
    im.executeModality('BUTTONS',[['nurse','nurse'],['doc','doc']]) #chiamare subito il medico manualmente
    o = im.ask(actionname=None, timeout=200)

    if o == 'nurse':
      im.execute('nurse')
    else:
      im.execute('doc')

    time.sleep(1)  
    '''  
    im.executeModality('BUTTONS',[['nurse','nurse'],['doc','doc']]) #chiamare subito il medico manualmente

    im.executeModality('ASR',["help"])        #i pazienti sono avvisati che per ricevere assistenza devono dire 'help'
    h = im.ask(actionname=None, timeout=200)

    sonar = im.robot.sensorvalue()
    frontsonar = sonar[1]
    print('Rilevo distanza di',frontsonar)      #qui aggiungere il face recognition per ''non parlare con i muri'' TODO

    if h == 'nurse':
      im.execute('nurse')
    if h == 'doc':
      im.execute('doc')


    if (frontsonar >0.1 and frontsonar <3) or h == "help":
    

        

        time.sleep(1)

        im.robot.raiseArm('R') #alt fermati con la mano
        
        im.execute('alt')   #esegue l'azione alt

        grave = False
      
        time.sleep(4)
        im.executeModality('TEXT_title','Whats your problem?')
        #transparency: non voglio scocciarti ma...
        im.executeModality('TEXT_default','I don\'t want bother you, but why are you standing at this hour of the night?')

        #il paziente ha 3 opzioni: oppure la 4 che e' chiamare direttamente qualcuno

        im.executeModality('ASR',["I am sick","I can\'t sleep","I was thirsty"])
        im.executeModality('BUTTONS',[["I am sick","I am sick"],["I can\'t sleep","I can\'t sleep"],["I was thirsty","I was thirsty"],["other","other"]])
        c = im.ask(actionname=None, timeout=20)

        if c == "I am sick":
          im.executeModality('TEXT_default','How bad you feel? ')
          im.executeModality('BUTTONS',[['1','A little'],['5','So-So'],['10','Too much']])
          b = im.ask(actionname=None, timeout=15)

          if b=='1':
              im.executeModality('TEXT_default','Take a moment, or wait untill tomorrow')  
              im.executeModality('IMAGE','img2/moment.jpg')    #Prendi un moment e ritorna al letto, passera'
              time.sleep(4)

          elif b=='5':
            im.execute('nurse')    #Ok chiamo un infermiera
            time.sleep(4)
            grave = True

          else:
            im.execute('doc')    #E' grave! ok chiamo un medico
            time.sleep(4)
            grave = True
        
        elif c == "I can\'t sleep":
          im.execute('tips1')    #take melatonin o valerian
          time.sleep(4)

        elif c == "I was thirsty":
          im.execute('tips2')    #near your bed there is the water bottle
          time.sleep(4)

        else:
          im.executeModality('TEXT_default','I am sorry but it is beyond my capability')
          time.sleep(4)
          im.execute('nurse')  #call nurse
          time.sleep(4)

        #non e' grave dai la buona notte
        if not grave:
          im.executeModality('TEXT_title','Good night')
          im.executeModality('TEXT_default','Ok, now return in your room and try to rest...')
          im.executeModality('TTS','Ok, now return in your room and try to rest...')
          im.executeModality('IMAGE','img2/gn.gif')
          time.sleep(4)


        # e' grave resta col paziente
        else:
          im.executeModality('TEXT_title','Keep calm')
          im.executeModality('TEXT_default','I will be here with you until doctor arrives')
          im.executeModality('TTS','Ok, now return in your room and try to rest...')
          im.executeModality('IMAGE','img2/calm.gif')
          time.sleep(4)
    
#TODO
#Buttons per call doc e call nurse sempre visibili





if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

        
    mws.run_interaction(supervisor) # blocking

    #Future work: fare in modo che questo si ripeta ogni volta che incontra un paziente!
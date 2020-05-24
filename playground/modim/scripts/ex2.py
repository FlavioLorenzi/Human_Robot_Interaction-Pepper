import os, sys

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')


import ws_client
from ws_client import *



# Definition of interaction functions
#se rileva qualcuno nel range allora dice benvenuto con tablet e voce


#non so perche ma funziona senza init



def quiz():
	im.executeModality('IMAGE','img/pepperr.jpg')
	im.executeModality('TEXT_default','Wanna play with me?')
	im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
	# wait for answer
	a = im.ask(actionname=None, timeout=15)
	if a=='yes':
		r = im.askUntilCorrect('quiz', timeout=15)
		im.executeModality('TEXT_default',r)

		#come fare ad inserire score negativo se sbaglio risp?

		o = im.askUntilCorrect('quizHistory', timeout=15)
		im.executeModality('TEXT_default',o)


		p = im.askUntilCorrect('quizMusic', timeout=15)
		im.executeModality('TEXT_default',p)

		#score = score + 3

	else:
		im.executeModality('TEXT_default','Bye bye')


	
	im.executeModality('IMAGE','img/master.jpg')
	im.executeModality('TEXT_default','You are a master')
	
		#im.executeModality('IMAGE','img/sad.png')
		#im.executeModality('TEXT_default','You have to improve yourself')


#Non riesco a far funzionare le action, forse vanno indirizzate meglio.
  

#quiz manuale, piu diretto
def quiz2():
	
	score = 0
	im.init()
	im.executeModality('IMAGE','img/pepperr.jpg')
	im.executeModality('TEXT_default','Wanna play with me?')
	im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
	# wait for answer
	a = im.ask(actionname=None, timeout=15)
	if a=='yes':

		im.executeModality('TEXT_default','Ok, lets play')
		
		time.sleep(2)

		im.executeModality('IMAGE','img/berlin.png')
		#the robot say this:
		im.executeModality('TTS','Lets talk about history')
		#write on the tablet
		im.executeModality('TEXT_default','In which year the Berlin Wall fall?')
		im.executeModality('BUTTONS',[['1989','1989'],['1999','1999'],['1960','1960']])
	
		b = im.ask(actionname=None, timeout=15)
		if b=='1989':
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

		c = im.ask(actionname=None, timeout=15)

		if c == 'roma':
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

		d = im.ask(actionname=None, timeout=15)
		if d=='4':
			im.executeModality('TEXT_default','Very good')
			score = score +1
		else:
			im.executeModality('TEXT_default','Not good')
			

		time.sleep(3)
		#final score
		if score == 3:
			im.executeModality('IMAGE','img/master.jpg')
			im.executeModality('TEXT_default','You are a master')
		else:
			im.executeModality('IMAGE','img/sad.png')
			im.executeModality('TEXT_default','You have to improve yourself')		


	else:
		im.executeModality('TEXT_default','Ok, bye bye')









# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    #quiz
        
    mws.run_interaction(quiz2) # blocking

    #mws.run_interaction(quiz2) # blocking

    

    





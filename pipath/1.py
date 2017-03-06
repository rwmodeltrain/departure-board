# -*- coding: utf-8 -*-
import os
import logging

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


def ExecuteDepartureboard ():
	#read billboard.ini for location ini files
	config = ConfigParser()
	config.read('appinit.ini')
	apppath = config.get('General','apppath')
	appname = config.get('General','appname')

	# Python 2.X only!
	#execfile (apppath+appname)
	if os.getuid() == 0:
		os.system('sudo python ' +apppath+appname)
	else:
		os.system('python ' +apppath+appname)
		

if __name__ == '__main__':

		
		if os.path.exists('AppInitErrors.log'): 
   	 		os.remove('AppInitErrors.log')

		logging.basicConfig(level=logging.DEBUG, filename='AppInitErrors.log')

		
		try:
    			ExecuteDepartureboard()
		except:
    			logging.exception("Error:")
    	
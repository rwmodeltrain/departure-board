# -*- coding: utf-8 -*-
import os
import glob
import pygame
import time
import random
import threading
import datetime
import io
import sys
import logging
from time import gmtime, strftime



try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


			
class StationCollection(object):
	def __init__(self):
		self.stations = []
		self._data = self.stations
		
	def append(self, object):
		self.stations.append (object)
		
	def __iter__(self):
		for elem in self._data:
			yield elem
			
	def GetActiveStation(self):
		station=Station()
		returnstation = Station()
		for station in self.stations:
			if station.active == True:
				returnstation = station
		return returnstation
		
		
	
	
class Station(object):
	def __init__(self):
		
		self.trains = []
		self.ads = []
		
		#id
		@property
		def id(self):
			return self.__id
		@id.setter
		def id(self, id):
			self.__id=id

		#name
		@property
		def name(self):
			return self.__name
		@name.setter
		def name(self, name):
			self.__name=name

		#active
		@property
		def active(self):
			return self.__active
		@name.setter
		def active(self, active):
			self.__active=active
			
		#traincount
		@property
		def traincount(self):
			return self.__traincount
		@traincount.setter
		def traincount(self, traincount):
			self.__traincount=traincount

		#adcount
		@property
		def adcount(self):
			return self.__adcount
		@adcount.setter
		def adcount(self, adcount):
			self.__adcount=adcount
			
		#advertize
		@property
		def advertize(self):
			return self.__advertize
		@advertize.setter
		def advertize(self, advertize):
			self.__advertize=advertize
			
		#advertizemode
		@property
		def advertizemode(self):
			return self.__advertizemode
		@advertizemode.setter
		def advertizemode(self, advertizemode):
			self.__advertizemode=advertizemode
	

	def GetTrainsFromIniFile (self,inipath):
   				
		config=ConfigParser()
		# parse ini file for station. Filename = stationname+.ini
		config.read(inipath+self.name+'.ini')
		

		#read countoftrains
		countoftrains = config.getint('General', 'traincount')
		logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': Read '+str(countoftrains)+' trains from: '+inipath+self.name+'.ini')
		self.traincount=countoftrains
		
		#read trains
		for intI in range (1, countoftrains+1):
			train = Train()
			train.inid = config.getint('Train'+str(intI), 'inid')
			train.id = config.getint('Train'+str(intI), 'id')
			train.da = config.get('Train'+str(intI), 'da')
			train.type = config.get('Train'+str(intI), 'type')
			train.destination = config.get('Train'+str(intI), 'destination')
			train.rail = config.get('Train'+str(intI), 'rail')
			train.position = config.getint('Train'+str(intI), 'position')
			train.status = config.get('Train'+str(intI), 'status')
			dt = datetime.timedelta(minutes=3 +(train.position*3))
			traintime = format(datetime.datetime.now() + dt,"%H:%M")
			train.time = traintime
			MyTrainType = TrainType()
			MyTrainType = GetTrainTypeByType(train.type)
			train.logofile = MyTrainType.logofile
			train.logoxpos = MyTrainType.logoxpos
			self.trains.append (train)

	def SaveTrainsToIniFile (self,inipath):
		#used when quitting app, only useful when pyscript is started as sudo
		config=ConfigParser()
		# parse stations file
		config.read(inipath+self.name+'.ini')
	
		train = Train()
		for train in self.trains:
			config.set('Train'+str(train.inid), 'rail', train.rail)
			config.set('Train'+str(train.inid), 'position', str(train.position))
			config.set('Train'+str(train.inid), 'status', train.status)
			
		with open(inipath+self.name+'.ini', 'w') as configfile:
			config.write(configfile)	
	
	
	def GetAdsFromIniFile (self,inipath, adpath):
		config=ConfigParser()

		# parse stations file
		config.read(inipath+self.name+'.ini')

		#read countoftrains
		countofads = config.getint('General', 'adcount')
		self.adcount=countofads
		
		logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': Read adinfo ('+str(countofads)+') from: '+inipath+self.name+'.ini')

	
		#read ads
		for intI in range (1, countofads+1):
			MyAd = Ad()
			MyAd.id = config.getint('Ad'+str(intI), 'id')
			MyAd.type = config.get('Ad'+str(intI), 'type')
			MyAd.position = config.getint('Ad'+str(intI), 'position')
			MyAd.active = config.getboolean('Ad'+str(intI), 'active')
			MyAd.filename = adpath+config.get('Ad'+str(intI), 'filename')
			self.ads.append (MyAd)
		
	def GetActiveAd(self):
		MyAd=Ad()
		returnad = Ad()
		for MyAd in self.ads:
			if MyAd.active == True:
				returnad = MyAd
		return returnad

	def GetNextAd(self):
		MyAd=Ad()
		MyAd2 = Ad()
		returnad = Ad()
		
		MyAd = self.GetActiveAd()
		MyAd.active = False
		
		#update positions
		for MyAd2 in self.ads:
			if MyAd2.position == 1:
				MyAd2.position = self.adcount
			else:
				MyAd2.position -=1
		
				
		#Get ad with position 1
		for MyAd2 in self.ads:
			if MyAd2.position == 1:
				MyAd2.active = True
				returnad = MyAd2
		return returnad


class Ad(object):
	def __init__(self):

		#id
		@property
		def id(self):
			return self.__id
		@id.setter
		def id(self, id):
			self.__id=id

		#type
		@property
		def type(self):
			return self.__type
		@type.setter
		def type(self, type):
			self.__type=type
							
		#position
		@property
		def position(self):
			return self.__position
		@position.setter
		def position(self, position):
			self.__position=position
			
		#active
		@property
		def active(self):
			return self.__active
		@active.setter
		def active(self, active):
			self.__active=active	

		#filename
		@property
		def filename(self):
			return self.__filename
		@filename.setter
		def filename(self, filename):
			self.__filename=filename	

			
	def __del__(self):	
		pass


class TrainTypeCollection(object):
	def __init__(self):
		self.traintypes = []
		self._data = self.traintypes
		
	def append(self, object):
		self.traintypes.append (object)
		
	def __iter__(self):
		for elem in self._data:
			yield elem


class TrainType(object):
	def __init__(self):

		#id
		@property
		def id(self):
			return self.__id
		@id.setter
		def id(self, id):
			self.__id=id

		#type
		@property
		def type(self):
			return self.__type
		@type.setter
		def type(self, type):
			self.__type=type

		#logofile
		@property
		def logofile(self):
			return self.__logofile
		@logofile.setter
		def logofile(self, logofile):
			self.__logofile=logofile

		#logoxpos
		@property
		def logoxpos(self):
			return self.__logoxpos
		@logoxpos.setter
		def logoxpos(self, logoxpos):
			self.__logoxpos=logoxpos



class RouteInfoCollection(object):
	def __init__(self):
		self.routeinfos = []
		self._data = self.routeinfos
		
	def append(self, object):
		self.routeinfos.append (object)
		
	def __iter__(self):
		for elem in self._data:
			yield elem



class RouteInfo(object):
	def __init__(self):

		#id
		@property
		def id(self):
			return self.__id
		@id.setter
		def id(self, id):
			self.__id=id

		#type
		@property
		def type(self):
			return self.__type
		@type.setter
		def type(self, type):
			self.__type=type

		#description
		@property
		def description(self):
			return self.__description
		@description.setter
		def description(self, description):
			self.__description=description

		#message
		@property
		def message(self):
			return self.__message
		@message.setter
		def message(self, message):
			self.__message=message	
			
		#audiofile
		@property
		def audiofile(self):
			return self.__audiofile
		@audiofile.setter
		def audiofile(self, audiofile):
			self.__audiofile=audiofile
							
		#station
		@property
		def station(self):
			return self.__station
		@station.setter
		def station(self, station):
			self.__station=station
			
		#trainid
		@property
		def trainid(self):
			return self.__trainid
		@trainid.setter
		def trainid(self, trainid):
			self.__trainid=trainid	

		#rail
		@property
		def rail(self):
			return self.__rail
		@rail.setter
		def rail(self, rail):
			self.__rail=rail

			
	def __del__(self):	
		pass




class Train(object):
	def __init__(self):

		#inid
		@property
		def inid(self):
			return self.__inid
		@inid.setter
		def inid(self, inid):
			self.__inid=inid

		#id
		@property
		def id(self):
			return self.__id
		@id.setter
		def id(self, id):
			self.__id=id

		#DA (depart/arrive)
		@property
		def da(self):
			return self.__da
		@da.setter
		def da(self, da):
			self.__da=da

		#type
		@property
		def type(self):
			return self.__type
		@type.setter
		def type(self, type):
			self.__type=type
			
		#destination
		@property
		def destination(self):
			return self.__destination
		@destination.setter
		def destination(self, destination):
			self.__destination=destination

		#time
		@property
		def time(self):
			return self.__time
		@time.setter
		def time(self, time):
			self.__time=time
		
		#rail
		@property
		def rail(self):
			return self.__rail
		@rail.setter
		def rail(self, rail):
			self.__rail=rail	
		
		#position
		@property
		def position(self):
			return self.__position
		@position.setter
		def position(self, position):
			self.__position=position
			
		#status
		@property
		def status(self):
			return self.__status
		@status.setter
		def status(self, status):
			self.__status=status
			
		#logofile
		@property
		def logofile(self):
			return self.__logofile
		@logofile.setter
		def logofile(self, logofile):
			self.__logofile=logofile

		#logoxpos
		@property
		def logoxpos(self):
			return self.__logoxpos
		@logoxpos.setter
		def logoxpos(self, logoxpos):
			self.__logoxpos=logoxpos
			
	def __del__(self):	
		pass


class TrainCollection(object):
    def __init__(self):
        self.trains = []
    	self._data = self.trains
    
    def append(self, object):
		self.trains.append (object)

    def __iter__(self):
        for elem in self._data:
            yield elem
            

		

class TrainScreen (object):
	screen = None;
	def __init__(self):

			
		#activestation
		@property
		def activestation(self):
			return self.__activestation

		@activestation.setter
		def activestation(self, activestation):
			self.__activestation=activestation
		
		#msgvolume
		@property
		def msgvolume(self):
			return self.__msgvolume

		@msgvolume.setter
		def msgvolume(self, msgvolume):
			self.__msgvolume=msgvolume


		#mixerinit
		@property
		def mixerinit(self):
			return self.__mixerinit

		@mixerinit.setter
		def mixerinit(self, mixerinit):
			self.__mixerinit=mixerinit

			
		#useTFT
		@property
		def useTFT(self):
			return self.__useTFT

		@useTFT.setter
		def useTFT(self, useTFT):
			self.__useTFT=useTFT

		#screenwidth
		@property
		def screenwidth(self):
			return self.__screenwidth

		@screenwidth.setter
		def screenwidth(self, screenwidth):
			self.__screenwidth=screenwidth

		#screenheight
		@property
		def screenheight(self):
			return self.__screenheight

		@screenheight.setter
		def screenheight(self, screenheight):
			self.__screenheight=screenheight

		#imagelogofile
		@property
		def imagelogofile(self):
			return self.__imagelogofile

		@imagelogofile.setter
		def imagelogofile(self, imagelogofile):
			self.__imagelogofile=imagelogofile


	def InitPanel(self):
		#Init new pygame screen
		if self.useTFT==True:
			os.environ["SDL_FBDEV"] = "/dev/fb1"
		
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.display.init()

		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print "Screen size: %d x %d" % (size[0], size[1])
		self.screenwidth = size[0]
		self.screenheight = size[1]
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		# Clear the screen to start
		self.screen.fill((0, 0, 0))        
		# Initialise use of font
		pygame.font.init()
		# Update screen
		pygame.display.update()
		
			
	def GetScreenTrainByID(self,inty):
		obj=Train()
		for obj in self.activestation.trains:
			if obj.id == inty:
				obj2 = obj
		return obj2
								

	def CheckTrains(self):
		exit()

	def InitScreen(self):
		self.strTime = strftime("%H:%M", gmtime())
		pygame.mouse.set_visible(0)
		# Fill the screen with white (255, 255, 255)
		white = (255, 255, 255)
		self.screen.fill(white)

		if self.activestation.advertizemode == 0:
			#screenheader
			imagelogo = pygame.image.load(self.imagelogofile)
			logging.info (self.imagelogofile)
			self.screen.blit(imagelogo, (3,5))
			font=pygame.font.Font('FreeSans.ttf', 11)

			#station and time
			text=font.render(self.activestation.name, 1, (10, 10, 10))
			self.screen.blit(text, (50, 7))
			text=font.render(self.strTime, 1, (10, 10, 10))
			self.screen.blit(text, (127, 7))			


			#departure header
			text=font.render('DEPART', 1, (10,10,10))
			self.screen.blit(text, (3,32))
		
			train=Train()
			for train in self.activestation.trains:
				self.tvalue = train.time + " " + train.destination
				text=font.render(self.tvalue, 1, (10, 10, 10))
				vert1=34+(train.position*12)
				vert2=vert1+2
				self.screen.blit(text, (5,vert1))
				if train.logofile != "None":
					imagelogo = pygame.image.load(train.logofile)
					self.screen.blit(imagelogo, (100+train.logoxpos,vert2))
				text=font.render(train.rail, 1, (10, 10, 10))
				self.screen.blit(text, (150,vert1))
			pygame.display.update()
				
		elif self.activestation.advertizemode == 1:
			MyAd=Ad()
			MyAd = self.activestation.GetActiveAd()
			adfilename = MyAd.filename
			if MyAd.type == 'JPG':
				image = pygame.image.load(adfilename)
				self.screen.blit(image, (0,0))
				pygame.display.update()
			if MyAd.type == 'MP4':
				pygame.init() 
				pygame.mixer.quit() 
				
				background = pygame.Surface((self.screenwidth,self.screenheight)) 

				self.screen.blit(background, (0, 0)) 
				pygame.display.update() 

				movie = pygame.movie.Movie(adfilename) 
				mrect = pygame.Rect(0,0,self.screenwidth,self.screenheight) 
				movie.set_display(self.screen, mrect.move(0, 0)) 

				if self.msgvolume !=0:
					movie.set_volume(self.msgvolume/3)
				else:
					movie.set_volume(0)

				movie.play() 

 				while movie.get_busy() == True: 
 					nameof_killfile="stop_processx.txt"
 					if os.path.exists(nameof_killfile): 
 							os.remove(nameof_killfile)
 							exit()
 				
			logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': '+"Finished "+ adfilename + ": " + strftime("%H:%M:%S",time.localtime(time.time())))
			
		if self.activestation.advertizemode == 2:
			#getnextad
			MyAd = Ad()
			MyAd = self.activestation.GetNextAd()
			adfilename = MyAd.filename
			time.sleep(1.5)

			self.activestation.advertizemode = 1
			self.InitScreen()

	def UpdateTime(self):
		CurTime = strftime("%H:%M:%S", gmtime())
		print self.strTime
		if CurTime != self.strTime:
			self.strTime = CurTime
			self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (50, 7, 145, 13), 0)
			font=pygame.font.Font('FreeSans.ttf', 11)
			text=font.render(self.strtime, 1, (10, 10, 10))
			self.screen.blit(text, (127, 7))			
			pygame.display.update()
	

	def TrainDeparture(self, trainid, stationid, audiofile):
	
		#slide to right
		#move other trains up
		#add moved train to bottom
		
		font=pygame.font.Font('FreeSans.ttf', 11)
		MyTrain = Train()
		MyTrain= GetTrainByID(trainid, stationid)
		
		if stationid == self.activestation.id:

			#play whistle
			self.mixerinit = True
			pygame.mixer.init()
			MySound = pygame.mixer.Sound(audiofile)
			MySound.set_volume(self.msgvolume)
			MySound.play(0,0,0)
			logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Sound play command given for file: " + audiofile)

			y1 = 34 + (MyTrain.position * 12)
			traintext = MyTrain.time + " " + MyTrain.destination

		
			self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (0, y1, 160, 13), 0)
			text=font.render(traintext, 1, (10, 10, 10))
			self.screen.blit(text, (5,y1))
			if MyTrain.logofile != "None":
				imagelogo = pygame.image.load(MyTrain.logofile)
				self.screen.blit(imagelogo, (100+MyTrain.logoxpos,y1+2))
			text=font.render(MyTrain.rail, 1, (10, 10, 10))
			self.screen.blit(text, (150,y1))
			pygame.display.update()

			#flash text 3 times
			for intI in range (0, 3):
				time.sleep (0.5)
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (35, y1, 115, 13), 0)
				pygame.display.update()
				time.sleep (0.5)
				text=font.render(MyTrain.destination, 1, (10, 10, 10))
				self.screen.blit(text, (35,y1))
				if MyTrain.logofile != "None":
					imagelogo = pygame.image.load(MyTrain.logofile)
					self.screen.blit(imagelogo, (100+MyTrain.logoxpos,y1+1))
				pygame.display.update()


			#move text to right
			for intI in range (0, 120):
				#grey box
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (35, y1, 145, 13), 0)
				if self.useTFT == True:
					time.sleep(0.02)
				text=font.render(MyTrain.destination, 1, (10, 10, 10))
				self.screen.blit(text, (35+intI,y1))
				if MyTrain.logofile != "None":
					imagelogo = pygame.image.load(MyTrain.logofile)
					self.screen.blit(imagelogo, (100+MyTrain.logoxpos+intI,y1+1))
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (145, y1, 15, 13), 0)
				text=font.render(MyTrain.rail, 1, (10, 10, 10))
				self.screen.blit(text, (150,y1))
				self.rect = pygame.draw.rect(self.screen, (255,255,255),(160,y1,160,13),0)
				pygame.display.update()
		
			#let text appear from left
			for intI in range (0, 135):
				# maak vakje grijs waar de tekst moet scrollen
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (0, y1, 145, 13), 0)
				if self.useTFT == True:
					time.sleep(0.02)
				text=font.render(MyTrain.destination, 1, (10, 10, 10))
				self.screen.blit(text, (-100+intI,y1))
				if MyTrain.logofile != "None":
					imagelogo = pygame.image.load(MyTrain.logofile)
					self.screen.blit(imagelogo, (-35+MyTrain.logoxpos+intI,y1+2))
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (0, y1, 35, 13), 0)
				text=font.render(MyTrain.time, 1, (10, 10, 10))
				self.screen.blit(text, (5,y1))
				self.rect = pygame.draw.rect(self.screen, (255,255,255),(160,y1,160,13),0)
				pygame.display.update()		
		
			time.sleep (0.5)
			self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, y1, 115, 13), 0)
			pygame.display.update()
			
			#move grey block to right				
			for intI in range (0, 160):	
				self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, y1, 160, 13), 0)
				self.rect = pygame.draw.rect(self.screen, (225, 225, 225), (intI, y1, 160, 13), 0)
			
				text=font.render(traintext, 1, (10, 10, 10))
				self.screen.blit(text, (5+intI,y1))
				if MyTrain.logofile != "None":
					imagelogo = pygame.image.load(MyTrain.logofile)
					self.screen.blit(imagelogo, (100+MyTrain.logoxpos+intI,y1+2))
				text=font.render(MyTrain.rail, 1, (10, 10, 10))
				self.screen.blit(text, (150+intI,y1))
				self.rect = pygame.draw.rect(self.screen, (255,255,255),(160,y1,160,13),0)

				pygame.display.update()
				if self.useTFT == True:
					time.sleep(0.02)

		
		
			#move other trains up
			train=Train()
			intY2 = 13
			for intY in range(0, 12):
				intY2 +=-1
				for train in self.activestation.trains:
					self.tvalue = train.time + " " + train.destination
					if MyTrain.position == 1:
						vert1=12
					else:
						vert1=24
					if train.position !=1 and train.id != MyTrain.id:
						vert2 = vert1+2
						text=font.render(self.tvalue, 1, (225, 225, 225))
						vert1=32+(train.position*12)+intY2-11
						vert2=vert1+2
						self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, vert1, 160, 14), 0)
						self.screen.blit(text, (5,vert1))
						if train.logofile != "None":
							imagelogo = pygame.image.load(train.logofile)
							self.screen.blit(imagelogo, (100+train.logoxpos,vert2))
						text=font.render(train.rail, 1, (225, 225, 225))
						self.screen.blit(text, (150,vert1))
								
				pygame.display.update()
				if self.useTFT == True:
					time.sleep(0.1)
				else:
					time.sleep(0.05)
			
				
		#ajust trainpositions		
		MyStation = Station()
		MyStation = GetStationByID (stationid)
		for train in MyStation.trains:
			if train.position == MyStation.traincount:
				tijdstip1 = train.time
	
			#if > old position, then subtract 1
			if train.id != MyTrain.id: 
				if (train.position == 1 and (train.status == "Incoming")):
					train.position = 1
				elif train.position > 1:
					train.position += -1		
	
		#add 3 minutes to last time		
		tijdstip = datetime.datetime.strptime(tijdstip1, "%H:%M")
		dt = datetime.timedelta(minutes=3)
		traintime = format(tijdstip + dt,"%H:%M")
		MyTrain.time = traintime
		
		MyTrain.position = MyStation.traincount
		MyTrain.status = "On the way"
		MyTrain.rail = "-"

		
		if stationid == self.activestation.id: self.InitScreen()
		CheckAdvertize (self.activestation)
		t0=time.time()
			
			
	
	
	def TrainArrival(self, newtrainid, newtraintime, newtrainrail, stationid, audiofile):
		#find train
		MyTrain=Train()
		MyTrain= GetTrainByID(newtrainid, stationid)
		
		OldPos = MyTrain.position
 		MyTrain.time = newtraintime
		MyTrain.rail = newtrainrail
		MyTrain.status = "Incoming"
		
		train=Train()
		newtrainposition = 1
		
		MyStation = Station()
		MyStation = GetStationByID (stationid)
		
		for train in MyStation.trains:
			#if < old position, add 1
			if train.id != MyTrain.id: 
				if (train.position == 1 and (train.status == "Incoming")):
						newtrainposition = 2

		if stationid == self.activestation.id:
			#play arrival message as mentioned in Stations.ini
			self.mixerinit = True
			pygame.mixer.init()
			logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Mixer initiated")
			MySound = pygame.mixer.Sound(audiofile)
			MySound.set_volume(self.msgvolume)
			MySound.play(0,0,0)
			logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Sound play command given for file: " + audiofile)

			self.activestation.advertizemode = 0
			self.InitScreen()
			if newtrainposition <> OldPos:			
				#move from oldpos to train.position
				y1 = 44 + ((newtrainposition-1)*12)
				y2 = 32 + (OldPos * 12)
				font=pygame.font.Font('FreeSans.ttf', 11)
				x1=0			
			
				for intI in range (0, (y2-y1)):
					time.sleep (0.1)
					x1+=1
					#move other trains down
					train=Train()
					for train in self.activestation.trains:
						self.tvalue = train.time + " " + train.destination
						if train.position == 1 and train.status == "Incoming":					
							#leave row 1 where it is
							if newtrainposition == 1:
								text=font.render(self.tvalue, 1, (225, 225, 225))
							else:
								text=font.render(self.tvalue, 1, (10, 10, 10))
							vert1=46
							vert2=vert1+2
							self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, vert1, 160, 13), 0)
							self.screen.blit(text, (5,vert1))
							if train.logofile != "None":
								imagelogo = pygame.image.load(train.logofile)
								self.screen.blit(imagelogo, (100+train.logoxpos,vert2))
							text=font.render(train.rail, 1, (10, 10, 10))
							self.screen.blit(text, (150,vert1))				
						else:
							if train.id != MyTrain.id:
								text=font.render(self.tvalue, 1, (225, 225, 225))
								if train.position < OldPos:
									if x1<13:
										vert1=32+(train.position*12)+x1+2
									else:
										vert1=32+(train.position*12)+12	+2				
								else:
									vert1=32+(train.position*12)
								vert2=vert1+2
								self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, vert1, 160, 14), 0)
								self.screen.blit(text, (5,vert1))
								if train.logofile != "None":	
									imagelogo = pygame.image.load(train.logofile)
									self.screen.blit(imagelogo, (100+train.logoxpos,vert2))
								text=font.render(train.rail, 1, (225, 225, 225))
								self.screen.blit(text, (150,vert1))
					
					#move mytrain up
					self.rect = pygame.draw.rect(self.screen, (255, 255, 255), (0, y2-intI+1, 160, 14), 0)
					text = MyTrain.time + " " + MyTrain.destination
					text=font.render(text, 1, (10, 10, 10))
					self.screen.blit(text, (5,y2-intI))
					if MyTrain.logofile != "None":
						imagelogo = pygame.image.load(MyTrain.logofile)
						self.screen.blit(imagelogo, (100+MyTrain.logoxpos,y2+2-intI))
					text=font.render(MyTrain.rail, 1, (10, 10, 10))
					self.screen.blit(text, (150,y2-intI))
					pygame.display.update()
				
		MyTrain.position = newtrainposition
		
		#ajust trainpositions
		for train in MyStation.trains:
			#als < oude positie, dan 1 erbij op
			if train.id != MyTrain.id: 
				if (train.position == 1 and (train.status == "Incoming")):
					train.position=1 
				elif train.position < OldPos:
					train.position += 1		
		self.RecalculateTrainTimes(stationid)
		
		if stationid == self.activestation.id:
			self.InitScreen()	
		
	def RecalculateTrainTimes(self, stationid):
		train = Train()
		MyStation = Station()
		MyStation = GetStationByID (stationid)
	
		for train in MyStation.trains:
			if train.position > 1:
				#find train with position - 1
				for train2 in self.activestation.trains:
					if train2.position == (train.position-1) and train.status != "Incoming":
						#recalulate time
						tijdstip1=train2.time
						tijdstip = datetime.datetime.strptime(tijdstip1, "%H:%M")
						dt = datetime.timedelta(minutes=3)
						traintime = format(tijdstip + dt,"%H:%M")
						train.time = traintime							
			
	def PrintMessage (self, strA):
			font=pygame.font.Font('FreeSans.ttf', 11)
			# Fill the screen with red (255, 0, 0)
			red = (255, 255, 255)
			self.screen.fill(red)
			text=font.render(strA, 1, (10, 10, 10))
			self.screen.blit(text, (35,84))
			pygame.display.update()

	def __del__(self):
		"""Clean up"""

def GetStationByID(inty):
	obj=Station()
	for obj in MyStations:
		if obj.id == inty:
			obj2 = obj
	return obj2

def GetTrainByID(inty, stationid):
	obj=Train()
	MyStation = GetStationByID(stationid)
	for obj in MyStation.trains:
		if obj.id == inty:
			obj2 = obj
	return obj2

def GetTrainTypeByType(type):
	obj=TrainType()
	for obj in MyTrainTypes:
		if obj.type == type:
			obj2 = obj
	return obj2


def tail_lines(filename,linesback=10,returnlist=0):
    ##source: Ed Pascoe: http://code.activestate.com/recipes/157035-tail-f-in-python/
    """Does what "tail -10 filename" would have done
       Parameters:
            filename   file to read
            linesback  Number of lines to read from end of file
            returnlist Return a list containing the lines instead of a string

    """
    avgcharsperline=75

    file = io.open(filename,'r', encoding="UTF-8")
    while 1:
    
        try: file.seek(-1 * avgcharsperline * linesback,2)
        except IOError: file.seek(0)
        if file.tell() == 0: atstart=1
        else: atstart=0

        lines=file.read().split(chr(10))
        if (len(lines) > (linesback+1)) or atstart: break
        #The lines are bigger than we thought
        avgcharsperline=avgcharsperline * 1.3 #Inc avg for retry
    file.close()

    if len(lines) > linesback: start=len(lines)-linesback -1
    else: start=0
    if returnlist: return lines[start:len(lines)-1]

    out=""
    for l in lines[start:len(lines)-1]: out=out + l + "/n"
    return out

def CheckAdvertize(MyActiveStation):
		MyActiveStation.advertizemode = 1
		MyTrain = Train()
		for MyTrain in MyActiveStation.trains:
			if MyTrain.rail != "-": MyActiveStation.advertizemode = 0


def departureboard():
	
	#main code
	MyStation = ""
	
	# instantiate
	config = ConfigParser()

	apppath = os.path.realpath(__file__)


	nameof_killfile="stop_processx.txt"
	if os.path.exists(apppath+nameof_killfile): 
		os.remove(apppath+nameof_killfile)
		
	nameof_killfile="kill_pi.txt"
	if os.path.exists(apppath+nameof_killfile):
		os.remove(apppath+nameof_killfile)

	nameof_killfile="reboot_pi.txt"
	if os.path.exists(apppath+nameof_killfile):
		os.remove(apppath+nameof_killfile)


	#read departure-board.ini for location ini files etc.
	config.read('departure-board.ini')
	inipath = config.get('General','inipath')
	adpath = config.get('General','adpath')
	audiopath = config.get('General','audiopath')
	logopath = config.get('General','logopath')	
	CurrentStation = config.get('General','currentstation')
	msgvolume = float(config.getint('General','msgvolume'))/100
	useTFT = config.getboolean('General','usetft')
	
	#read Trackinfo.ini file
	config.read(inipath+'Trackinfo.ini')
	logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': Open '+inipath+'Trackinfo.ini for input')
	
	
	#read traintypeinfo (in Trackinfo.ini)
	countoftraintype = config.getint('General','traintypecount')
	for intI in range (1, countoftraintype+1):
		MyTrainType = TrainType()
		MyTrainType.id = config.getint('TrainType'+str(intI), 'id')	
		MyTrainType.type = config.get('TrainType'+str(intI), 'type')
		MyTrainType.logoxpos = config.getint('TrainType'+str(intI), 'logoxpos')
		logofile = config.get('TrainType'+str(intI), 'logofile')
		if logofile != "None":
			MyTrainType.logofile = logopath+config.get('TrainType'+str(intI), 'logofile')
		else:
			MyTrainType.logofile = "None"
		MyTrainTypes.append (MyTrainType)


	#read stationinfo (from Trackinfo.ini)
	countofstations = config.getint('General', 'stationcount')
	for intI in range (1, countofstations+1):
		MyStation = Station()
		MyStation.id = config.getint('Station'+str(intI), 'id')
		MyStation.name = config.get('Station'+str(intI), 'name')
		if MyStation.name == CurrentStation:
			MyStation.active = True
		else:
			MyStation.active = False
		MyStations.append (MyStation)
		MyStation.GetTrainsFromIniFile(inipath)
		logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': '+'Traininfo read for: '+MyStation.name)
		MyStation.GetAdsFromIniFile(inipath, adpath)
		logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': '+'Adinfo read for: '+MyStation.name)

	

	#read routeinfo (in Trackinfo.ini)
	countofrouteinfo = config.getint('General','routeinfocount')
	for intI in range (1, countofrouteinfo+1):
		MyRouteInfo = RouteInfo()
		MyRouteInfo.id = config.getint('Routeinfo'+str(intI), 'id')
		MyRouteInfo.description = config.get('Routeinfo'+str(intI), 'name')
		MyRouteInfo.type = config.get('Routeinfo'+str(intI), 'type')
		MyRouteInfo.message = config.get('Routeinfo'+str(intI), 'koplopermessage')
		MyRouteInfo.audiofile = audiopath+config.get('Routeinfo'+str(intI), 'audiofile')
		MyRouteInfo.station = config.getint('Routeinfo'+str(intI), 'station')
		MyRouteInfo.trainid = config.getint('Routeinfo'+str(intI), 'trainid')
		MyRouteInfo.rail = config.get('Routeinfo'+str(intI), 'rail')
		MyRouteInfos.append (MyRouteInfo)
	
	logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': '+'Routeinfo read.')	

	#initialize TrainScreen
	MyTrainScreen = TrainScreen()

	
	#set imagelogofile
	MyTrainScreen.imagelogofile = logopath + "logo.png" 
	
	#setvolume
	MyTrainScreen.msgvolume = msgvolume
	logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': Volume: '+str(msgvolume))
	
	#setuseofTFT
	logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': Use TFT: '+str(useTFT))
	MyTrainScreen.useTFT = useTFT

	#init Panel
	MyTrainScreen.InitPanel()
	
	
	#set active station
	MyTrainScreen.activestation = MyStations.GetActiveStation()
	MyTrainScreen.activestation.advertizemode = 0
	CheckAdvertize (MyTrainScreen.activestation)
	logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': '+"ActiveStation: "+MyTrainScreen.activestation.name)
	logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': '+"ActiveAd: " + MyTrainScreen.activestation.GetActiveAd().filename)

	#obsolete since use of disable_audio_dither=1 in /boot/config.txt
	MyTrainScreen.mixerinit=True 
	
	pygame.mixer.init()
	logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Mixer initiated")
	audiofile = audiopath+"Whistle1.ogg"
	MySound = pygame.mixer.Sound(audiofile)
	MySound.set_volume(MyTrainScreen.msgvolume)
	MySound.play(0,0,0)
	logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+': First whistle played ('+audiofile+') with volume ' + str(MyTrainScreen.msgvolume))

	MyTrainScreen.InitScreen()
	
	#check for latest logfile
	list_of_files = glob.glob('/mnt/koploper/*.txt') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)

	koploperlog = latest_file
	intteller=0
	
	latest=1
	x=0
	t0=time.time()
	logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': latest koploperfile: '+koploperlog)

	#main loop
	while True:
		if MyTrainScreen.activestation.advertizemode ==1:
			if MyTrainScreen.activestation.GetActiveAd().type == "MP4": 
				t0=0
		if time.time() - t0 > 5:
				CheckAdvertize(MyTrainScreen.activestation)
				if MyTrainScreen.activestation.advertizemode != 0:
					MyTrainScreen.activestation.advertizemode = 2
					MyTrainScreen.InitScreen()
					t0= time.time()
					logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': '+"New t0:" + strftime("%H:%M:%S",time.localtime(t0)))
				
		
		intteller +=1
		if intteller == 1000:
			intteller = 0
			#import os
			lines = tail_lines(koploperlog,50,1)
						
			#check logfile
			for line in lines:
				x=x+1
				if x > 0: 
					cols = line.strip().split("\t")
					if int(cols[0]) > latest:
						dt = datetime.timedelta(minutes=1)
						traintime = format(datetime.datetime.now() + dt,"%H:%M")
						newtraintime = traintime
						inputmessage = cols[2][-16:]
						if inputmessage[:3]=="msg":
							logging.info (strftime("%H:%M:%S",time.localtime(time.time()))+': Input from Koploper: '+inputmessage)
							#find routeinfo
							MyRouteInfo = RouteInfo()
							for MyRouteInfo in MyRouteInfos:
								if MyRouteInfo.message == inputmessage:
									if MyRouteInfo.type == "arrival":
										MyTrainScreen.TrainArrival(MyRouteInfo.trainid, newtraintime,MyRouteInfo.rail, MyRouteInfo.station, MyRouteInfo.audiofile)									
									elif MyRouteInfo.type == "departure":
										MyTrainScreen.TrainDeparture(MyRouteInfo.trainid, MyRouteInfo.station, MyRouteInfo.audiofile)

			latest = int(cols[0])
			
	
		nameof_killfile="stop_processx.txt"
		if os.path.exists(apppath+nameof_killfile): 
   	 		os.remove(nameof_killfile)
			exit()
			
		nameof_killfile="kill_pi.txt"
		if os.geteuid() != 0:
			if os.path.exists(apppath+nameof_killfile):
				os.system("sudo shutdown now")
				
		nameof_killfile="reboot_pi.txt"
		if os.geteuid() != 0:
			if os.path.exists(apppath+nameof_killfile):
				os.system("sudo reboot")
								
 
		event = pygame.event.poll()
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
			pygame.quit()
			exit()
		if (event.type == pygame.KEYDOWN) and (event.key == 0x100):
			MyStation = Station()
			for MyStation in MyStations:
				MyStation.SaveTrainsToIniFile(inipath)
	
			pygame.quit()
			if os.geteuid() != 0:
				exit()
			else:
				response = raw_input("What to do with other PI's? Reboot (1 or r), Shutdown (2 or s), Nothing (0 or n): ")
				if response =="2" or response == "s":
					os.system("cp " + inipath+"kill_pi.txt " + apppath+"kill_pi.txt")
				if response =="1" or response == "r":
					os.system("cp " + inipath+"reboot_pi.txt " + apppath+"reboot_pi.txt")
				response = raw_input("Quit app? (0=no, 1=yes)")
				if response =="1" or response == "y":
					nameof_killfile="kill_pi.txt"
					if os.path.exists(apppath+nameof_killfile):
   	 					os.remove(apppath+nameof_killfile)
					nameof_killfile="reboot_pi.txt"
					if os.path.exists(apppath+nameof_killfile):
   	 					os.remove(apppath+nameof_killfile)
					exit()
		

		#train 1 leaves of arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x101):
			MyTrain = Train()
			train = Train()
			
			for train in MyTrainScreen.activestation.trains:
				if train.position == 1:			
					if train.status == "Incoming":
						#trein vertrekt
						trainid = train.id
						dept=1
					else:
						#trein komt aan
						dept=0
						newtrainid = train.id
						dt = datetime.timedelta(minutes=1)
						traintime = format(datetime.datetime.now() + dt,"%H:%M")
						newtraintime = traintime
						newtrainrail = "1"				
			if dept==1:
				MyTrainScreen.TrainDeparture(trainid, MyTrainScreen.activestation.id,'')
			else:
				MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')
		
		#train 2 leaves of arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x102):
			MyTrain = Train()
			train = Train()
			
			for train in MyTrainScreen.activestation.trains:
				if train.position == 2:			
					if train.status == "Incoming":
						#trein vertrekt
						trainid = train.id
						dept=1
						
					else:
						#trein komt aan
						dept=0
						newtrainid = train.id
						dt = datetime.timedelta(minutes=1)
						traintime = format(datetime.datetime.now() + dt,"%H:%M")
						newtraintime = traintime
						newtrainrail = "1"				
			if dept==1:
				MyTrainScreen.TrainDeparture(trainid, MyTrainScreen.activestation.id,'')
			else:
				MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')


		#train 3 arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x103):
			MyTrain = Train()
			train = Train()
			for train in MyTrainScreen.activestation.trains:
				if train.position == 3:			
					newtrainid = train.id
			dt = datetime.timedelta(minutes=1)
			traintime = format(datetime.datetime.now() + dt,"%H:%M")
			newtraintime = traintime
			newtrainrail = "1"				
			MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')


		#train 4 arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x104):
			MyTrain = Train()
			train = Train()
			for train in MyTrainScreen.activestation.trains:
				if train.position == 4:			
					newtrainid = train.id
			dt = datetime.timedelta(minutes=1)
			traintime = format(datetime.datetime.now() + dt,"%H:%M")
			newtraintime = traintime
			newtrainrail = "2"				
			MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')

		#train 5 arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x105):
			MyTrain = Train()
			train = Train()
			for train in MyTrainScreen.activestation.trains:
				if train.position == 5:			
					newtrainid = train.id
			dt = datetime.timedelta(minutes=1)
			traintime = format(datetime.datetime.now() + dt,"%H:%M")
			newtraintime = traintime
			newtrainrail = "1"				
			MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')

	
		#train 6 arrives
		if (event.type == pygame.KEYDOWN) and (event.key == 0x106):
			MyTrain = Train()
			train = Train()
			for train in MyTrainScreen.activestation.trains:
				if train.position == 6:			
					newtrainid = train.id
			dt = datetime.timedelta(minutes=1)
			traintime = format(datetime.datetime.now() + dt,"%H:%M")
			newtraintime = traintime
			newtrainrail = "1"				
			MyTrainScreen.TrainArrival(newtrainid, newtraintime, newtrainrail, MyTrainScreen.activestation.id,'')

		#switch to next station
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_MULTIPLY):
			MyStation = Station()
			MyActiveStationID = MyTrainScreen.activestation.id
			if MyActiveStationID == 1:  NewActiveStationID = 2
			if MyActiveStationID == 2:  NewActiveStationID = 3
			if MyActiveStationID == 3:  NewActiveStationID = 1
			
			MyTrainScreen.activestation.active = False
			
			for MyStation in MyStations:
				if MyStation.id == NewActiveStationID: MyStation.active = True
			
			MyTrainScreen.activestation = MyStations.GetActiveStation()
			MyTrainScreen.activestation.advertizemode = 0
			MyTrainScreen.InitScreen()
			
			
		#volume up
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_PLUS):
			if MyTrainScreen.msgvolume <= 0.8:
				MyTrainScreen.msgvolume += .2
				#play bip
				MyTrainScreen.mixerinit = True
				pygame.mixer.init()
				audiofile = audiopath+"bip.ogg"
				MySound = pygame.mixer.Sound(audiofile)
				MySound.set_volume(MyTrainScreen.msgvolume)
				MySound.play(0,0,0)
				logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Volume increase to: " + str(MyTrainScreen.msgvolume))

				
			
		#volume down		
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_KP_MINUS):
			if MyTrainScreen.msgvolume >=0.2:
				MyTrainScreen.msgvolume -= .2
				#play bip
				MyTrainScreen.mixerinit = True
				pygame.mixer.init()
				audiofile = audiopath+"bip.ogg"
				MySound = pygame.mixer.Sound(audiofile)
				MySound.set_volume(MyTrainScreen.msgvolume)
				MySound.play(0,0,0)
				logging.info(strftime("%H:%M:%S",time.localtime(time.time()))+": Volume decrease to: " + str(MyTrainScreen.msgvolume))



if __name__ == '__main__':

		MyStations = StationCollection()
		MyRouteInfos = RouteInfoCollection()
		MyTrainTypes = TrainTypeCollection()

		config = ConfigParser()

		if os.path.exists('DevErrors.log'): 
   	 		os.remove('DevErrors.log')


		logging.basicConfig(level=logging.DEBUG, filename='DevErrors.log')
		t0=time.time()
		inipath=''
		
		try:
    			departureboard()
		except:
    			logging.exception("Error in departure-board:")
    	
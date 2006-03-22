# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os,sys
from baseConfig import pConfig

class pModules:
	
	modNames = []
	modInstances = []
	
	def __init__(self):
		self.loadModuleNames()
		self.instantiateModules()
		
	def loadModuleNames(self):
		# load the module names from the config file
		for mod in pConfig.getValues(pConfig.getNodes("base.module")):
			self.modNames.append(mod.strip())
		
	def instantiateModules(self):
		# import the modules the user wants
		# and instantiate the classes
		for mod in self.modNames:
			# set the necessary paths to import our modules
			sys.path = [os.getcwd()+"/modules/"+mod+"/"]+sys.path
			self.modInstances.append(__import__(mod).__dict__[mod]())
	
	# trigger routines before an event
	def triggerBefore(self, httpd, name):
		self.__hook(httpd, "before_"+name)
	
	# trigger routines after an event
	def triggerAfter(self, httpd, name):
		self.__hook(httpd, "after_"+name)
	
	# calls the routines assigned to the given hook
	def __hook(self, httpd, name):
		for mod in self.modInstances:
			if hasattr(mod, name) and getattr(mod, name)(httpd) == False:
				return
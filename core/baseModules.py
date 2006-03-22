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
		self.__loadModuleNames()
		self.__instantiateModules()
		
	def __loadModuleNames(self):
		"""
		Loads the module names from the config file.
		"""
		for mod in pConfig.getValues(pConfig.getNodes("base.module")):
			self.modNames.append(mod.strip())
		
	def __instantiateModules(self):
		"""
		Imports the modules the user wants and instantiates the module classes.
		"""
		for mod in self.modNames:
			# set the necessary paths to import our modules
			sys.path = [os.getcwd()+"/modules/"+mod+"/"]+sys.path
			self.modInstances.append(__import__(mod).__dict__[mod]())
	
	def triggerBefore(self, httpd, name):
	"""
	Calls the modules' routines before an event is triggered
	"""
		self.__hook(httpd, "before_"+name)
	
	def triggerAfter(self, httpd, name):
	"""
	Calls the modules' routines after an event is triggered
	"""
		self.__hook(httpd, "after_"+name)
	
	def __hook(self, httpd, name):
	"""
	Calls the routines assigned to the given hook.
	"""
		for mod in self.modInstances:
			if hasattr(mod, name) and getattr(mod, name)(httpd) == False:
				return
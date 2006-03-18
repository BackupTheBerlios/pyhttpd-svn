# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os,sys
from baseConfig import pConfig

class pModules:
	def __init__(self):
		# load the module names from the config file
		mods = []
		for mod in pConfig.getNodes("base.modules.module"):
			mods.append(mod.firstChild.nodeValue.strip())
		
		# import the modules the user wants
		# and instantiate the classes
		self.modules = []
		for mod in mods:
			# set the necessary paths to import our modules
			sys.path = [os.getcwd()+"/modules/"+mod+"/"]+sys.path
			self.modules.append(__import__(mod).__dict__[mod]())
	
	# calls the routines assigned to the given hook
	def hook(self, httpd, name):
		for mod in self.modules:
			if hasattr(mod, name) and getattr(mod, name)(httpd) == False:
				return
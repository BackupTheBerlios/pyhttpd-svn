##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os,sys,inspect

sys.path = [os.getcwd()+"/modules/"]+sys.path

class pModules:
	configfile = ""
	directory = ""
	modules = []
	
	def __init__(self, configfile="config/modules", directory="modules/"):
		self.configfile = configfile
		
		fd = open(self.configfile)
		
		mods = []
		for line in fd:
			if line.strip() != "" and not line.strip().startswith("#"):
				mods.append(line.strip())
				
		fd.close()
		
		# import the modules the user wants
		# and instantiate the classes
		for mod in mods:
			self.modules.append(__import__(mod).__dict__[mod]())
	
	def hook(self, httpd, name):
		for mod in self.modules:
			if hasattr(mod, name) and getattr(mod, name)(httpd) == False:
				return
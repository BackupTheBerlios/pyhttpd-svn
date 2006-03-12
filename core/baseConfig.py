##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from xml.dom import minidom

class pConfig:
	configdata = {}
	
	def loadConfiguration(self):
		xmldoc = minidom.parse("config/config.xml")
		for config in xmldoc.firstChild.childNodes:
			if config.nodeType == 1:
				self.configdata[str(config.nodeName.upper())] = str(config.firstChild.nodeValue)
		
		self.configdata["SERVROOT"] = os.getcwd()
	loadConfiguration = classmethod(loadConfiguration)
	
	def getAttr(self, name):
		if self.configdata.has_key(name.upper()):
			return self.configdata[name.upper()]
		else:
			raise AttributeError, name
	getAttr = classmethod(getAttr)
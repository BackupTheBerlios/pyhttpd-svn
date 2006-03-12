##################################################################
#	PyWeb
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from baseConfig import pConfig

class dirindex:
	configfile = ""
	indexes = []
	
	def __init__(self, configfile="config/dirindex"):
		self.configfile = configfile
		
		fd = open(self.configfile)
		
		for line in fd:
			if line.strip() != "" and not line.strip().startswith("#"):
				self.indexes.append(line.strip())
		
		fd.close()

	def before_GET(self, httpd):
		if httpd.path.endswith("/"):
			httpd.path += self.findIndexFile(pConfig.getAttr("docroot")+httpd.path);
	
	def findIndexFile(self, directory):
		files = os.listdir(directory)
		for index in self.indexes:
			if index in files:
				return index
		
		return ""
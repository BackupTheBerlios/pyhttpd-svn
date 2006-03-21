# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from baseConfig import pConfig

class dirindex:
	def __init__(self):
		# read the directory indexes from the config file
		self.indexes = pConfig.getValues(pConfig.getNodes("dirindex.index"))

	def before_GET(self, httpd):
		if httpd.path.endswith("/"):
			httpd.path += self.findIndexFile(pConfig.getValue("base.docroot")+httpd.path);
	
	def findIndexFile(self, directory):
		files = os.listdir(directory)
		for index in self.indexes:
			if index in files:
				return index
		
		return ""
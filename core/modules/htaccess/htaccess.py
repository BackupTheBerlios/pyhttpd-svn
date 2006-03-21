# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id: htaccess.py 26 2006-03-18 15:30:40Z twenty-three $
#	(c) 2006 by Tim Taubert
##################################################################

import os
from xml.dom import minidom

from baseConfig import pConfig

class htaccess:
	active = False
	
	def __init__(self):
		return
	
	def before_GET(self, httpd):
		htfile = self.findhtaccessFile(pConfig.getValue("base.docroot")+httpd.path)
		if htfile:
			parsehtaccessFile(self, htfile)
			active = True
	
	def findhtaccessFile(self, path):
		if not os.path.isdir(path) or path.endswith("/"):
			path = "/".join(path.split("/")[:-1])
		while os.path.isdir(path):
			if os.path.isfile(path+"/.htaccess"):
				return path+"/.htaccess"
			path = "/".join(path.split("/")[:-1])
		return False
	
	def parsehtaccessFile(self, htfile):
		xmldoc = minidom.parse(htfile)
		xmldoc = xmldoc.getElementsByTagName("config")[0]
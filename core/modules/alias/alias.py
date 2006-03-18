# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

from baseConfig import pConfig

class alias:
	def __init__(self):
		self.aliases = {}
		for alias in pConfig.getNodes("aliases.alias"):
			key = alias.getElementsByTagName("path")[0].firstChild.nodeValue.strip()
			val = alias.getElementsByTagName("target")[0].firstChild.nodeValue.strip()
			self.aliases[key] = val
	
	def before_GET(self, httpd):
		for (key, val) in self.aliases.items():
			if httpd.path.startswith(key):
				return False
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
			key, val = [pConfig.getValue("source", alias), pConfig.getValue("target", alias)]
			self.aliases[key] = val
	
	def before_GET(self, httpd):
		for (key, val) in self.aliases.items():
			if httpd.path.startswith(key):
				return False
# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from xml.dom import minidom

class pConfig:
	def loadConfiguration(self):
		self.xmldoc = minidom.parse("config/config.xml")
		self.xmldoc = self.xmldoc.getElementsByTagName("config")[0]
		
		self.filterNodes(self.xmldoc)
		
		#print self.getNodes("base.modules.module")[0].firstChild.nodeValue
	loadConfiguration = classmethod(loadConfiguration)
	
	def filterNodes(self, nodes):
		for node in nodes.childNodes:
			if node.nodeType != 1:
				nodes.removeChild(node)
			else:
				self.filterNodes(node)
	filterNodes = classmethod(filterNodes)
	
	def getValue(self, path):
		paths = path.split(".")
		node = self.xmldoc
		for p in paths:
			node = node.getElementsByTagName(p)
			if not node:
				raise AttributeError, p
				break
			node = node[0]
		return node.firstChild.nodeValue
	getValue = classmethod(getValue)

	def getNodes(self, path):
		paths = path.split(".")
		node = self.xmldoc
		for p in paths[:-1]:
			node = node.getElementsByTagName(p)
			if not node:
				raise AttributeError, p
				break
			node = node[0]
		return node.getElementsByTagName(paths[-1])
	getNodes = classmethod(getNodes)
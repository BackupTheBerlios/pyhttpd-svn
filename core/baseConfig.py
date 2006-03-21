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
	loadConfiguration = classmethod(loadConfiguration)
	
	def getValue(self, path, node=None):
		if not node:
			node = self.xmldoc
		
		for p in path.split("."):
			node = node.getElementsByTagName(p)
			if not node:
				raise AttributeError, p
				break
			node = node[0]
		return node.firstChild.nodeValue
	getValue = classmethod(getValue)
	
	def getValues(self, nodes):
		values = []
		for child in nodes:
			values.append(child.firstChild.nodeValue)
		
		return values
	getValues = classmethod(getValues)
	
	def getNode(self, path, node=None):
		if not node:
			node = self.xmldoc
		
		for p in path.split("."):
			node = node.getElementsByTagName(p)
			if not node:
				raise AttributeError, p
				break
			node = node[0]
		return node
	getNode = classmethod(getNode)

	def getNodes(self, path, node=None):
		if not node:
			node = self.xmldoc
			
		paths = path.split(".")
		for p in paths[:-1]:
			node = node.getElementsByTagName(p)
			if not node:
				raise AttributeError, p
				break
			node = node[0]
		return node.getElementsByTagName(paths[-1])
	getNodes = classmethod(getNodes)
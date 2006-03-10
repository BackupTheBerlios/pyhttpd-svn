##################################################################
#	PyWeb
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
import myBaseHTTPServer
import mimetypes

from baseConfig import pConfig
import baseHeaders
import baseRoutines

class pHTTPRequestHandler(myBaseHTTPServer.BaseHTTPRequestHandler):
	cookies = {}
	postdata = {}
	
	def do_GET(self):
		self.handleFileFlag = True
		
		baseRoutines.parsePaths(self)
		baseHeaders.parseHeaders(self)
		self.modules.hook(self, "before_GET")

		'''if self.path.find("?") > -1:
			name, data = self.path.split("?")
			self.path = name
			baseHeaders.parseGETData(self, data)'''
		
		if not os.path.isfile(self.path):
			if os.path.isfile(pConfig.getAttr("docroot")+self.path):
				self.path = pConfig.getAttr("docroot")+self.path
			elif os.path.isfile(pConfig.getAttr("docroot")+"/"+self.path):
				self.path = pConfig.getAttr("docroot")+"/"+self.path
			else:
				self.send_response(400)
				self.end_headers()
				self.handleFileFlag = False
		
		if self.handleFileFlag:
			self.handleFile(self.path)
		
		self.modules.hook(self, "after_GET")
	
	def do_POST(self):
		baseHeaders.parseHeaders(self)
		baseHeaders.parsePOSTData(self)
		if not self.modules.hook(self, "before_POST"):
			return
		
		if self.path.endswith("/"):
			dirIndex = pDirIndex()
			filename = dirIndex.findIndexFile(pConfig.getAttr("docroot")+self.path);
		else:
			filename = pConfig.getAttr("docroot")+self.path
		
		self.handleFile(filename)
		
		if not self.modules.hook(self, "after_POST"):
			return

	def handleFile(self, filename):
		fd = open(filename)
		content = fd.read()
		fd.close()
		self.send_response(200)
		
		mime = mimetypes.MimeTypes()
		mimetype = mime.guess_type(filename)
		self.send_header("Content-Type", mimetype[0])
		if mimetype[1]:
			self.send_header("Content-Encoding", mimetype[1])
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		self.wfile.write(content)
		self.wfile.flush()
##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from baseHTTPServer import BaseHTTPRequestHandler
from mimetypes import MimeTypes

from baseConfig import pConfig
import baseHeaders
import baseRoutines

class pHTTPRequestHandler(BaseHTTPRequestHandler):
	#cookies = {}
	#postdata = ""

	# Make rfile unbuffered -- we need to read one line and then pass
	# the rest to a subprocess, so we can't use buffered input.
	rbufsize = 0
	
	def do_HEAD(self):
		print "HEAD cmd used"
	
	def do_PUT(self):
		print "PUT cmd used"
	
	def do_GET(self):
		self.handleCommand()
	
	def do_POST(self):
#		baseHeaders.parsePOSTData(self)
		self.handleCommand()

	def handleCommand(self):
		self.handleFileFlag = True
		
		baseRoutines.parsePaths(self)
		#baseHeaders.parseHeaders(self)
		
		# trigger the "before" hook
		self.modules.hook(self, "before_"+self.command)

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
			try:
				self.handleFile(self.path)
			except:
				pass
		
		# trigger the "after" hook
		self.modules.hook(self, "after_"+self.command)

	def handleFile(self, filename):
		fd = open(filename)
		content = fd.read()
		fd.close()
		
		self.send_response(200)
		
		mime = MimeTypes()
		mimetype = mime.guess_type(filename)
		self.send_header("Content-Type", mimetype[0])
		if mimetype[1]:
			self.send_header("Content-Encoding", mimetype[1])
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		self.wfile.write(content)
		self.wfile.flush()
# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os,select
from baseConfig import pConfig

class cgihandler:
	def __init__(self):
		return
	
	def before_GET(self, httpd):
		self.processFile(httpd)
		
	def before_POST(self, httpd):
		self.processFile(httpd)
		
	def processFile(self, httpd):
		ext = httpd.path.split(".")[-1]
		handler = self.findCGIHandler(httpd, ext)
		
		if handler:
			self.parseFile(httpd, handler)
			
			# the main routine shouldn't process the file anymore
			httpd.handleFileFlag = False
			return False
		
	def findCGIHandler(self, httpd, ext):
		for handler in pConfig.getNodes("cgihandler.handler"):
			for ext in pConfig.getValues(pConfig.getNodes("ext", handler)):
				if httpd.path.endswith(ext):
					# return path to the interpreter
					return pConfig.getValue("int" ,handler)
		# no handler was found
		return None
	
	def parseFile(self, httpd, handler):
		env = {}
		env["SERVER_SOFTWARE"]	= pConfig.getValue("base.software")
		env["SERVER_NAME"]		= "localhost"
		env["GATEWAY_INTERFACE"]= "CGI/1.1"
		
		env["SERVER_PROTOCOL"]	= "HTTP/1.1"
		env["SERVER_PORT"]		= pConfig.getValue("base.port")
		env["REQUEST_METHOD"]	= httpd.command
		
		env["PATH_INFO"]		= os.path.dirname(httpd.path)
		env["PATH_TRANSLATED"]	= os.path.dirname(pConfig.getValue("base.docroot")+httpd.path)
		env["QUERY_STRING"]		= httpd.query
		
		env["REMOTE_ADDR"]		= "127.0.0.1"
		env["REMOTE_HOST"]		= ""
		
		env["AUTH_TYPE"]		= ""
		env["REMOTE_IDENT"] 	= ""
		env["REMOTE_USER"]		= ""

		length = httpd.headers.getheader("content-length")
		if length:
			env["CONTENT_LENGTH"]	= length
			env["CONTENT_TYPE"]		= httpd.headers.getheader("content-type")
		else:
			env["CONTENT_LENGTH"]	= ""
			env["CONTENT_TYPE"]		= ""
		
		#env["REQUEST_TIME"]	= ""
		#env["REMOTE_PORT"]		= ""
		
		env["SCRIPT_NAME"]		= httpd.path
		env["REQUEST_URI"]		= httpd.path
		env["DOCUMENT_ROOT"]	= pConfig.getValue("base.docroot")
		env["SERVER_ADMIN"]		= pConfig.getValue("base.admin")
		env["SCRIPT_FILENAME"]	= pConfig.getValue("base.docroot")+httpd.path
		
		# collect the headers additionally sent by the user
		for key in httpd.headers.keys():
			newkey = key.upper().replace("-","_")
			if not env.has_key(newkey):
				env["HTTP_"+newkey] = httpd.headers.getheader(key)
		
		os.environ.update(env)
		
		httpd.wfile.flush()

		# fork and pipe our cgi data
		r, w = os.pipe()
		
		pid = os.fork()
		if pid:
			# main process
			# read the pipe
			os.close(w)
			r = os.fdopen(r)
			output = r.read()
			
			pid, sts = os.waitpid(pid, 0)
		else:
			# child process
			# if there is client data then pipe it
			if length:
				os.dup2(httpd.rfile.fileno(), 0)
			
			# create the pipes
			os.close(r)
			w = os.fdopen(w, "w")
			os.dup2(w.fileno(), 1)
			os.execve(handler, [handler, pConfig.getValue("base.docroot")+httpd.path], os.environ)
		
		# if there is client data then throw away additional data
		if length:
			while select.select([httpd.rfile], [], [], 0)[0]:
				if not httpd.rfile.read(1):
					break
		
		# process the php output
		status = ""
		for line in output.split("\n"):
			if line == "":
				break
			if line.startswith("Status: "):
				status = line.split(" ")[1]
				break
		
		# sent data to the browser
		if status:
			httpd.send_response(int(status))
		else:
			httpd.send_response(200, "Script output follows")
		httpd.wfile.write(output)
		httpd.wfile.flush()
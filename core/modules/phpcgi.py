##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import os
from baseConfig import pConfig

class phpcgi:
	def __init__(self):
		return
	
	def before_GET(self, httpd):
		self.processFile(httpd)
		
	def before_POST(self, httpd):
		self.processFile(httpd)
		
	def processFile(self, httpd):
		if httpd.path.endswith(".php"):
			self.parseFile(httpd)
			
			# the main routine shouldn't process the file anymore
			httpd.handleFileFlag = False
			return False
	
	def parseFile(self, httpd):
		env = {}
		env["SERVER_SOFTWARE"]	= pConfig.getAttr("software")
		env["SERVER_NAME"]		= "localhost"
		env["GATEWAY_INTERFACE"]= "CGI/1.1"
		
		env["SERVER_PROTOCOL"]	= "HTTP/1.1"
		env["SERVER_PORT"]		= pConfig.getAttr("port")
		env["REQUEST_METHOD"]	= httpd.command
		
		env["PATH_INFO"]		= os.path.dirname(httpd.path)
		env["PATH_TRANSLATED"]	= os.path.dirname(pConfig.getAttr("docroot")+httpd.path)
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
		env["PHP_SELF"]			= httpd.path
		env["DOCUMENT_ROOT"]	= pConfig.getAttr("docroot")
		env["SERVER_ADMIN"]		= pConfig.getAttr("admin")
		env["SCRIPT_FILENAME"]	= pConfig.getAttr("docroot")+httpd.path
		
		# collect the headers additionally sent by the user
		for key in httpd.headers.keys():
			newkey = key.upper().replace("-","_")
			if not env.has_key(newkey):
				env["HTTP_"+newkey] = httpd.headers.getheader(key)
		
		os.environ.update(env)
		httpd.send_response(200, "Script output follows")
		
		httpd.wfile.flush()
		
		# fork and pipe our cgi data
		pid = os.fork()
		if pid:
			# main process
			pid, sts = os.waitpid(pid, 0)
		else:
			# child process
			os.dup2(httpd.rfile.fileno(), 0)
			os.dup2(httpd.wfile.fileno(), 1)
			os.execve("/usr/bin/php-cgi", ["php-cgi"], os.environ)
##################################################################
#	PyWeb
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

from baseConfig import pConfig
from baseHTTPServer import HTTPServer
from baseRequestHandler import pHTTPRequestHandler
from baseModules import pModules

if __name__ == "__main__":
	# load configuration data
	pConfig.loadConfiguration()
	
	# start main server thread
	httpd = HTTPServer(('',int(pConfig.getAttr("port"))), pHTTPRequestHandler)
	
	# load modules
	pHTTPRequestHandler.modules = pModules()
	
	# let the server serve
	httpd.serve_forever()
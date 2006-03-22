# -*- coding: utf-8 -*-

##################################################################
#	PyWeb
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

from baseConfig import pConfig
from baseSocketServer import BaseServer
from baseHTTPServer import BaseHTTPRequestHandler
from baseModules import pModules

if __name__ == "__main__":
	# load configuration data
	pConfig.loadConfiguration()
	
	# start main server thread
	httpd = BaseServer(('',int(pConfig.getValue("base.port"))), BaseHTTPRequestHandler)
	
	# load modules
	BaseHTTPRequestHandler.modules = pModules()
	
	# let the server serve
	httpd.serve_forever()
##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import time

class user:
	logintime = 0
	ipaddr = ""
	
	def __init__(self, httpd):
		self.logintime = time.localtime()
		self.ipaddr = httpd.address_string()
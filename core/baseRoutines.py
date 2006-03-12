##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

def parsePaths(httpd):
	# parse query string
	if httpd.path.find("?") > -1:
		httpd.path, httpd.query = httpd.path.split("?")
	else:
		httpd.query = ""
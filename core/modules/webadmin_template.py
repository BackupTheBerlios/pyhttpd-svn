##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

PREFIX = "modules/templates/"

def getTemplate(name, variables):
	return parseTemplate(PREFIX+name+".tpl", variables)

def parseTemplate(filename, variables):
    return open(filename, 'r').read() % variables
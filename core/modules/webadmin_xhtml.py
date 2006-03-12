##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import webadmin_template

def sendPage(httpd, xhtml):
	httpd.send_response(200,"OK")
	httpd.send_header("Content-Type", "application/xhtml+xml; charset=UTF-8")
	httpd.send_header("Content-Length", str(len(xhtml)))
	httpd.end_headers()
	
	httpd.wfile.write(xhtml)
	httpd.wfile.flush()

def showLogin(httpd):
	xhtml = webadmin_template.getTemplate("login",{"title":"PyWebAdmin","version":"0.0.1"})
	sendPage(httpd, xhtml)

def showIndex(httpd):
	xhtml = webadmin_template.getTemplate("index",{"title":"PyWebAdmin","version":"0.0.1"})
	sendPage(httpd, xhtml)
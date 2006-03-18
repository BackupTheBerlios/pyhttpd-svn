##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import webadmin_login,webadmin_xhtml

WEBADMIN_ROOT	= "/webadmin/"
COOKIE			= "pyHTTPdWebAdminUUID"

class webadmin:
	sessions = {}
	
	def __init__(self):
		return
	
	def before_GET(self, httpd):
		if httpd.path.startswith(WEBADMIN_ROOT):
			# user already logged in?
			if httpd.cookies.has_key(COOKIE) and self.sessions.has_key(httpd.cookies[COOKIE]) and webadmin_login.checkLogin(httpd, self):
				action = httpd.path.split("/")[2]
				if action == "":
					webadmin_xhtml.showIndex(httpd)
			else:
				webadmin_xhtml.showLogin(httpd)
	
	def before_POST(self, httpd):
		if httpd.path.startswith(WEBADMIN_ROOT):
			action = httpd.path.split("/")[2]
			if action == "login":
				if httpd.postdata.has_key("user") and httpd.postdata.has_key("pass"):
					webadmin_login.userLogin(httpd, self)
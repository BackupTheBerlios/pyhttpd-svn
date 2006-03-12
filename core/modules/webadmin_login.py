##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import time,random,md5
import webadmin_user

def generateUUID():
	a = long(time.time() * 1000)
	b = long(random.random() * 100000000000000000L)
	c = long(random.random() * 100000000000000000L)
	
	uuid = md5.md5(str(a)+str(b)+str(c)).hexdigest()
	
	return uuid

def userLogin(httpd, webadmin):
	username = httpd.postdata["user"]
	password = httpd.postdata["pass"]
	
	if username == "admin" and password == "test":
		uuid = generateUUID()
		webadmin.sessions[uuid] = webadmin_user.user(httpd)
		
		# set cookie and redirect
		httpd.send_response(302,"Found")
		httpd.send_header("Set-Cookie", "PyWebAdminUUID="+uuid+"; path=/;")
		httpd.send_header("Location","/webadmin/")
		httpd.end_headers()

def checkLogin(httpd, webadmin):
	uuid = httpd.cookies["PyWebAdminUUID"]
	user = webadmin.sessions[uuid]
	if user.ipaddr == httpd.address_string():
		return True
	else:
		return False
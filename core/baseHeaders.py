# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

'''
def parseHeaders(httpd):
	parseCookies(httpd)
	
def parseCookies(httpd):
	cookies = httpd.headers.getheader("cookie")
	if cookies:
		cookies = cookies.split(";")
		for cookie in cookies:
			name, value = cookie.strip().split("=")
			httpd.cookies[name] = value

def parsePOSTData(httpd):
	clen = httpd.headers.getheader("content-length")
	httpd.posttype = httpd.headers.getheader("content-type")
	if clen:
		httpd.postdata = httpd.rfile.read(int(clen))

def parseGETData(httpd, data):
	parseValues(httpd, data)

def parseValues(data):
	postdata = {}
	fields = data.split("&")
	for field in fields:
		print field
		name, value = field.split("=")
		postdata[name] = value
	return postdata
'''
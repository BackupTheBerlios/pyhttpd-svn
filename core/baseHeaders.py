##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

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
	if clen:
		data = httpd.rfile.read(int(clen))
		parseValues(httpd, data)

def parseGETData(httpd, data):
	parseValues(httpd, data)

def parseValues(httpd, data):
	fields = data.split("&")
	for field in fields:
		name, value = field.split("=")
		httpd.postdata[name] = value
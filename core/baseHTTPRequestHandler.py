# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import	os, sys, socket, time, mimetools
from	mimetypes	import MimeTypes

from	baseConfig	import pConfig
import	baseRoutines

DEFAULT_ERROR_MESSAGE =	"<head><title>Error response</title></head><body><h1>Error response</h1><p>Error code %(code)d.</p><p>Message: %(message)s.</p><p>Error code explanation: %(code)s = %(explain)s.</body>"

def _quote_html(html):
	return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class pHTTPRequestHandler:
	
	rbufsize = 0
	wbufsize = 0

	sys_version			= "Python/2.4"
	server_version		= "BaseHTTP/"
	protocol_version	= "HTTP/1.0"
	
	# message-like class used to parse headers
	MessageClass = mimetools.Message
	
	# needed for timestamp formatting
	weekdayname	= ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	monthname	= [None,
					'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
					'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	
	# standard conform http response codes
	responses = {
		100: ('Continue', 'Request received, please continue'),
		101: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'),
		
		200: ('OK', 'Request fulfilled, document follows'),
		201: ('Created', 'Document created, URL follows'),
		202: ('Accepted', 'Request accepted, processing continues off-line'),
		203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
		204: ('No response', 'Request fulfilled, nothing follows'),
		205: ('Reset Content', 'Clear input form for further input.'),
		206: ('Partial Content', 'Partial content follows.'),
		
		300: ('Multiple Choices', 'Object has several resources -- see URI list'),
		301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
		302: ('Found', 'Object moved temporarily -- see URI list'),
		303: ('See Other', 'Object moved -- see Method and URL list'),
		304: ('Not modified', 'Document has not changed since given time'),
		305: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'),
		307: ('Temporary Redirect', 'Object moved temporarily -- see URI list'),
		
		400: ('Bad request', 'Bad request syntax or unsupported method'),
		401: ('Unauthorized', 'No permission -- see authorization schemes'),
		402: ('Payment required', 'No payment -- see charging schemes'),
		403: ('Forbidden', 'Request forbidden -- authorization will not help'),
		404: ('Not Found', 'Nothing matches the given URI'),
		405: ('Method Not Allowed', 'Specified method is invalid for this server.'),
		406: ('Not Acceptable', 'URI not available in preferred format.'),
		407: ('Proxy Authentication Required', 'You must authenticate with this proxy before proceeding.'),
		408: ('Request Time-out', 'Request timed out; try again later.'),
		409: ('Conflict', 'Request conflict.'),
		410: ('Gone', 'URI no longer exists and has been permanently removed.'),
		411: ('Length Required', 'Client must specify Content-Length.'),
		412: ('Precondition Failed', 'Precondition in headers is false.'),
		413: ('Request Entity Too Large', 'Entity is too large.'),
		414: ('Request-URI Too Long', 'URI is too long.'),
		415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
		416: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'),
		417: ('Expectation Failed', 'Expect condition could not be satisfied.'),
		
		500: ('Internal error', 'Server got itself in trouble'),
		501: ('Not Implemented', 'Server does not support this operation'),
		502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
		503: ('Service temporarily overloaded', 'The server cannot process the request due to a high load'),
		504: ('Gateway timeout', 'The gateway server did not receive a timely response'),
		505: ('HTTP Version not supported', 'Cannot fulfill request.'),
	}
	
###################################################################################
	
	def __init__(self, request, client_address, server):
		self.request = request
		self.client_address = client_address
		self.server = server
		try:
			self.setup()
			self.handle()
			self.finish()
		finally:
			sys.exc_traceback = None    # Help garbage collection
			
	def setup(self):
		self.connection	= self.request
		self.rfile		= self.connection.makefile('rb', self.rbufsize)
		self.wfile		= self.connection.makefile('wb', self.wbufsize)
	
	def finish(self):
		if not self.wfile.closed:
			self.wfile.flush()
		self.wfile.close()
		self.rfile.close()
	
	def do_HEAD(self):
		print "HEAD cmd used"
	
	def do_PUT(self):
		print "PUT cmd used"
	
	def do_GET(self):
		self.handleCommand()
	
	def do_POST(self):
		self.handleCommand()
	
	def handleCommand(self):
		self.handleFileFlag = True
		
		baseRoutines.parsePaths(self)
		
		# trigger the "before" hook
		self.modules.triggerBefore(self, self.command)
		
		if not os.path.isfile(self.path):
			if os.path.isfile(pConfig.getValue("base.docroot")+self.path):
				self.path = pConfig.getValue("base.docroot")+self.path
			elif os.path.isfile(pConfig.getValue("base.docroot")+"/"+self.path):
				self.path = pConfig.getValue("base.docroot")+"/"+self.path
			else:
				self.send_response(404)
				self.end_headers()
				self.handleFileFlag = False
		
		if self.handleFileFlag:
			try:
				self.handleFile(self.path)
			except:
				pass
		
		# trigger the "after" hook
		self.modules.triggerAfter(self, self.command)

	def handleFile(self, filename):
		fd = open(filename)
		content = fd.read()
		fd.close()
		
		self.send_response(200)
		
		mime = MimeTypes()
		mimetype = mime.guess_type(filename)
		self.send_header("Content-Type", mimetype[0])
		if mimetype[1]:
			self.send_header("Content-Encoding", mimetype[1])
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		self.wfile.write(content)
		self.wfile.flush()

	def parse_request(self):
		self.command = None  # set in case of error on the first line
		self.request_version = version = "HTTP/0.9" # Default
		self.close_connection = 1
		requestline = self.raw_requestline
		if requestline[-2:] == '\r\n':
			requestline = requestline[:-2]
		elif requestline[-1:] == '\n':
			requestline = requestline[:-1]
		self.requestline = requestline
		words = requestline.split()
		if len(words) == 3:
			[command, path, version] = words
			if version[:5] != 'HTTP/':
				self.send_error(400, "Bad request version (%r)" % version)
				return False
			try:
				base_version_number = version.split('/', 1)[1]
				version_number = base_version_number.split(".")
				if len(version_number) != 2:
					raise ValueError
				version_number = int(version_number[0]), int(version_number[1])
			except (ValueError, IndexError):
				self.send_error(400, "Bad request version (%r)" % version)
				return False
			if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
				self.close_connection = 0
			if version_number >= (2, 0):
				self.send_error(505,
							"Invalid HTTP Version (%s)" % base_version_number)
				return False
		elif len(words) == 2:
			[command, path] = words
			self.close_connection = 1
			if command != 'GET':
				self.send_error(400,
								"Bad HTTP/0.9 request type (%r)" % command)
				return False
		elif not words:
			return False
		else:
			self.send_error(400, "Bad request syntax (%r)" % requestline)
			return False
		self.command, self.path, self.request_version = command, path, version
	
		# Examine the headers and look for a Connection directive
		self.headers = self.MessageClass(self.rfile, 0)
	
		conntype = self.headers.get('Connection', "")
		if conntype.lower() == 'close':
			self.close_connection = 1
		elif (conntype.lower() == 'keep-alive' and
				self.protocol_version >= "HTTP/1.1"):
			self.close_connection = 0
		return True
	
	def handle_one_request(self):
		self.raw_requestline = self.rfile.readline()
		if not self.raw_requestline:
			self.close_connection = 1
			return
		if not self.parse_request(): # An error code has been sent, just exit
			return
		mname = 'do_' + self.command
		if hasattr(self, mname):
			getattr(self, mname)()
		else:
			self.send_error(501, "Unsupported method (%r)" % self.command)
	
	def handle(self):
		self.close_connection = 1
	
		self.handle_one_request()
		while not self.close_connection:
			self.handle_one_request()
	
	def send_error(self, code, message=None):
		try:
			short, long = self.responses[code]
		except KeyError:
			short, long = '???', '???'
		if message is None:
			message = short
		explain = long
		self.log_error("code %d, message %s", code, message)
		# using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
		content = (self.error_message_format %
					{'code': code, 'message': _quote_html(message), 'explain': explain})
		self.send_response(code, message)
		self.send_header("Content-Type", "text/html")
		self.send_header('Connection', 'close')
		self.end_headers()
		if self.command != 'HEAD' and code >= 200 and code not in (204, 304):
			self.wfile.write(content)
	
	error_message_format = DEFAULT_ERROR_MESSAGE
	
	def send_response(self, code, message=None):
		self.log_request(code)
		if message is None:
			if code in self.responses:
				message = self.responses[code][0]
			else:
				message = ''
		if self.request_version != 'HTTP/0.9':
			self.wfile.write("%s %d %s\r\n" %
								(self.protocol_version, code, message))
			# print (self.protocol_version, code, message)
		self.send_header('Server', self.version_string())
		self.send_header('Date', self.date_time_string())
	
	def send_header(self, keyword, value):
		"""Send a MIME header."""
		if self.request_version != 'HTTP/0.9':
			self.wfile.write("%s: %s\r\n" % (keyword, value))
	
		if keyword.lower() == 'connection':
			if value.lower() == 'close':
				self.close_connection = 1
			elif value.lower() == 'keep-alive':
				self.close_connection = 0
	
	def end_headers(self):
		if self.request_version != 'HTTP/0.9':
			self.wfile.write("\r\n")
	
	def log_request(self, code='-', size='-'):
		self.log_message('"%s" %s %s', self.requestline, str(code), str(size))
	
	def log_error(self, *args):
		self.log_message(*args)
	
	def log_message(self, format, *args):
		sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))
	
	def version_string(self):
		return self.server_version + ' ' + self.sys_version
	
	# returns the current date and time formatted for a message header
	def date_time_string(self):
		now = time.time()
		year, month, day, hh, mm, ss, wd, y, z = time.gmtime(now)
		s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
				self.weekdayname[wd],
				day, self.monthname[month], year,
				hh, mm, ss)
		return s
	
	# returns the current time formatted for logging
	def log_date_time_string(self):
		now = time.time()
		year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
		s = "%02d/%3s/%04d %02d:%02d:%02d" % (
				day, self.monthname[month], year,
				hh, mm, ss)
		return s
	
	def address_string(self):
		host, port = self.client_address[:2]
		return socket.getfqdn(host)

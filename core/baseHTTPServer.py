# -*- coding: utf-8 -*-

##################################################################
#	pyHTTPd
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

import socket, sys, os, threading

class pHTTPServer:
	
	address_family = socket.AF_INET
	socket_type = socket.SOCK_STREAM
	request_queue_size = 5
	allow_reuse_address = False
	daemon_threads = False
	
	def __init__(self, server_address, RequestHandlerClass):
		self.server_address = server_address
		self.RequestHandlerClass = RequestHandlerClass
	
		self.socket = socket.socket(self.address_family, self.socket_type)
		self.server_bind()
		self.server_activate()
	
	def server_bind(self):
		if self.allow_reuse_address:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)
	
		host, port = self.socket.getsockname()[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port
	
	def server_activate(self):
		self.socket.listen(self.request_queue_size)
	
	def serve_forever(self):
		while 1:
			self.handle_request()
	
	def get_request(self):
		return self.socket.accept()
	
	def handle_request(self):
		try:
			request, client_address = self.get_request()
		except socket.error:
			return
		if self.verify_request(request, client_address):
			try:
				self.process_request(request, client_address)
			except:
				self.handle_error(request, client_address)
				self.close_request(request)
	
	def verify_request(self, request, client_address):
		return True
	
	def process_request_thread(self, request, client_address):
		try:
			self.finish_request(request, client_address)
			self.close_request(request)
		except:
			self.handle_error(request, client_address)
			self.close_request(request)
	
	def process_request(self, request, client_address):
		t = threading.Thread(target = self.process_request_thread,
								args = (request, client_address))
		if self.daemon_threads:
			t.setDaemon (1)
		t.start()
	
	def server_close(self):
		self.socket.close()
	
	def finish_request(self, request, client_address):
		self.RequestHandlerClass(request, client_address, self)
	
	def close_request(self, request):
		request.close()
	
	def fileno(self):
		return self.socket.fileno()
	
	def handle_error(self, request, client_address):
		print '-'*40
		print 'Exception happened during processing of request from',
		print client_address
		import traceback
		traceback.print_exc() # XXX But this goes to stderr!
		print '-'*40

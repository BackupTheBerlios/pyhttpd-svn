##################################################################
#	PyWeb
#	$Id$
#	(c) 2006 by Tim Taubert
##################################################################

class alias:
	configfile = ""
	aliases = {}
	
	def __init__(self, configfile="config/aliases"):
		self.configfile = configfile
		
		fd = open(self.configfile)
		
		for line in fd:
			if line.strip() != "" and not line.strip().startswith("#"):
				key, val = line.strip().split()
				self.aliases[key] = val
				
		fd.close()
	
	def before_GET(self, httpd):
		for (key, val) in self.aliases.items():
			if httpd.path.startswith(key):
				return False
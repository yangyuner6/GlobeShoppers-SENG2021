class Message(object):
	def __init__(self, sender, receiver, message, automated, time):
		self.sender = sender
		self.message = message
		self.receiver = receiver
		self.automated = automated
		self.time = time
		

	@property
	def getSender(self):
		return self._sender
	


	@property
	def getReceiver(self):
		return self._receiver
	

	
	@property
	def getMessage(self):
		return self._message


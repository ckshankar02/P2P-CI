import socket
import sys
import threading
import pickle


<<<<<<< HEAD
rfcList = []						#HOLDS THE LIST RFCS AND THE PEERS THAT HAVE THEM
rfcLock = threading.Lock()
activePeers = []					#HOLDS THE LIST OF ACTIVE PEERS IN THE P2P NETWORK
=======
rfcList = []
rfcLock = threading.Lock()
activePeers = []
>>>>>>> c1c6112ceb79c4cea60c349bac65f6b43810d582
peerLock = threading.Lock()

class clientHandler(threading.Thread):
	def __init__(self, newTuple):
		threading.Thread.__init__(self)
<<<<<<< HEAD
		self.status = ''
		self.client = newTuple[0]
		self.address = newTuple[1]
	
	
	#Message received from the Client is Parsed
	def parseMsg(self, decodedMsg):
		m1 = decodedMsg.split("\n")
		m2 = []
		for l in m1:
			m2.append(str(l).split(' '))
		title = ''
		for s in range(1,len(m2[3])):
			title = title+' '+m2[3][s]
		if(m2[0][0] in ('LIST')):
			return(m2[0][0], None, m2[1][1], m2[2][1], None, m2[0][1])
		else:
			return(m2[0][0], m2[0][2], m2[1][1], m2[2][1], title, m2[0][3])
	
	
	#Response to the Clients for all type of REQUESTS		
	def sendMsgToClient(self, status, appendMsg):
		preMsg = 'P2P-CI/1.0 '+status+'\n'+appendMsg
		self.client.send(bytes(preMsg,'UTF-8'))
	
	
	#Adding RFC to Server
	def addRfc(self,msg):
		status = '200 OK'
		rfcLock.acquire()
		rfcList.append((msg[1],msg[4],msg[2],msg[3]))
		rfcLock.release()	
		ack = 'RFC '+msg[1]+' '+msg[4]+' '+msg[2]+' '+msg[3]
		self.sendMsgToClient(status, ack)

		
	#Look Up Service
	def lookUpRfc(self, msg):
		listPeers = ''
		rfcNum = msg[1]
		sp = '<c>'
		for list in rfcList:
			if(list[0] == rfcNum):
				listPeers = listPeers+list[0]+sp+list[1]+sp+list[2]+sp+list[3]+'\n'		
				
		if len(listPeers) == 0:			#If the requested RFC is not available with any PEER in the network
			status = '404 Not Found'
		else:
			status = '200 OK'
		
		self.sendMsgToClient(status, listPeers)

	
	#Listing all the Active Peers
	def listAll(self, msg):
		status = '200 OK'
		listAll = ''
		sp = '<c>'
		for r in rfcList:
			listAll = listAll+r[0]+sp+r[1]+sp+r[2]+sp+r[3]+'\n'
		self.sendMsgToClient(status, listAll)
		
		
	#Client Connection Termination Handler	
	def  endClientHandler(self,addr):
		print('Client has closed the connection')
		activePeers.remove(addr)
		tempRfcList = list(rfcList)
		for r in tempRfcList:
			if r[2] == addr[0]:
				rfcList.remove(r)
		del tempRfcList
	
	
	def run(self):
		#Whenever a connection is opened with a client
		#a new entry is made in activePeers
		peerLock.acquire()
		activePeers.append(self.address)
		peerLock.release()
		
		#Loops to keep listening the client's request
		flag = 0		
		while flag == 0:
			try:
				receivedMsg = self.client.recv(1024)
			except ConnectionResetError:
				break;			
			decodedMsg = receivedMsg.decode('UTF-8')
			if len(decodedMsg) != 0:					#Checked to ensure connection close (CTRL+C)
				actualMsg = self.parseMsg(decodedMsg)
				if actualMsg[5] != 'P2P-CI/1.0':
					status = '505 P2P-CI Version Not Supported'
					self.sendMsgToClient(status, '')
				else:
					method = actualMsg[0]
					if method == 'ADD':
						self.addRfc(actualMsg)
					elif method == 'LOOKUP':
						self.lookUpRfc(actualMsg)
					elif method == 'LIST':
						self.listAll(actualMsg)
					else:
						status = '400 Bad Request'
						self.sendMsgToClient(status, '')
			else:
				flag = 1								#Flag is set to break the LOOP
				
		self.endClientHandler(self.address)				#Handles the Client Connection Termination
		self.client.close()
		
		
def main():
	#Creating Sockets to List on port 7734
=======
		self.client = newTuple[0]
		self.address = newTuple[1]
	
	def parseMsg(self, decodedMsg):
		m1 = decodedMsg.split("<cr><lf>")
		m2 = []
		for l in m1:
			m2.append(str(l).split("<sp>"))
		print(m2)
		if(m2[0][0] in ('ADD','LOOKUP')):
			return(m2[0][0], m2[0][2], m2[1][1], m2[2][1], m2[3][1])
		else:
			return(m2[0][0], m2[1][1], m2[2][1])
	
	def addRfc(self,msg):
		rfcLock.acquire()
		rfcList.append((msg[1],msg[4],msg[2],msg[3]))
		rfcLock.release()		

	
	def lookUpRfc(self, msg):
		listPeers=[]
		rfcNum = msg[1]
		for list in rfcList:
			if(list[0]==rfcNum):
				listPeers.append((list[2],list[3]))
		
		pickleDump = pickle.dumps(listPeers)
		self.client.send(pickleDump)
		
	def listAll(self, msg):
		peerInfoDump = pickle.dumps(activePeers)
		self.client.send(peerInfoDump)
	
	def run(self):
		peerLock.acquire()
		activePeers.append(self.address)
		peerLock.release()
		flag = 0
		while flag == 0:
			receivedMsg = self.client.recv(1024)
			decodedMsg = receivedMsg.decode('UTF-8')
			actualMsg = self.parseMsg(decodedMsg)
		
			if actualMsg[0] == 'ADD':
				self.addRfc(actualMsg)
			elif actualMsg[0] == 'LOOKUP':
				self.lookUpRfc(actualMsg)
			else:
				self.listAll(actualMsg)
		
		self.client.close()

def main():
>>>>>>> c1c6112ceb79c4cea60c349bac65f6b43810d582
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	host = socket.gethostname()
	port = 7734	
	soc.bind((host,port)) 
	soc.listen(5)

	while True:
		print("Waiting on new client....")
		c = clientHandler(soc.accept())
		c.start()

if __name__ == '__main__':
	main()
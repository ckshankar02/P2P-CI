import socket
import sys
import threading
import pickle


rfcList = []
rfcLock = threading.Lock()
activePeers = []
peerLock = threading.Lock()

class clientHandler(threading.Thread):
	def __init__(self, newTuple):
		threading.Thread.__init__(self)
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
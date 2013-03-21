import socket
import sys
import pickle
import threading

class requestor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()
	
	def run(self):
		cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostbyname('10.139.66.178')
		port = 7734
		cliSocket.connect((host,port))
		self.requestServer(cliSocket)
		
	def downloadRFC(self, listOfPeers, idx):
		
	
	def requestServer(self, cliSoc):
		flag = 0
		while flag == 0:
			print("1. Add RFC to Server \n2. Look Up an RFC \n3. Request Whole Index List \n4. Leave the Network")
			option = str(input("Option = "))
			if option == '1':
				self.sendRFCAddRequest(cliSoc)
			elif option == '2':
				self.lookUpRequest(cliSoc)
			elif option == '3':
				self.wholeIndexRequest(cliSoc)
			elif option == '4':
				#leaveNetwork(cliSoc)
				flag = 1
			else:
				print("Enter Proper Options. Please!!!")
	
	def sendRFCAddRequest(self, cliSoc):
		version = 'P2P-CI/1.0'
		sp = '<sp>'
		end = '<cr><lf>'
		method = 'ADD'
		RFC = 'RFC'+sp+str(input("RFC Number = "))
		host = 'Host:'+sp+socket.gethostbyname(socket.gethostname())
		port = 'Port:'+sp+str(5678)
		title = 'Title:'+sp+str(input("RFC title = "))
		
		sendMessage = method+sp+RFC+sp+version+end+host+end+port+end+title+end+end
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		
		
	def lookUpRequest(self, cliSoc):
		version = 'P2P-CI/1.0'
		sp = '<sp>'
		end = '<cr><lf>'
		method = 'LOOKUP'
		RFC = 'RFC'+sp+str(input("RFC Number = "))
		host = 'Host:'+sp+socket.gethostbyname(socket.gethostname())
		port = 'Port:'+sp+str(5678)
		title = 'Title:'+sp+str(input("RFC title = "))
		sendMessage = method+sp+RFC+sp+version+end+host+end+port+end+title+end+end
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		peerList = pickle.loads(cliSoc.recv(2048))
		#print(peerList)
		
		idx = 1
		print("#\tHost IP Address\tPort")
		for p in peerList:
			print("%d.\t%s\t%s"%(idx,p[0],p[1]))
			idx += 1
		print(str(idx)+". Don't want to download")
		option = input("option = ")
		while int(option) > len(peerList)+1:
			option = input("Enter Proper option = ") 
		if int(option) == idx:
			return
		else:
			self.downloadRFC(peerList, int(option))
		
		
	def wholeIndexRequest(self, cliSoc):
		version = 'P2P-CI/1.0'
		sp = '<sp>'
		end = '<cr><lf>'
		method = 'LIST'
		host = 'Host:'+sp+socket.gethostbyname(socket.gethostname())
		port = 'Port:'+sp+str(5678)		
		sendMessage = method+sp+version+end+host+end+port+end+end
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		entirePeerList = pickle.loads(cliSoc.recv(2048))
		print(entirePeerList)

class uploader(threading.Thread)
	def __init__(self, newTuple):
		threading.Thread.__init__(self)
		self.client = newTuple[0]
		self.address = newTuple[1]

	def parseMsg(self, decodedMsg)
		m1 = decodedMsg.split("<cr><lf>")
		m2 = []
		for l in m1:
			m2.append(str(l).split("<sp>"))
		print(m2)
		
		
		'''	if(m2[0][0] in ('GET')):
				return(m2[0][0], m2[0][2], m2[1][1], m2[2][1], m2[3][1])
			else:
				return(m2[0][0], m2[1][1], m2[2][1])'''
			
			
	def run(self)
		receivedMsg = self.client.recv(1024)
		decodedMsg = receivedMsg.decode('UTF-8')
		actualMsg = self.parseMsg(decodedMsg)
		
		
		
def main():	
	reqClient = requestor()	
	
	uploaderSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	host = socket.gethostname()
	port = 5678
	uploaderSoc.bind((host,port)) 
	uploaderSoc.listen(5)
	while True:
		print("Waiting on new client....")
		u =  uploader(uploaderSoc.accept())
		u.start()
	
if __name__ == '__main__':	
	main()
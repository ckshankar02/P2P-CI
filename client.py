import socket
import sys
<<<<<<< HEAD
import threading
import time
import platform
import os

#Thread to interact with Server
class requestor(threading.Thread):
	def __init__(self, uport):
		threading.Thread.__init__(self)
		self.uploadPort = uport
		self.start()
		
	def run(self):
		#Opens a permanent connection with the server
		cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostbyname(socket.gethostname())		#Need to be changed when running clients and server on different Machines
		port = 7734
		cliSocket.connect((host,port))
		self.requestServer(cliSocket)	
	
	#Forms all the messages to be sent to the server.
	#Uses the method ADD, LOOKUP and LIST as criteria to generate message
	def formMessage(self, type, rfcNo):
		version = 'P2P-CI/1.0'
		sp = ' '
		end = '\n'
		host = 'Host:'+sp+socket.gethostbyname(socket.gethostname())
		port = 'Port:'+sp+str(self.uploadPort)	
		method = type
		sendMsg = ''
		if type == 'ADD':			
			RFC = 'RFC'+sp+str(input("RFC Number = "))
			title = 'Title:'+sp+str(input("RFC title = "))
			#sendMsg = method+sp+RFC+sp+'P2P-CI/2.0'+end+host+end+port+end+title+end+end	#Test for VERSION NOT SUPPORTED
			#sendMsg = 'REMOVE'+sp+RFC+sp+version+end+host+end+port+end+title+end+end		#Test for BAD REQUEST				
			#sendMsg = method+sp+RFC+sp+version+end+host+end+port+end+title+end+end			#PROPER REQUEST
		elif type == 'LOOKUP':			
			RFC = 'RFC'+sp+str(input("RFC Number = "))
			title = 'Title:'+sp+str(input("RFC title = "))
			sendMsg = method+sp+RFC+sp+version+end+host+end+port+end+title+end+end
		elif type == 'GET':
			RFC = 'RFC'+sp+rfcNo
			OS = 'OS:'+sp+platform.platform()
			sendMsg = method+sp+RFC+sp+version+end+host+end+OS+end+end
		else:
			sendMsg = method+sp+version+end+host+end+port+end+end		
		return sendMsg				
	
	#Options for Client interface
	def requestServer(self, cliSoc):	
		self.flag = 0	
		while self.flag == 0:
			print("\n1. Add RFC to Server \n2. Look Up an RFC \n3. Request Whole Index List \n4. Leave the Network")
=======
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
>>>>>>> c1c6112ceb79c4cea60c349bac65f6b43810d582
			option = str(input("Option = "))
			if option == '1':
				self.sendRFCAddRequest(cliSoc)
			elif option == '2':
				self.lookUpRequest(cliSoc)
			elif option == '3':
				self.wholeIndexRequest(cliSoc)
			elif option == '4':
<<<<<<< HEAD
				cliSoc.close()
				self.flag = 1
			else:
				print("Invalid Selection. Re-enter the Option!!!")
	
	#RFC Add Request
	def sendRFCAddRequest(self, cliSoc):
		sendMessage = self.formMessage('ADD',0)
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		data = cliSoc.recv(2048) 
		decodedData = data.decode('UTF-8')
		print('\n'+decodedData+'\n')
		
		
	def parseMsg(self, msg):
		splitMsg = msg.split("\n")
		return splitMsg
	
	
	
	#Lookup Request to the Server
	def lookUpRequest(self, cliSoc):
		#Sends a lookup request
		sendMessage = self.formMessage('LOOKUP',0)
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		data = cliSoc.recv(1024) 
		decodedData = data.decode('UTF-8')
		peerList = self.parseMsg(decodedData)
		print('\n'+peerList[0])
		
		#if the requested RFC is available in the P2P network then 
		#all the hosts containing the RFC are listed.
		if '200 OK' in peerList[0]:			
			for i in range(1,len(peerList)-1):
				peerDetails = peerList[i].split('<c>')
				print("%d. Host:%s\tPort:%s"%(i,peerDetails[2],peerDetails[3]))
			print(str(i+1)+". Quit Download Option")
			option = input("option = ")
			while int(option) > len(peerList)+1 or int(option) == 0:
					option = input("Enter Proper option = ") 
			if int(option) == i+1:
					return
			else:
				self.downloadRFC(peerList[int(option)])	    
				return
		
		
		
	def downloadRFC(self, pList):
		selectedHost = pList.split('<c>')
		#extracting the RFC Number, Host IP address, Host Port
		rfc = selectedHost[0]
		host = selectedHost[2]
		port = int(selectedHost[3])
		
		#opengin a socket to download from the selected peer
		downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		downloadSocket.connect((host,port))
		
		#Sending a GET Request to the Peer for the required RFC
		sendMessage = self.formMessage('GET', rfc)
		downloadSocket.send(bytes(sendMessage,'UTF-8'))	
		
		#Receiving the status message + DATA from the peer
		data = downloadSocket.recv(2048) 
		decodedData = data.decode('UTF-8')
		print('\n'+decodedData+'\n')
		
		#If the status is OK then a file is created and /
		#contents are downloaded and the download socket is closed.
		if '200 OK' in decodedData:
			filename = 'RFC'+rfc+'.txt'
			f = open(filename,'w')		
			data = ''
			while data != bytes('','UTF-8'):
				data = downloadSocket.recv(2048) 
				f.write(data.decode('UTF-8'))
			f.close()			
		downloadSocket.close()
	
	
	
	#Prints the Index received from the server.
	def printList(self,rfcList):
		masterList = rfcList.split('\n')
		print('\n'+masterList[0]+'\n')
		if '200 OK' in masterList[0]:
			for i in range(1,len(masterList)-1):
					r = masterList[i].split('<c>')
					print(str(i)+'.\t'+r[0]+'\t'+r[1]+'\t'+r[2]+'\t'+r[3]+'\n')
	
	
	
	#Sends LIST ALL Message to the server to receive the entire LIST
	def wholeIndexRequest(self, cliSoc):
		sendMessage = self.formMessage('LIST',None)
		cliSoc.send(bytes(sendMessage,'UTF-8'))	
		data = cliSoc.recv(1024) 
		decodedData = data.decode('UTF-8')
		self.printList(decodedData);
		
		
#Thread to provide the download service to other peers in the network.
class uploader(threading.Thread):
=======
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
>>>>>>> c1c6112ceb79c4cea60c349bac65f6b43810d582
	def __init__(self, newTuple):
		threading.Thread.__init__(self)
		self.client = newTuple[0]
		self.address = newTuple[1]

<<<<<<< HEAD
		
		
	def parseMsg(self, decodedMsg):
		m1 = decodedMsg.split("\n")
		m2 = []
		for l in m1:
			m2.append(str(l).split(" "))		
		return m2

		
		
	#Response to other Clients requesting download
	def buildResponse(self, stat, fileName):
		sp = ' ' 
		end = '\n'
		OS = 'OS:'+sp+platform.platform()+end
		currTime = 'Date:'+sp+time.asctime()+end
		if stat != '200 OK':
			lstModTme = 'Last-Modified:'+end
			contentLen = 'Content-Length:'+end
		else:
			seconds = os.path.getmtime(fileName)
			lstModTme = 'Last-Modified:'+sp+time.strftime('%Y-%m-%d %H:%M', time.localtime(seconds))+end
			contentLen = 'Content-Length:'+str(os.path.getsize(fileName))+end
			
		contentType = 'Content-Type: text/plain'+end
		resMsg = 'P2P-CI/1.0'+sp+stat+end+currTime+OS+lstModTme+contentLen+contentType
		return resMsg
		
		
		
	#Response to other Clients requesting download
	def respondToRequest(self,message):	
		method = message[0][0]
		version = message[0][3]
		file = 'RFC'+message[0][2]+'.txt'				
		status = ''
		if method != 'GET':								#Only GET Request is supported
			status = '400 Bad Request'			
		elif version != 'P2P-CI/1.0':					#Only P2P-CI/1.0 is supported
			status = '505 P2P-CI Version Not Supported' 
		elif not os.path.exists(file):					#The file is checked in the current working directory	
			status = '404 Not Found'
		else:
			status = '200 OK'
			
		responseMsg = self.buildResponse(status, file)	#Response to the other peer requesting a file download
		self.client.send(bytes(responseMsg,'UTF-8'))
		if status == '200 OK':
			f = open(file,'r')
			for line in f:
				self.client.send(bytes(line,'UTF-8'))
			f.close()
		self.client.close()		
			
			
			
	def run(self):
		receivedMsg = self.client.recv(1024)
		decodedMsg = receivedMsg.decode('UTF-8')
		actualMsg = self.parseMsg(decodedMsg)
		self.respondToRequest(actualMsg)
		
		
		
#Class to handle uploading			
class uploadHandler(threading.Thread):		
	def __init__(self, uport):
		threading.Thread.__init__(self)
		self.uploaderSoc = None
		self.port = uport
		self.start()	
	
	
	def run(self):
		self.uploaderSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		host = socket.gethostname()
		self.uploaderSoc.bind((host,self.port)) 
		self.uploaderSoc.listen(5)
		while True:
			try:
				u =  uploader(self.uploaderSoc.accept())
				u.start()
			except OSError:
				print('Client closed its connection')
				break
				
				
def main():		
	uploaderPort = int(input("Upload Port Number = ") ) #Port to Upload
	reqClient = requestor(uploaderPort) 				#Thread to communicate with the server
	uploadToClient = uploadHandler(uploaderPort) 		#Thread handling upload process
	while reqClient.isAlive():
		pass
	uploadToClient.uploaderSoc.close() 					#Closing the client 

=======
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
>>>>>>> c1c6112ceb79c4cea60c349bac65f6b43810d582
	
if __name__ == '__main__':	
	main()
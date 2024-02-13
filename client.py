from socket import *
import random
# set server's name and port
serverName = 'localhost'
serverPort = 1501
livesRemaining = 99
print("***************************")
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# receive input from user
sentence = "start"

# send sentence to server
clientSocket.send(sentence.encode())
receivedSentence = clientSocket.recv(1024) 
rcvList = receivedSentence.decode().split(",")
#print(rcvList)
print ('Show host:', rcvList[1])
print (rcvList[2])
clientSocket.close()

while(livesRemaining):
    # create object socket ipv4, tcp
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    
    # receive input from user
    sentence = input('Your guess is: ')
    # send sentence to server
    clientSocket.send(sentence.encode())

    # read data received from server
    receivedSentence = clientSocket.recv(1024) 
    rcvList = receivedSentence.decode().split(",")

    statusCode = int(rcvList[0])
    message = rcvList[1]
    wordStatus = rcvList[2]

    if(statusCode < 10):
        livesRemaining = statusCode
        print("lives remaining:", livesRemaining)
    elif(statusCode == 100):
        
        print(message)
    elif(statusCode == 200 or statusCode == 300):
        print(message)
        clientSocket.close()
        break
            
    
    # print the received data
    print ('Show host:', message)
    
    print (wordStatus)
    clientSocket.close()

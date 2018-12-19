
# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;



'''
RS-Server will be run before client to create socket and host 
name and will wait until it get client request after getting connected,
server will forward challange string to TLDS after connecting to them.
TLDS servers will return digest to AUTH and then AUTH will compare the digest and 
will send TLDS info to client to connect to based on digest match.
IF not match then it will forward Authentication failed message.


TO RUN AUTH server Type: python3 AUTH.py

'''

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc

# creating RS-Server Socket
def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    try:
        ssTSCOM=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TS1]: TLDS2(COM) socket2 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    try:
        ssTSEDU=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TS2]: TLDS1(EDU) socket2 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))





    server_binding=('',5000)
    portTSEDU=6001
    portTSCOM=6002
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)



    # send a intro  message to the client.

    msg="Connected TO RS Server ::"
    
    csockid.send(msg.encode('utf-8'))



    TSEDUCount=0
    TSEDU_host= "Java.cs.rutgers.edu"
    TSCOMCount=0
    TSCOM_host= "cpp.cs.rutgers.edu"

    # accepting data and comparing digest and sending data to client accordingly.
    while (True):
        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        if(data_from_client==""):
            break
        data_from_client=data_from_client.strip("\n")
        datasplit=data_from_client.split()

        str1=datasplit[0]
        digest=datasplit[1]
        

        # connecting to TLDS servers
        if str1 != "":
            
            if TSCOMCount == 0:
                sa_sameas_myaddr2=mysoc.gethostbyname(TSCOM_host)    
                server_binding2=(sa_sameas_myaddr2,portTSCOM)
                ssTSCOM.connect(server_binding2)
                TSCOMCount=TSCOMCount+1

            if TSEDUCount == 0:
                sa_sameas_myaddr3=mysoc.gethostbyname(TSEDU_host)
                server_binding3=(sa_sameas_myaddr3,portTSEDU)
                ssTSEDU.connect(server_binding3)
                TSEDUCount=TSEDUCount+1


            msg=str1

            ssTSCOM.send(msg.encode('utf-8'))    
            data_from_server=ssTSCOM.recv(100)
            data_from_server=data_from_server.decode('utf-8')

                
            msg=str1

            ssTSEDU.send(msg.encode('utf-8'))   
            data_from_server1=ssTSEDU.recv(100)
            data_from_server1=data_from_server1.decode('utf-8')


            if(data_from_server == digest):
                cmsg=data_from_server
                
                ssTSCOM.send('open'.encode('utf-8'))
                ssTSEDU.send('skip'.encode('utf-8'))
                cmsg=TSCOM_host + " "+"TLDS1"
                csockid.send(cmsg.encode('utf-8'))
                
            elif(data_from_server1 == digest):
                cmsg=data_from_server1
                
                ssTSCOM.send('skip'.encode('utf-8'))
                ssTSEDU.send('open'.encode('utf-8'))
                cmsg=TSEDU_host + " "+"TLDS2"
                csockid.send(cmsg.encode('utf-8'))
                
            
            else:

                cmsg="Authentication Failed"
                
                csockid.send(cmsg.encode('utf-8'))
            

   # Close the server socket

    ssTSCOM.close()
    ssTSEDU.close()
    ss.close()
    print("END OF PROGRAM")
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()


time.sleep(5)
exit()


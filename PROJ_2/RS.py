
# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;



'''
RS-Server will be run before client to create socket and host 
name and will wait until it get client request after getting connected,
server will look if it Has the DNS information that the client want,
IF not then it will forward it to TS server based on the request .com or .edu.
If Rs server has not found info in its database and cant forward request to TS servers,
then it will return Host not found error.
IF Rs server has forward that information to TSserver, Then it will foward infomation returned by TS servers.


RS server will take information of where TS server are running as well as the input for RSserver txt file.
for example: python3 ./RS.py $TSCOMHOSTNAME $TSEDUHOSTNAME  PROJ2-DNSRS.txt

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
        ssTSEDU=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: TLDS1(EDU) socket2 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    try:
        ssTSCOM=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: TLDS2(COM) socket2 created")
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


# creating Disctionary of DNS information from DNSRS.txt file.
# sys.argv[] will take argument from the Run Command. 

    RSDNS_tabel={}

    fileRS=open(sys.argv[3],"r")
    while (True):
        line = fileRS.readline()
        line = line.strip('\n')
        if(line==""):
            break
        word = line.split()
        RSDNS_tabel[word[0]] = dict(IP = word[1], Flag = word[2])
    


# send a intro  message to the client.

    msg="Connected TO RS Server ::"
    
    csockid.send(msg.encode('utf-8'))



    TSEDUCount=0
    TSCOMCount=0

    # accepting data and look into disctionary if it exists, if not send TS info. 
    while (True):
        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        if(data_from_client==""):
            break
        print(data_from_client)
        datasplit=data_from_client.split(".")

        datasplit=datasplit[-1]
        

        # checking disctioary for match in Rs server.
        if data_from_client in RSDNS_tabel:
            
            msg=RSDNS_tabel[data_from_client]
            msg1=msg["Flag"]+" "+msg["IP"]
            
            csockid.send(msg1.encode('utf-8'))
        # connecting to TSCOM server
        elif datasplit == "com":
            
            if TSCOMCount == 0:
                sa_sameas_myaddr2=mysoc.gethostbyname(sys.argv[1])
                print("SA SAme as My address"+
                sa_sameas_myaddr2)
                server_binding2=(sa_sameas_myaddr2,portTSCOM)
                ssTSCOM.connect(server_binding2)
                TSCOMCount=TSCOMCount+1


            msg=data_from_client
            ssTSCOM.send(msg.encode('utf-8'))
        
            data_from_server=ssTSCOM.recv(100)
            csockid.send(data_from_server)


        # connecting to TSEDU server
        elif datasplit == "edu":

            if TSEDUCount == 0:
                sa_sameas_myaddr3=mysoc.gethostbyname(sys.argv[2])
                server_binding3=(sa_sameas_myaddr3,portTSEDU)
                ssTSEDU.connect(server_binding3)
                TSEDUCount=TSEDUCount+1


            msg=data_from_client
            ssTSEDU.send(msg.encode('utf-8'))
        
            data_from_server=ssTSEDU.recv(100)
            
            csockid.send(data_from_server)


        else:

            seradd="HOSTNAME ERROR: HOST NOT FOUND IN RSserver"
              
            csockid.send(seradd.encode('utf-8'))

   # Close the server socket

    ssTSCOM.close()
    ssTSEDU.close()
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()


time.sleep(5)
exit()


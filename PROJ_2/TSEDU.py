
# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;




'''
TS-Server will be run before client to create socket and host 
name and will wait until it get RS Server request for info after getting connected client,
TLDS 2 EDU server will look for the information that RS server didn't find in its database. 
IF TLDS 2 EDU server has information it will return info with a flag A.
else return HOSTname Error.

TLDS 2 EDU Server will take input of txt file during the Run Command, 
For Example: python3 ./TSEDU.py PROJ2-DNSEDU.txt


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
        print("[S]: TLDS2 EDU Server  socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',6001)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a RSserver at", addr)


# creating Disctionary of DNS information from DNSTS.txt file. 
# sys.argv[1] will take argument from the Run Command.  

    TSDNS_tabel={}

    fileTS=open(sys.argv[1],"r")
    while (True):
        line = fileTS.readline()
        line = line.strip('\n')
        if(line==""):
            break
        word = line.split()
        TSDNS_tabel[word[0]] = dict(IP = word[1], Flag = word[2])


# accepting data and look into disctionary if it exists, if not send ERROR msg. 
    while (True):
        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        if(data_from_client==""):
            break
        print(data_from_client)

        # checking disctioary for match.
        if data_from_client in TSDNS_tabel:

        	
            msg=TSDNS_tabel[data_from_client]
            msg1=msg["Flag"]+" "+msg["IP"]
            csockid.send(msg1.encode('utf-8'))

        else:
            seradd="HOSTNAME ERROR: HOST NOT FOUND IN TSEDU Server" 
            csockid.send(seradd.encode('utf-8'))
 



    
   # Close the server socket
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()


time.sleep(5)
exit()


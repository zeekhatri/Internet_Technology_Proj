
# Name :-  Zeel Khatri ; Kishan Zalora




'''
TS-Server will be run before client to create socket and host 
name and will wait until it get client request after getting connected,
server will look for the information that RS server didn't had and ask client
to connect TS-Serrver. IF Ts server has information it will return info with a flag A.
else return HOSTname Error.

'''

import numpy as mypy
import threading
import time
import random

import socket as mysoc

# creating RS-Server Socket
def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',6000)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)


# creating Disctionary of DNS information from DNSTS.txt file.    

    TSDNS_tabel={}

    fileTS=open("PROJI-DNSTS.txt","r")
    while (True):
        line = fileTS.readline()
        line = line.strip('\n')
        if(line==""):
            break;
        word = line.split()
        TSDNS_tabel[word[0]] = dict(IP = word[1], Flag = word[2])


# accepting data and look into disctionary if it exists, if not send ERROR msg. 
    while (True):
        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        if(data_from_client==""):
            break;
        print(data_from_client)

        # checking disctioary for match.
        if data_from_client in TSDNS_tabel:
            msg=TSDNS_tabel[data_from_client]
            msg1=msg["Flag"]+" "+msg["IP"]
            csockid.send(msg1.encode('utf-8'))

        else:
            seradd="HOSTNAME ERROR: HOST NOT FOUND"
              
            csockid.send(seradd.encode('utf-8'))
 



    
   # Close the server socket
    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()


time.sleep(5)
exit()


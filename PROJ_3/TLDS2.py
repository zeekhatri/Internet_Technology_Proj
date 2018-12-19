
# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;




'''
TS-Server will be run before client to create socket and host 
name and will wait until it get AUTH Server request for info after getting connected to AUTH,
TLDS2 will first generate Digest based on the challange and the key and return that to AUTH Server.
Then BAsed on the MAtch TLDS will recive a client request and 
TLDS2 server will look for the information and 
IF TLDS2 server has information it will return info with a flag A.
else return HOSTname Error.

TO RUN TLDS2 Server Type: python3 TLDS2.py 

'''




import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc
import hmac

# creating RS-Server Socket
def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: TLDS2 EDU Server  socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    try:
        cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]:  Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))


    server_binding=('',6001)
    port_cs=6005

    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a RSserver at", addr)

    
    client_binding=('',port_cs)
    cs.bind(client_binding)
    cs.listen(1)


    # creating Disctionary of DNS information from PROJ3-TLDS2.txt file. 
    # getting key from key file
 

    TSDNS_tabel={}
    count=0
    countc=0
    keyFile=open('PROJ3-KEY2.txt',"r")
    while (True):
        line=keyFile.readline()
        line=line.strip('\n')
        if (line==""):
            break
        key=line

    keyFile.close()

    fileTS=open('PROJ3-TLDS2.txt',"r")
    while (True):
        line = fileTS.readline()
        line = line.strip('\n')
        if(line==""):
            break
        word = line.split()
        TSDNS_tabel[word[0]] = dict(IP = word[1], Flag = word[2])


    # accepting data from auth genereting digest and return.
    # then after client requets look into disctionary if it exists, if not send ERROR msg. 

    while (True):
        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        data_from_client=data_from_client.strip('\n')

        if(data_from_client==""):
            break

        d1=hmac.new(key.encode(),data_from_client.encode("utf-8"))     

        digest=d1.hexdigest()
        csockid.send(digest.encode('utf-8'))

        data_from_client=csockid.recv(100)
        data_from_client=data_from_client.decode('utf-8')
        data_from_client=data_from_client.strip('\n')


        if (data_from_client=='open'):

            csockidc,addr=cs.accept()   
            
            count=count+1
            countc=countc+1 
            print('Got connection: '+ str(countc))
            data_from_client=csockidc.recv(100)
            data_from_client=data_from_client.decode("utf-8")
            if(data_from_client==""):
                break
            data_from_client=data_from_client.strip("\n")

            

            # checking disctioary for match.
            if data_from_client in TSDNS_tabel:
                
                msg=TSDNS_tabel[data_from_client]
                msg1=msg["Flag"]+" "+msg["IP"]
                csockidc.send(msg1.encode('utf-8'))

            else:
                seradd="HOSTNAME ERROR: HOST NOT FOUND IN TLDS2. "
                
                csockidc.send(seradd.encode('utf-8'))

            
   # Close the server socket
    ss.close()
    cs.close()
    print("END OF PROGRAM")
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()


time.sleep(5)

exit()


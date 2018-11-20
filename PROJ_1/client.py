
# Name :-  Zeel Khatri ; Kishan Zalora


'''
 This is client, it will read HNS.txt and will store every DNS in the a List.
 -> Then it will send DNS one by one to RS(Root server). 
 -> if root server has the IP address then it will send it with a Flag A.
 -> if RS dont have it then it will send a Flag NS with a TS(TOP Server) HOST machine name.
 -> then it will connect to TS server and Check if the DNS information exist in TS.
 -> IF TS server DONt have teh infomation then it will send HOSTNAME Error.

'''

import numpy as mypy
import threading
import time
import random

import socket as mysoc

def client():
    # Creating Socket for RS.
    try:
        csRS=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket1 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    # Creating Socket for TS.    
    try:
        csTS=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket2 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
  
# Define the port on which you want to connect to the server 
# Defineing TS and RS Server PORTS.

    portRS = 5000
    portTS = 6000                
    sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
    
# connect to the server on local machine

    server_binding=(sa_sameas_myaddr,portRS)
    csRS.connect(server_binding) 
    data_from_server=csRS.recv(200)

#receive data from the server 
  
    print("[C]: Data received from server::",data_from_server.decode('utf-8'))

# Ceating file for Output

    out=open("RESOLVED.txt","w")
    out.write("*** HOSTNAME   ::    IP    ::   FLAG\n\n\n")



# Read from a file and create a List of DNS
    DNS_tabel =[]

    fileC=open("PROJI-HNS.txt","r")
    while(True):
        line = fileC.readline()
        line = line.strip('\n')
        DNS_tabel.append(line)
        if(line==""):
            break;

    fileC.close()

    

# Sending DNS to RS server and then TS server
    count=0
    for i in DNS_tabel:
        if(i==""):
            csRS.send("".encode('utf-8'))
            break;
        msg=i
        csRS.send(msg.encode('utf-8'))
        
        data_from_server=csRS.recv(200)
        data_from_server=data_from_server.decode('utf-8')
        data_from_server=data_from_server.strip('\n')
        word=data_from_server.split()
        flag=word[0]
        IP=word[1]

        # checking flag recieved from RS server and output if flag is A.   
        if(flag =="A"):
            
            out.write(msg + "    " + IP + "    " + flag + "\n")
            
        # connect and then Send DNS to TS server if flag is 
        elif(flag =="NS"):
            
            # connecting to TS server once   
            if count == 0:
                sa_sameas_myaddr2=mysoc.gethostbyname(IP)
                server_binding2=(sa_sameas_myaddr2,portTS)
                csTS.connect(server_binding2)
                count=count+1

            # sending DNS to TS server
            msg=i
            csTS.send(msg.encode('utf-8'))
        
            data_from_server=csTS.recv(200)
            data_from_server=data_from_server.decode('utf-8')
            data_from_server=data_from_server.strip('\n')
            word=data_from_server.split()
            flag=word[0]
            IP=word[1]


            # check if the flag is A then Output to file else output with error 

            if(flag =="A"):
        
                out.write(msg + "      " + IP + "      " + flag+"\n")

            else:

                out.write(msg + "    " + data_from_server+"\n")

            
            
        # Incase if flag is invalid    
        else:


            out.write(msg + "    " + IP + "   FLAG INVALID  ")




    # close the cclient socket

    out.close()
    csTS.close()
    csRS.close() 
    exit()   


t2 = threading.Thread(name='client', target=client)
t2.start()
time.sleep(5)

exit()



# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;


'''
 This is client, it will read HNS.txt and will store every DNS in the a List.
 -> Then it will send DNS one by one to RS(Root server). 
 -> if root server has the IP address then it will send it with a Flag A.
 -> if RS dont have it then Rs Server will send it to a TS(TOP Server).
 -> then RS server will retuen the infomation that it found.
 -> IF TS servers and RSserver Don't have infomation then it will send HOSTNAME Error.

 client will take argument of input file txt and where RS server is host in the Run command.
 For example: python ./CLIENT.py $RSHOSNAME PROJ2-HNS.txt

'''

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc

def client():
    # Creating Socket for RS.
    try:
        csRS=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket1 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
     
  
# Define the port on which you want to connect to the server 
# Defineing RS Server PORTS.

    portRS = 5000
                    
    sa_sameas_myaddr =mysoc.gethostbyname(sys.argv[1])
    
# connect to the server on local machine

    server_binding=(sa_sameas_myaddr,portRS)
    csRS.connect(server_binding) 
    data_from_server=csRS.recv(100)

#receive data from the server 
  
    print("[C]: Data received from RS server::",data_from_server.decode('utf-8'))

# Creating file for Output

    out=open("RESOLVED.txt","w")
    out.write("*** HOSTNAME   ::    IP    ::   FLAG\n\n\n")



# Read from a file and create a List of DNS
# sys.argv[] will take argument from the Run Command. 

    DNS_tabel =[]

    fileC=open(sys.argv[2],"r")
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
            break
        msg=i
        print(i)
        csRS.send(msg.encode('utf-8'))
        
        data_from_server=csRS.recv(200)
        data_from_server=data_from_server.decode('utf-8')

        data_from_server1=data_from_server.strip('\n')
        word=data_from_server1.split()
        flag=word[0]
        IP=word[1]

        # checking flag recieved from RS server and output if flag is A.   
        if(flag =="A"):
            
            out.write(msg + "    " + IP + "    " + flag + "\n")


            
        # Incase if flag is invalid or None   
        else:


            out.write(msg + "    " + data_from_server+  "   FLAG INVALID  " +"\n")




    # close the cclient socket

    out.close()
    #csTS.close()
    csRS.close() 
    exit()   


t2 = threading.Thread(name='client', target=client)
t2.start()
time.sleep(5)

exit()


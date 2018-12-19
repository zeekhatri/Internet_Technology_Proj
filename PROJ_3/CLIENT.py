
# Name1 :-  Zeel Khatri ; 
# Name2 :-  Kishan Zalora;


'''
 This is client, it will read each line from HNS.txt and will store Key, challange and DNS in the a List.
 -> Then it will send key and challange to AUTH. 
 -> Then Auth will return a Machine address of TLDS1 or TLDS2 Based on the key match to TLDS servers.
 -> Client will then connect to TLDS to get DNS Info.

 TO Run Client type: python3 ./CLIENT.py

'''

import numpy as mypy
import threading
import time
import random
import sys
import socket as mysoc
import hmac

def client():
    # Creating Socket for RS.
    try:
        csRS=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket1 created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    

         
  
# Define the port on which you want to connect to the server 
# Defineing AUTH Server PORTS.

    portRS = 5000
    portTSCOM=6005
    host=mysoc.gethostname()
                    
    sa_sameas_myaddr =mysoc.gethostbyname(host)
    
# connect to the server on local machine

    server_binding=(sa_sameas_myaddr,portRS)
    csRS.connect(server_binding) 
    data_from_server=csRS.recv(100)

#receive data from the server 
  
    print("[C]: Data received from RS server::",data_from_server.decode('utf-8'))

# Creating file for Output

    out=open("RESOLVED.txt","w")
    out.write("*** SERVER   ::   HOSTNAME   ::    IP    ::   FLAG ***\n\n\n")



# Read from a file and create a List of DNS and also adding digest after generating

    DNS_tabel =[]

    fileC=open('PROJ3-HNS.txt',"r")
    while(True):
        line = fileC.readline()      
        line = line.strip('\n')

        if(line==""):
            break
        
        line = line.split()
        DNS_tabel.append(line)

    fileC.close()

    # making digest AND adding to DNS Tabel

    for i in DNS_tabel:
        key=i[0]
        str=i[1]
        d1= hmac.new(key.encode(),str.encode("utf-8"))
        i.append(d1.hexdigest())
        
   

# Sending DNS to RS server and then connecting to TLDS server, PRINTING TO OUTPUT AS WELL
    for i in DNS_tabel:
        if(i==""):
            csRS.send("".encode('utf-8'))
            break
        msg=i[1] + " " + i[3]
        
        csRS.send(msg.encode('utf-8'))
        
        data_from_server=csRS.recv(200)
        data_from_server=data_from_server.decode('utf-8')
        data_split=data_from_server.split()
        data_from_server=data_split[0]


        try:
            ssTSCOM=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
            print("[S]: TLDS socket created")
        except mysoc.error as err:
            print('{} \n'.format("socket open error ",err))


        sa_sameas_myaddr2=mysoc.gethostbyname(data_from_server)    
        server_binding2=(sa_sameas_myaddr2,portTSCOM)
        ssTSCOM.connect(server_binding2)

        msg = i[2] 
        ssTSCOM.send(msg.encode('utf-8'))
        data_from_server=ssTSCOM.recv(100)
        data_from_server=data_from_server.decode('utf-8')

        data_from_server1=data_from_server.strip('\n')
        data_from_server1=data_from_server
        word=data_from_server1.split()
        flag=word[0]
        IP=word[1]

        # checking flag recieved from RS server and output if flag is A.   
        if(flag =="A"):
            
            out.write(data_split[1] +"   "+msg + "    " + IP + "    " + flag + "\n")
            
        # ignore but print NS string
        elif(flag =="NS"):
            
            out.write(data_split[1] +"   "+msg + "    " + IP + "    " + flag + " :- IGNORED TEST CASE\n")
    
        # Incase IP ADDRESS not found    
        else:

            out.write(data_split[1] +"   "+msg + "    " + data_from_server+  "\n")

        ssTSCOM.close()
        


           

    # close the cclient socket 

    out.close()
    csRS.close() 
    print("END OF PROGRAM")
    exit()   


t2 = threading.Thread(name='client', target=client)
t2.start()
time.sleep(5)

exit()


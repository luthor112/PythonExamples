#!/usr/bin/env python2

import socket
import ssl
import thread

ALLOWED_CLIENTS = ["TLS_Server_2"]

def get_common_name(cert):
    common_name = None
    
    for data_tuple in cert["subject"]:
        if data_tuple[0][0] == "commonName":
            common_name = data_tuple[0][1]
            break
    
    return common_name

def deal_with_it(clientsocket, from_address):
    try:
        print "Receiving from", from_address
        print "Client\'s CN:", get_common_name(clientsocket.getpeercert())
        
        if get_common_name(clientsocket.getpeercert()) in ALLOWED_CLIENTS:
            data = clientsocket.recv(1)
            
            while not data == "q":
                data_length = ""
                while not data == " ":
                    data_length += data
                    data = clientsocket.recv(1)
                
                data_length = int(data_length)
                
                message = ""
                
                while data_length:
                    to_read = 1024 if data_length > 1024 else data_length
                    data = clientsocket.recv(to_read)
                    message += data
                    data_length -= len(data)
                
                print message
                
                data = clientsocket.recv(1)
        else:
            print "BAD IDENTITY"
    finally:
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
    
    print "End of communication."

if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Because of testing
    serversocket.bind(("", 31337))
    serversocket.listen(5)
    
    serversocket = ssl.wrap_socket(serversocket, keyfile="tls_server.key", certfile="tls_server.pem", server_side=True, cert_reqs=ssl.CERT_REQUIRED, ca_certs="ca.cert.pem", suppress_ragged_eofs=False)
    
    print "Server online!"
    
    try:
        while True:
            (clientsocket, from_address) = serversocket.accept()
            thread.start_new_thread(deal_with_it, (clientsocket, from_address))
    except KeyboardInterrupt:
        pass
    
    print "Server offline."

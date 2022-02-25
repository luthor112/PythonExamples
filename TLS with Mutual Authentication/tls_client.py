#!/usr/bin/env python2

import socket
import ssl

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 31337
SERVER_COMMON_NAME = "TLS_Server"

def get_common_name(cert):
    common_name = None
    
    for data_tuple in cert["subject"]:
        if data_tuple[0][0] == "commonName":
            common_name = data_tuple[0][1]
            break
    
    return common_name

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s = ssl.wrap_socket(s, keyfile="tls_server2.key", certfile="tls_server2.pem", cert_reqs=ssl.CERT_REQUIRED, ca_certs="ca.cert.pem", suppress_ragged_eofs=False)
    
    s.connect((SERVER_HOST, SERVER_PORT))
    print "Server\'s CN:", get_common_name(s.getpeercert())
    
    if get_common_name(s.getpeercert()) == SERVER_COMMON_NAME:
        used_cipher = s.cipher()
        print "Cipher used:", used_cipher[0]
        print "From SLL version:", used_cipher[1]
        print "Secret bits:", used_cipher[2]
        
        data = raw_input("-> ")
        try:
            while not data == "":
                s.sendall(str(len(data))+" "+data)
                data = raw_input("-> ")
            else:
                s.sendall("q")
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
    else:
        print "BAD IDENTITY"
        s.shutdown(socket.SHUT_RDWR)
        s.close()

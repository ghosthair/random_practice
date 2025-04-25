import socket
import threading
import sys
import datetime
import time, os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from helper import to_bytes, from_bytes, gen_server_rsa_keypair
import binascii


print_lock = threading.Lock()  # mutex lock for display access


def print_msg(msg):
    '''
    Print a message with current timestamp
    msg: the message string
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")
            

def handle_client(client_socket, client_ip, client_port):
    '''
    Handles connection from a client
    client_socket: socket to use to read/write to client
    client_ip:     IP address of client
    client_port:   port number of client connection
    '''
    
    print_msg("Connection from " + client_ip + ":" + client_port)
    
    # TODO: Implement server side of authentication protocol and store established 
    #       session key in the session_key variable as a byte string


    # Grabbing needed keys
    with open("./Client_Auth_hmk/client_pubkey", "rb") as f:
        pem_pub = f.read()
    public_key = serialization.load_pem_public_key(pem_pub)

    with open("./Client_Auth_hmk/server_prikey", "rb") as e:
        pem_pri = e.read()
    ser_private_key = serialization.load_pem_private_key(pem_pri, password=None)
 
    # This is the total message received, not pared out. Will need to parse
        #out the signed version and actual message.
    session_key = client_socket.recv(1024)

    #Parsing out the message and the signed version
    signed_key = session_key[256:]
    session_info = session_key[:256]

    #will raise an error if not signed properly.
    public_key.verify(
        signed_key,
        session_info,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    #Starting the decryption process.
    plaintext = ser_private_key.decrypt(
        session_info, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(),
        label=None
        )
    )

    # Parsing out the session key to get the actual key.
    # session_dec_key = from_bytes(plaintext[:26])
    dec_sequence = from_bytes(plaintext[26:28])
    dec_time = from_bytes(plaintext[28:32])

    # add the actual impacts if time is oleder than 10 seconds
    current_time = time.time()
    if dec_time - current_time <= 10:
        print("Time check is good.")
    else:
        session_key = None
        print("Time came back out of bounds.")

    #Adding one to the sequence number, for addiditonal checks
    return_sequence = dec_sequence + 1
    current_time_msg = int(current_time)

    #Consildation of the parts for the session message, session key + sequence number + time
    return_key = plaintext[:26] + to_bytes(return_sequence) + to_bytes(current_time_msg, 4)

    #Encryption of the consolidated message.
    return_ciphertext = public_key.encrypt(
        return_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    #The actual socket to send.
    client_socket.send(return_ciphertext)

    # TODO: End of the todo block
    # --------------------------------------------------------------#
    #
    
    
    # Print session key
    if session_key is None:
        print_msg ("No session key established!")
    else:
        print_msg ("Established session key: " + str(binascii.hexlify(session_key)))
    
   
    # Close the connection (must always be done)
    if client_socket:
        client_socket.close()
    print_msg("Connection closed to " + client_ip + ":" + client_port)
        
        
        
if __name__ == '__main__':

    host = '127.0.0.1'   # ip to use to accept connections
    port = 5000          # port number to use to accept connections


    # Create a server socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  

    # Allow only five clients at a time 
    server_socket.listen(5)

    print_msg("Listening for connection on " + host + ":" + str(port))


    while True:
        try:
            client_socket, address = server_socket.accept()  # accept new connection
            client_ip = address[0]
            client_port = str(address[1])

            # Start a thread to handle client connection
            threading.Thread(target=handle_client, args=(client_socket, client_ip, client_port), daemon=True).start()
            
        except KeyboardInterrupt:  # CTRL+C
            print("")
            print_msg("Server stopped")

            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(0)
        except Exception as e:
            print_msg("Exception: " + str(e))
            
            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(1)


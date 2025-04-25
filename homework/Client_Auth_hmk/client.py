import socket
import threading
import sys
import datetime
import time, os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from helper import to_bytes, from_bytes, gen_client_rsa_keypair
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
        
if __name__ == '__main__':
    host = '127.0.0.1'  # server ip
    port = 5000         # server port

    # Create a regular client socket
    client_socket = socket.socket()      

    # Establish connection with server
    print_msg("Establishing connection to " + host + ":" + str(port))
    try:
        client_socket.connect((host, port))  # connect to the server
    except Exception as e:
        print_msg("Error during connection: " + str(e))
        sys.exit(1)

    # TODO: Implement client side of authentication protocol and store established 
    #       session key in the session_key variable as a byte string
    
    session_key = os.urandom(26)
    sequence = 10000
    seq_bytes = to_bytes(sequence, 2)
    time_stmp = int(time.time())
    time_bytes = time_stmp.to_bytes(4, 'big')
    session_msg = session_key + seq_bytes + time_bytes

    #Grabbing Keys
    with open("./Client_Auth_hmk/server_pubkey", "rb") as f:
        pem_pub = f.read()
    public_key = serialization.load_pem_public_key(pem_pub)

    with open("./Client_Auth_hmk/client_prikey", "rb") as e:
        client_private_key = serialization.load_pem_private_key(
            e.read(),
            password=None
        )

    #Encrypting message
    ciphertext = public_key.encrypt(
        session_msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    #Signing message
    signed_session = client_private_key.sign(
        ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    #Creating the message of the signed version and the message
    full_msg = ciphertext + signed_session
    #Sending the consolidated message.
    client_socket.sendall(full_msg)

    message_from_server = client_socket.recv(1024)
    ses_from_server = client_private_key.decrypt(
        message_from_server, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(),
        label=None
        )
    )

    # print(f"Message received from the server: {len(ses_from_server)}")
    return_sequence = from_bytes(ses_from_server[26:28])
    return_time = from_bytes(ses_from_server[28:])
    print(f"The returned sequence number is: {return_sequence}\nThe returned time stamp is:{return_time}")


    # TODO: End of the todo block
    # --------------------------------------------------------------#
    #

    # Print session key
    if session_key is None:
        print_msg ("No session key established!")
    else:
        print_msg ("Established session key: " + str(binascii.hexlify(full_msg)))

    # Close the connection
    if client_socket:
        client_socket.close()
    print_msg("Client stopped")
    sys.exit(0)
    
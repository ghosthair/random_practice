import socket
import threading
import sys
import datetime
import time, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

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
    session = os.urandom(32)
    time_stmp = str(time.time()).encode()
    padded_timestamp = time_stmp.ljust(32, b'\x00')
    session_key = session + padded_timestamp
    iv = os.urandom(16)
    aes_key = os.urandom(32)
    
    '''
    Notes from the crypto homework, no need to reinvent the wheel
        sym_key was given directly to the function in the crypto file
        param sym_key: the symmetric secret key (byte string)
            I believe this maybe one of the areas where we combine multiple encryption types,
            like the envelope method but with CBC mode. So generate data with sym_key, then
            encrypt with RSA key then send data.

        param iv: initial value used during encryption (byte string)

        Data will probably be session key, this is the infor that really important
    '''
    #Encrypting using AESCBS Mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC)
    encryptor = cipher.encryptor()

    #Padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(session_key) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    #Encrypt AES KEY
    public_key = None # Retrieve key from file
    enc_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    env_message = enc_key + iv + cipher_text
    # TODO: End of the todo block
    # --------------------------------------------------------------#
    #
    # Print session key
    if session_key is None:
        print_msg ("No session key established!")
    else:
        print_msg ("Established session key: " + str(binascii.hexlify(session_key)))

    # Close the connection
    if client_socket:
        client_socket.close()
    print_msg("Client stopped")
    sys.exit(0)
    
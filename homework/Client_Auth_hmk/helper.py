import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def gen_client_rsa_keypair():
    '''
    Generate a RSA public and private keypair

    Save the keypair as pem
    
    '''
    private_key = rsa.generate_private_key(65537, 2048)
    public_key = private_key.public_key()
    key = (public_key, private_key)
    pem_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem_pub.splitlines()[0]
    with open("./Client_Auth_hmk/client_pubkey", "wb") as f:
        f.write(pem_pub)
    pem_pri = private_key.private_bytes(
            encoding=serialization.Encoding.PEM, 
            format=serialization.PrivateFormat.TraditionalOpenSSL, 
            encryption_algorithm=serialization.NoEncryption())
    pem_pri.splitlines()[0]
    with open("./Client_Auth_hmk/client_prikey", "wb") as f:
        f.write(pem_pri)
        
    return key


def gen_server_rsa_keypair():
    '''
    Generate a RSA public and private keypair

    Save the keypair as pem
    
    '''
    private_key = rsa.generate_private_key(65537, 2048)
    public_key = private_key.public_key()
    key = (public_key, private_key)
    pem_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem_pub.splitlines()[0]
    with open("./Client_Auth_hmk/server_pubkey", "wb") as f:
        f.write(pem_pub)
    pem_pri = private_key.private_bytes(
            encoding=serialization.Encoding.PEM, 
            format=serialization.PrivateFormat.TraditionalOpenSSL, 
            encryption_algorithm=serialization.NoEncryption())
    pem_pri.splitlines()[0]
    with open("./Client_Auth_hmk/server_prikey", "wb") as f:
        f.write(pem_pri)

    return key

def to_bytes(x, y=2):
    bytes_x = x.to_bytes(y, byteorder='big')
    return bytes_x

def from_bytes(x, y=2):
    x_num = int.from_bytes(x, 'big')
    return x_num


if __name__ == "__main__":
    gen_client_rsa_keypair()
    gen_server_rsa_keypair()
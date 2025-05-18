from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import random
import hmac
import sys
import time

time_now = round(time.time(),5)

def print_with_ts(msg, hold=False, end="\n"):
    global time_now
    if not hold:
        time_now = round(time.time(),5)
        
    print("{:.5f}\t{}".format(time_now,msg), end=end)
    sys.stdout.flush()
    


curve = ec.SECP256R1()

#### A and Attacker
print("------------------------------------")
print("A and attacker interaction")
print("------------------------------------\n")

A_private_key = ec.generate_private_key(curve)   # A's ECDHE private key
A_public_key = A_private_key.public_key()        # A's ECDHE public key

AttA_private_key = ec.generate_private_key(curve)  # Attacker's ECDHE private key with A
AttA_public_key = AttA_private_key.public_key()    # Attacker's ECDHE public key shared with A

# Attacker sends their public key to A first 
# Then A sends their public key to attacker
print_with_ts("A gets attacker's ECDHE public key: " + AttA_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint).hex())
print_with_ts("Attacker gets A's ECDHE public key: " + A_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint).hex())


# Both compute the shared key
A_shared_key = A_private_key.exchange(ec.ECDH(), AttA_public_key)
AttA_shared_key = AttA_private_key.exchange(ec.ECDH(), A_public_key)

print_with_ts("A's computed shared key: " + A_shared_key.hex())
print_with_ts("Attacker's computed shared key with A: " + AttA_shared_key.hex(), hold=True)

if A_shared_key != AttA_shared_key:
    print_with_ts("Something is wrong...A and attacker does not have same shared key")
    sys.exit(1)
else:
    print("\n\033[93mNOTE: Both A and attacker computed same shared key (expected)\033[0m\n")

    
# A computes hash of some predefined data and sends the first two bytes (16 bit)
# of the hash to T
# Attacker can also compute the hash since they also have the shared key
hash_fixed_A = hmac.new(A_shared_key, b"SOME PREDEFINED DATA",'sha256').digest()
print_with_ts("A computes hash on some predefined data using shared key in HMAC_SHA256: " + hash_fixed_A.hex())
verifier_A = hash_fixed_A[0:2]  # also computed independently by attacker
print_with_ts("A sends first two bytes of hash to T: " + verifier_A.hex())

print("\n")

#### Attacker and B
# Objective: if attacker can select their ECDHE public key in a way that the verifier
# computed by B is same as that of A, then the MITM will be successful
# Also, here attacker would have already received the ECDHE public key from B
print("------------------------------------")
print("B and attacker interaction")
print("------------------------------------\n")

B_private_key = ec.generate_private_key(curve)  # B's ECDHE private key
B_public_key = B_private_key.public_key()       # B's ECDHE public key
print_with_ts("Attacker gets B's ECDHE public key: " + B_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint).hex())

# Attacker creates precise ECDHE public key
print_with_ts("Attacker computation in progress...", end="")
start_time = time.time()
while True:
    AttB_private_key = ec.generate_private_key(curve)  # Attacker's ECDHE private key
    AttB_public_key = AttB_private_key.public_key()    # Attacker's ECDHE public key to be shared with B
    
    # Attacker checks what the two bytes of the verifier will be if the above ECDHE
    # public key is used; retry if that's not same as verifier_A
    AttB_shared_key = AttB_private_key.exchange(ec.ECDH(), B_public_key)
    hash_fixed = hmac.new(AttB_shared_key, b"SOME PREDEFINED DATA",'sha256').digest()
    verifier = hash_fixed[0:2]
    
    if verifier == verifier_A:
        break
end_time = time.time()      
print("%0.2f"%(end_time-start_time) + "s")       

print_with_ts("B gets's attacker's ECDHE public key: " + AttB_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint).hex())


# With the ECDHE public key chosen by attacker, both B and attacker compute shared key
B_shared_key = B_private_key.exchange(ec.ECDH(), AttB_public_key)    
AttB_shared_key = AttB_private_key.exchange(ec.ECDH(), B_public_key)

print_with_ts("B's computed shared key: " + B_shared_key.hex())
print_with_ts("Attacker's computed shared key with B: " + AttB_shared_key.hex(), hold=True)

if B_shared_key != AttB_shared_key:
    print_with_ts("Something is wrong...B and attacker does not have same shared key")
    sys.exit(1)
else:
    print("\n\033[93mNOTE: Both B and attacker computed same shared key (expected)\033[0m\n")

    
  
# B computes hash of some predefined data and sends the first two bytes (16 bit)
# of the hash to T
hash_fixed_B = hmac.new(B_shared_key, b"SOME PREDEFINED DATA",'sha256').digest()
print_with_ts("B computes hash on some predefined data using shared key in HMAC_SHA256: " + hash_fixed_B.hex())
verifier_B = hash_fixed_B[0:2]
print_with_ts("B sends first two bytes of hash to T: " + verifier_B.hex())


# T compares values from A and B
if verifier_A == verifier_B:
    print("\n\033[93mNOTE: hash values in A and B are different, but the first two bytes are the same!\033[0m\n")
    print_with_ts("T says values from A and B are equal...MITM successful")
else:
    print_with_ts("T says values from A and B are not equal...MITM failed")

    


# server.py

import random
import sys
from socket import socket, SOCK_DGRAM, AF_INET

def generate_initial_state():
    return 0b000000000000000000  # All squares are empty (00)

def encode_msg(game_id, serial_id, game_flags, game_state, msg):
    data = (game_id << 40) | (serial_id << 32) | (game_flags << 18) | game_state
    game_message = msg.encode('utf-8')
    fixed_data = data.to_bytes(8, 'big') + game_message
    return fixed_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python server.py <IP> <PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Create UDP socket
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    udp_sock.bind((server_ip, server_port))
    print(f"Server is running on {server_ip}:{server_port}")

    game_id = random.randint(0, (2**24 - 1))
    serial_id = 0x00
    game_flags = 0x0000
    game_state = generate_initial_state()
    welcome_msg = "Welcome to Tic Tac Toe!"
    initial_message = encode_msg(game_id, serial_id, game_flags, game_state, welcome_msg)

    while True:
        print("Waiting for a client to send data...")
        data, client_address = udp_sock.recvfrom(1024)
        print(f"Received data from {client_address}")

        if data:
            print("Sending initial game state to client...")
            udp_sock.sendto(initial_message, client_address)

if __name__ == "__main__":
    main()

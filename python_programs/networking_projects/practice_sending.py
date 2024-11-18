from socket import socket, SOCK_DGRAM, AF_INET
import sys
import messaging as msg

game_id = 1
serial_id = 1
flags = 0
game_state = 0
test_message = "Testing the bad game id"

x = sys.argv[1]
y = int(sys.argv[2])
z = msg.encode_message(game_id, serial_id, flags, game_state, test_message)

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def send_data(udp_sock, endpoint, data):
  try:
    ret = udp_sock.sendto(data, endpoint)
    print("Sent %d bytes" % (ret))
  except Exception as e:
    print_error(e, "sendto")

udp_sock = socket(AF_INET, SOCK_DGRAM)
send_data(udp_sock, (x, y), z)

from socket import socket, SOCK_DGRAM, AF_INET
import random

def encode_message(game_id, message_id, flags, game_state, message):
  game_id &= 0xFFFFFF
  message_id &= 0xFF
  flags &= 0x3FFF
  game_state &= 0x3FFFF

  data = (game_id << 40) | (message_id << 32) | (flags << 18) | game_state
  
  data_bytes = data.to_bytes(8, byteorder="big")

  message_bytes = message.encode("utf-8")

  return data_bytes + message_bytes

def decode_message(data):
  data_part = int.from_bytes(data[:8], byteorder="big")

  game_id = (data_part >> 40) & 0xFFFFFF
  message_id = (data_part >> 32) & 0xFF
  flags = (data_part >> 18) & 0x3FFF
  game_state = data_part & 0x3FFFF

  message = data[8:].decode("utf-8")

  return game_id, message_id, flags, game_state, message

def generate_id():
    '''
    Game ID:
    24 bit random number, used throughout the game
    generated from client
    '''
    # rand_num = random.randint(0, (2**24-1))
    return random.randint(0, 0xFFFFFF)

def get_name():
  x = input("Enter player name: ")
  return x


def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def send_data(udp_sock, endpoint, data):
  try:
    ret = udp_sock.sendto(data, endpoint)
    # print("Sent %d bytes" % (ret))
  except Exception as e:
    print_error(e, "sendto")


def recv_data(udp_sock):
  try:
    data, (ip, port) = udp_sock.recvfrom(1024)
    return data, (ip, port)
  except Exception as e:
    print_error(e, "recvfrom")
    return None, None
# def main():
#   print(len(sys.argv))
#   if len(sys.argv) >= 3:
#     ip = sys.argv[1]
#     try:
#       port = int(sys.argv[2])
#     except:
#       print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
#       sys.exit(1)

#   data = None
#   if len(sys.argv) == 4:
#     data = sys.argv[3]
#     print("Will send %s to %s:%d via udp" % (data, ip, port))
#   else:
#     print("Must enter data to send as argument to program")

#   try:
#     udp_sock = socket(AF_INET, SOCK_DGRAM)
#     send_data(udp_sock, (ip, port), data)
#   except Exception as e:
#     print_error(e, "socket")

# if __name__ == "__main__":
  # data = b'o\xde1\x00\x00\x00\x00\x00David'
  # print(decode_message(data))

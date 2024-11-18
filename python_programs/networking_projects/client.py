import json as js
import re
import sys
import os
from socket import socket, SOCK_STREAM, AF_INET
from select import select

def print_error(e, f="Unknown"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def get_rooms():
    '''
    Collecting rooms from user, will return list if more than one
    Return string if just one
    '''
    try:
        CHAT_ROOMS = []
        room_num=int(input("How many rooms would you like to message? "))
        while room_num > 0:
            x = '#' + input("Enter the room (limit 60 characters):")
            if len(x) > 60:
                print("Too many characters for room!")
            else:
                CHAT_ROOMS.append(x)
            room_num -= 1
        return CHAT_ROOMS if len(CHAT_ROOMS) > 1 else CHAT_ROOMS[0]
    except ValueError:
        print("Invalid room number")
        return []

def get_username():
    u_name = '@' + input("Enter user name (limit 60 characters): ")
    if len(u_name) > 60:
        print("Error, too many characters.")
        return None
    return u_name

def first_msg(user_name, rooms):
    chat_message = {"actions": "connect", "user_name": user_name, "targets": rooms}
    json_msg = js.dumps(chat_message)
    # print(json_msg)
    return json_msg

def get_msg(user_name, target):
    x = input("Enter your message (limit 3800 characters): ")
    if len(x) > 3800:
        print("Message too long!")
        return None
    y = {"action": "message", "user_name": user_name, "target": target, "message": x}
    # print(y)
    return y

def disconnect_chat():
    disconnect = {"actions": "disconnect"}
    # print(disconnect)
    return disconnect

def received_messages(text):
    if text:
        terminal_width = os.get_terminal_size().columns
        # Move cursor to the right position
        seperator_lines = '-' * terminal_width
        print(seperator_lines)
        print(f"\033[{terminal_width - len(text)}G{text}")
        print(seperator_lines)

def send_data(tcp_sock, data):
    try:
        ret = tcp_sock.send(bytes(data, 'utf-8'))
    except KeyboardInterrupt as k:
        raise KeyboardInterrupt()
    except Exception as e:
        print_error(e, "send")

def recv_data(tcp_sock):
    try:
        data = tcp_sock.recv(4096)
        if len(data) == 0:
            return False
        return data
    except Exception as e:
        print_error(e, "recv")

def connect_socket(ip, port):
    try:
        tcp_sock = socket(AF_INET, SOCK_STREAM)
        tcp_sock.connect((ip, port))
        tcp_sock.setblocking(0)
        return tcp_sock
    except Exception as e:
        print_error(e, "connect")
        return None

def check_error(response):
    """
    Checks for errors in the server response.
    Prints the error message if an error is found.

    Parameters:
        response (str): JSON string of the server response.

    Returns:
        bool: False if an error is detected, True otherwise.
    """
    try:
        response_data = js.loads(response)  # Parse JSON response

        # Check if the response has a status of "error"
        if response_data.get("status") == "error":
            error_message = response_data.get("message", "Unknown error")
            print(f"Error: {error_message}")
            return False
        return True
    except js.JSONDecodeError:
        print("Received invalid JSON from server.")
        return False


def main():
    '''
    First section takes in args to connect and set up socket
    '''
    if len(sys.argv) >=3:
        ip = sys.argv[1]
        try:
            port = int(sys.argv[2])
        except:
            print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
            sys.exit(1)
    tcp_sock = connect_socket(ip, port)
    if not tcp_sock:
        return
    tcp_sock.setblocking(0)

    '''
    Start of chat, takes user name of user and rooms they want to connect to.
    If the user messes these up it ends the program and never connected.
    '''
    u_name = get_username()
    if not u_name:
        print("In valid username. Exiting.")
        return
    rooms = get_rooms()
    if not rooms:
        print("No room specified. Exiting")
        return
    
    '''
    Starting the connection
    '''
    read_sockets = [tcp_sock, sys.stdin]
    data = None
    #Send the first connection message
    first_message = first_msg(u_name, rooms)
    send_data(tcp_sock, first_message)

    '''
    Starting the main part of the program
    '''
    try:
        while data != 'quit\n':
            readlist, writelist, _ = select(read_sockets, [], [], 1)
            if tcp_sock in readlist:
                server_response = recv_data(tcp_sock)
                err_check = check_error(server_response)
                if err_check == False:
                    continue
                if server_response == False:
                    print("Sever went away, shutting down.")
                    data = 'quit'
                else:
                    rec_msgs = server_response.decode('utf-8')
                    received_messages(rec_msgs)
            print("Would you like to message a user or room?")
            x = input().lower().strip()
            if x == "user":
                y = input("User: ")
                y = "@" + y
            elif x == "room":
                y = input("Room: ")
                y = "#" + y
            message_data = get_msg(u_name, y)
            if message_data:
                json_message = js.dumps(message_data)
                send_data(tcp_sock, json_message)
            else:
                print("No message sent.")
            answer = input("Type 'quit' to exit or press Enter to contine: ")
            if answer == 'quit':
                print("Exiting chat.")
                end_chat = disconnect_chat()
                send_data(tcp_sock, end_chat)
                sys.exit()
    except KeyboardInterrupt as e:
        data = 'quit'
        print("User killed chat")
    finally:
        tcp_sock.close()

if __name__ == "__main__":
    print("Welcome to David's chat machine!\n")
    try:
        main()
    except KeyboardInterrupt as e:
        print("Killed by user!")



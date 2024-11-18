## Imports ------------------------------------------------------
import threading
from socket import socket, SOCK_DGRAM, AF_INET
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor
import messaging as msg
## Imports ------------------------------------------------------

## Constants and timeout set ------------------------
GAMES_DIC = {}  
GAMES_LOCKS = {}
# Flags Bitmask (bit positions 0 to 4, reserved: 5-13)
X_MOVE_FLAG = 1 << 13 
O_MOVE_FLAG = 1 << 12
X_WIN_FLAG = 1 << 11  
O_WIN_FLAG = 1 << 10   
TIE_FLAG = 1 << 9     
ERROR_FLAG = 1 << 8    
# Inactivity timeout (seconds)
TIMEOUT = 5 * 60  # 5 minutes


def print_error(e, f="UNKNOWN"):
    print(f"Error in {f}!")
    print(e)
    print(type(e))


def recv_data(udp_sock):
    try:
        data, (ip, port) = udp_sock.recvfrom(1024)
        # print(f"Data received: {data}")
        return data, ip, port
    except Exception as e:
        print_error(e, "recvfrom")
        return None, None, None


def gs_decode(x):
    '''Take the int, make 18 bits, then make list of 2-bit numbers (A to I)'''
    bin_x = bin(x)[2:].zfill(18)
    return [bin_x[i:i + 2] for i in range(0, 18, 2)]


def gs_encode(gs_list):
    '''
    Encode the list of 9 subfields 
    (2-bit each) into a single integer.
    '''
    try:
        new_bin_num = ''.join(gs_list)
        bin_num = int(new_bin_num, 2)  
        return bin_num
    except Exception as e:
        print_error(e, "gs_encode")
        return None


def check_winner(board):
    '''
    Check rows, columns, 
    and diagonals for a winner.
    '''
    def all_equal(lst):
        return lst[0] in ('01', '10') and all(x == lst[0] for x in lst)
    # print(f"Checking for winner on board: {board}")

    # Check rows
    for row in board:
        if all_equal(row):
            print(f"Winner found in row: {row}")
            return 'X' if row[0] == '01' else 'O'

    # Check columns
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        if all_equal(column):
            print(f"Winner found in column: {column}")
            return 'X' if column[0] == '01' else 'O'

    # Check diagonals
    diag1 = [board[i][i] for i in range(3)]
    if all_equal(diag1):
        print(f"Winner found in diagonal: {diag1}")
        return 'X' if diag1[0] == '01' else 'O'
    
    diag2 = [board[i][2 - i] for i in range(3)]
    if all_equal(diag2):
        print(f"Winner found in diagonal: {diag2}")
        return 'X' if diag2[0] == '01' else 'O'

    # No winner
    print("No winner yet.")
    return None


def random_move(board):
    '''
    Randomly select an empty square 
    for the server's move.
    '''
    empty_squares = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '00']
    if empty_squares:
        return random.choice(empty_squares)
    return None


def purge_inactive_games():
    '''
    Remove games that haven't had 
    interaction in the last 5 minutes.
    '''
    current_time = time.time()
    to_delete = []
    for game_id, game_data in GAMES_DIC.items():
        if current_time - game_data['last_interaction'] > TIMEOUT:
            to_delete.append(game_id)

    for game_id in to_delete:
        del GAMES_DIC[game_id]
        del GAMES_LOCKS[game_id]
        print(f"Purged inactive game: {game_id}")


def handle_error(udp_sock, game_id, message_id, flags, game_state, error_msg, ip, port):
    '''Handles error response by setting the ERROR_FLAG and sending the message back.'''
    flags |= ERROR_FLAG
    error_response = msg.encode_message(game_id, message_id, flags, game_state, error_msg)
    msg.send_data(udp_sock, (ip, port), error_response)
    print(f"Error handled for game {game_id}: {error_msg}")


def incoming_games(incoming_data, ip, port, udp_sock):
    '''
    Handles incoming game requests.
    '''
    if incoming_data:
        try:
            game_id, message_id, flags, game_state, message = msg.decode_message(incoming_data)
        except Exception as e:
            print_error(e, "decode_message")
            return
        # Get rid of the games over 5 minutes
        purge_inactive_games()

        if game_id not in GAMES_DIC and (message_id != 0 or flags != 0 or game_state != 0):
            handle_error(udp_sock, game_id, message_id, flags, game_state, "Invalid Game ID", ip, port)
            return

        # New game
        if game_id not in GAMES_DIC:
            # Randomly assign X or O to the player
            player_is_x = random.choice([True, False])
            player_flag = X_MOVE_FLAG if player_is_x else O_MOVE_FLAG

            # Initialize game state
            new_message = f"You are {'X' if player_is_x else 'O'}. Pick a move."
            GAMES_DIC[game_id] = {
                'lock': threading.RLock(),
                'message_id': message_id,
                'flags': player_flag,  # Assign turn to player
                'game_state': game_state,
                'message': new_message,
                'last_interaction': time.time()  # Track last interaction time
            }
            GAMES_LOCKS[game_id] = threading.RLock()
            print(f"New game created: {game_id}, Player is {'X' if player_is_x else 'O'}")

            response = msg.encode_message(game_id, message_id, player_flag, game_state, new_message)
            msg.send_data(udp_sock, (ip, port), response)
            return

        # Game exists, process the player's move
        with GAMES_LOCKS[game_id]:
            current_game = GAMES_DIC[game_id]
            #Checking serial ID
            if message_id != (current_game['message_id'] + 1) % 256:
                handle_error(udp_sock, game_id, message_id, flags, game_state, "Invalid Message ID", ip, port)
                return

            current_board = gs_decode(current_game['game_state'])
            incoming_board = gs_decode(game_state)

            # print(f"Current board state: {current_board}")
            # print(f"Incoming board state: {incoming_board}")
            # Update game state with the player's move
            current_game['game_state'] = gs_encode(incoming_board)

            # Check for winner or tie
            winner = check_winner(incoming_board)
            if winner == 'X':
                print("X has won the game.")
                current_game['flags'] |= X_WIN_FLAG
                current_game['flags'] &= ~O_MOVE_FLAG 
                current_game['flags'] &= ~X_MOVE_FLAG
                message = "X wins!"
            elif winner == 'O':
                print("O has won the game.")
                current_game['flags'] |= O_WIN_FLAG
                current_game['flags'] &= ~X_MOVE_FLAG 
                current_game['flags'] &= ~O_MOVE_FLAG
                message = "O wins!"
            elif not any('00' in row for row in incoming_board):
                print("The game has ended in a tie.")
                current_game['flags'] |= TIE_FLAG
                current_game['flags'] &= ~(X_MOVE_FLAG | O_MOVE_FLAG) 
                message = "It's a tie!"
            else:
                # print(f"Server is making a move (O's turn).")
                move = random_move(incoming_board)
                if move:
                    row, col = move
                    # print(f"Server (O) moves to position ({row}, {col})")
                    if current_game['flags'] & X_MOVE_FLAG:  # X's turn
                        incoming_board[row][col] = '01'
                        current_game['flags'] ^= X_MOVE_FLAG  # Switch to O
                        current_game['flags'] |= O_MOVE_FLAG
                        message = "O's move next"
                    elif current_game['flags'] & O_MOVE_FLAG:  # O's turn
                        incoming_board[row][col] = '10'
                        current_game['flags'] ^= O_MOVE_FLAG  # Switch to X
                        current_game['flags'] |= X_MOVE_FLAG
                        message = "X's move next"

                # Update game state after server's move
                current_game['game_state'] = gs_encode([item for sublist in incoming_board for item in sublist])
                print(f"Game state after server's move: {current_game['game_state']}")

            # Adding one the serials id
            current_game['message_id'] = (current_game['message_id'] + 1) % 256

            # Update last interaction time
            current_game['last_interaction'] = time.time()

            # Send the updated game state back to the client
            new_game_msg = msg.encode_message(game_id, current_game['message_id'], current_game['flags'], current_game['game_state'], message)
            print(f"Sending message to client: {message}")
            msg.send_data(udp_sock, (ip, port), new_game_msg)
            # print("Message sent to client.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Not enough arguments. Please provide IP address and port.")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])

    udp_sock = socket(AF_INET, SOCK_DGRAM)
    udp_sock.bind((ip, port))
    print(f"Server listening on {ip}:{port}")

    # Use a ThreadPoolExecutor to manage threads
    executor = ThreadPoolExecutor(max_workers=10)

    try:
        while True:
            incoming_data, ip, port = recv_data(udp_sock)
            if incoming_data:
                executor.submit(incoming_games, incoming_data, ip, port, udp_sock)
    except KeyboardInterrupt:
        print("Shutting down server...")
        udp_sock.close()
        sys.exit(0)

import random
from messaging import decode_message, encode_message

def test_message_encoding_decoding():
    # Define test values (use some edge cases too)
    game_id = random.randint(0, 0xFFFFFF)  # 24-bit game ID
    message_id = random.randint(0, 0xFF)  # 8-bit message ID
    flags = random.randint(0, 0x3FFF)  # 14-bit flags
    game_state = random.randint(0, 0x3FFFF)  # 18-bit game state
    utf_message = "Test player message"

    print("Original values:")
    print(f"Game ID: {game_id}, Message ID: {message_id}, Flags: {flags}, Game State: {game_state}")
    print(f"UTF Message: {utf_message}")

    # Encode the message
    encoded_data = encode_message(game_id, message_id, flags, game_state, utf_message)

    # Decode the message
    decoded_game_id, decoded_message_id, decoded_flags, decoded_game_state, decoded_message = decode_message(encoded_data)

    print("\nDecoded values:")
    print(f"Game ID: {decoded_game_id}, Message ID: {decoded_message_id}, Flags: {decoded_flags}, Game State: {decoded_game_state}")
    print(f"UTF Message: {decoded_message}")

    # Verify that the original and decoded values match
    assert game_id == decoded_game_id, "Game ID mismatch"
    assert message_id == decoded_message_id, "Message ID mismatch"
    assert flags == decoded_flags, "Flags mismatch"
    assert game_state == decoded_game_state, "Game state mismatch"
    assert utf_message == decoded_message, "UTF message mismatch"

    print("\nTest passed!")


# Run the test
test_message_encoding_decoding()

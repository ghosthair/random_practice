import practice

# mask_var = 0x3FFFF
# var = (1 << 17) & mask_var
# bit_string = bin(var)[2:].zfill(18)
# print(bit_string)
# print(len(bit_string))

# test_var = 1 << 17
# bin_test_var = bin(test_var)
# print(bin_test_var[4:6])
# print(test_var)
# print(bin(test_var)[2:])
# print(len(bin(test_var)[2:]))

# x = 255
# # bin_x = bin(x)[2:].zfill(18)
# y = practice.gs_decode(x)
# print(y)
# print(type(y))
# z = practice.gs_encode(y)
# z_bin = bin(z)[2:].zfill(18)
# print(z)
# print(type(z))
# print(f"Binary: {z_bin}")
# print(f"Length: {len(z_bin)}")
# print(f"Type: {type(z_bin)}")
# game_list = ['11', '11', '11', '00', '10', '10', '00', '00', '00']
# game_list = [['11', '11', '11'], ['00', '10', '10'], ['00', '00', '00']]
# print(game_list)
# x = practice.gs_status(game_list)
# print(f"New list:\n{x}")

game_list = [
    '01', '10', '01',  # X, O, X
    '10', '01', '10',  # O, X, O
    '01', '00', '10'   # X, empty, O
]
print(game_list)
board = practice.gs_status(game_list)
practice.check_winner(board)
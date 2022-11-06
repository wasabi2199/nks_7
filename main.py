file = open("99535.56207b3fc1489dae.dat", "r")
pairs = file.readlines()
for i in range(len(pairs)):
    pairs[i] = int(pairs[i], base=16)
key_count = {}
key_biases = {}


def test(actual_approximation, u_4, x):
    result = 0
    if actual_approximation == 1:
        result = ((x >> 15) ^ (u_4 >> 1)) & 1
    if actual_approximation == 2:
        result = ((x >> 10) ^ (u_4 >> 4) ^ u_4) & 1
    if actual_approximation == 3:
        result = ((x >> 10) ^ (u_4 >> 1)) & 1
    return result


def inverse_s_box(input):
    left = (input & 0xF0) >> 4
    right = input & 0x0F
    s_box = [3, 9, 2, 6, 10, 0, 1, 4, 11, 12, 14, 5, 8, 13, 15, 7]
    output = 0

    o_left = s_box[left]
    o_right = s_box[right]

    output |= o_left << 4
    output |= o_right
    return output


def key_attack(actual_approximation):
    C = 0
    key_biases.clear()
    key_count.clear()
    max_bias = 0
    partial_subkey = 0
    for x in range(len(pairs)):
        ct = pairs[x]
        y = 0
        if actual_approximation == 1:
            y = (ct & 0xF000) >> 12
        if actual_approximation == 2:
            y = (ct & 0x0FF0) >> 4
        if actual_approximation == 3:
            y = (ct & 0x000F)
        for key in range(256):
            input = y ^ key
            u_4 = inverse_s_box(input)
            if test(actual_approximation, u_4, x):
                if key not in key_count.keys():
                    key_count[key] = 1
                else:
                    key_count[key] = key_count[key] + 1

    C = len(pairs)

    for key in key_count:
        count = key_count[key]
        bias = abs(count - (C / 2)) / C
        key_biases[key] = bias
        if bias > max_bias:
            max_bias = bias
            partial_subkey = key
    print("Subkey: ", hex(partial_subkey), " Bias: ", max_bias)
    return partial_subkey


def attack():
    key = 0

    # 0xF000
    s_1 = key_attack(1)
    key |= (s_1 << 12)

    #0x0FF0
    s_2 = key_attack(2)
    key |= (s_2 << 4)

    #0x000F
    s_3 = key_attack(3) & 0x000F
    key |= (s_3)

    print("K5: ", hex(key))
    #return key


attack()
import itertools

def pack_items_recursive(bin_dims, orientation_list):
    W, H, L = bin_dims

    if W <= 0 or H <= 0 or L <= 0:
        print("The width, length and height of bin must larger than 0.")
        return 0, 0

    n_optimal = 0
    total_packed = 0
    for a, b, c in orientation_list:
        n = (W // a) * (H // b) * (L // c)

        if n > n_optimal:
            n_optimal = n

        remaining_W = W - (W // a)
        remaining_H = H - (H // b)
        remaining_L = L - (L // c)

        remaining_n = 1
        while remaining_n >= 1: # when remaining_n < 1, stop
            if remaining_W <= 0 or remaining_H <= 0 or remaining_L <= 0:
                break
            else:
                remaining_n, _ = pack_items_recursive((remaining_W, remaining_H, remaining_L), [x for x in orientation_list if x != (a, b, c)])

            if n_optimal + remaining_n > total_packed:
                total_packed = n_optimal + remaining_n

    return n_optimal, total_packed

item_dimensions = (3, 4, 5)
orientation_list = list(itertools.permutations(item_dimensions))
print(orientation_list)
def transpose(array):
    array = array[:]  # make copy to avoid changing original
    n = len(array)
    for i, row in enumerate(array):
        array[i] = row + [None for _ in range(n - len(row))]

    array = list(zip(*array))

    for i, row in enumerate(array):
        array[i] = [elem for elem in row if elem is not None]
    array_clear = []
    for line in array:
        if len(line) > 0:
            array_clear.append(line)

    return array_clear

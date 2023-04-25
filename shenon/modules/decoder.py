from modules.decoder_utils.BST import Node


def codes_to_tree(matrix, line):
    for first_byte in matrix.keys():
        tree = Node()
        for second_byte in matrix[first_byte].keys():
            tree.insert(0, matrix[first_byte][second_byte], second_byte)

        matrix[first_byte] = tree

    tree = Node()
    for first_byte in line.keys():
        tree.insert(0, line[first_byte], first_byte)

    return tree


def tree_search(tree, buffer, input_file, eof_pos):
    node, buffer = tree.find_code(buffer)
    output_byte = node.data
    eof = False

    while not output_byte:
        input_byte = str(bin(int.from_bytes(input_file.read(1), 'little')))[2:]

        buffer += '0' * (8 - len(input_byte)) + input_byte

        node, buffer = node.find_code(buffer)
        output_byte = node.data

    if input_file.tell() == eof_pos:
        eof = True

    return eof, output_byte, buffer


def decode(input_filename, output_filename, matrix, line):
    with open(input_filename, "rb") as input_file, open(output_filename, "wb") as output_file:
        eof_pos = input_file.seek(0, 2)
        input_file.seek(0, 0)

        adj_len = input_file.read(1)
        if not adj_len:
            return
        adj_len = int.from_bytes(adj_len, 'little')

        buffer = input_file.read(1)
        if not buffer:
            return
        buffer = str(bin(int.from_bytes(buffer, 'little')))[2:]
        buffer = '0' * (8 - len(buffer)) + buffer

        eof, first_byte, buffer = tree_search(line, buffer, input_file, eof_pos)
        output_file.write(first_byte.to_bytes(1, 'little'))

        while not eof:
            eof, first_byte, buffer = tree_search(matrix[first_byte], buffer, input_file, eof_pos)
            output_file.write(first_byte.to_bytes(1, 'little'))

        buffer = buffer[:len(buffer) - adj_len]
        while buffer:
            eof, first_byte, buffer = tree_search(matrix[first_byte], buffer, input_file, eof_pos)
            output_file.write(first_byte.to_bytes(1, 'little'))


def run(input_filename, output_filename, matrix, line):
    line = codes_to_tree(matrix, line)
    decode(input_filename, output_filename, matrix, line)

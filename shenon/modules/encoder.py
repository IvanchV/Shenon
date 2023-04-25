from modules.encoder_utils import tables_creator as tc


def encode(input_filename, output_filename, matrix, line):
    with open(input_filename, "rb") as input_file, open(output_filename, "wb") as output_file:
        first_byte = input_file.read(1)
        if not first_byte:
            return
        first_byte = int.from_bytes(first_byte, 'little')
        byte = line[first_byte]

        adj_len = 0
        output_file.write(adj_len.to_bytes(1, 'little'))

        while True:
            if len(byte) >= 8:
                output_file.write(int(byte[:8], 2).to_bytes(1, 'little'))
                byte = byte[8:]

            second_byte = input_file.read(1)
            if not second_byte:
                if byte:
                    adj_len = 8 - len(byte)
                    byte += '0' * adj_len
                    output_file.write(int(byte, 2).to_bytes(1, 'little'))
                break
            second_byte = int.from_bytes(second_byte, 'little')

            byte += matrix[first_byte][second_byte]

            first_byte = second_byte

    with open(output_filename, "rb+") as output_file:
        output_file.write(adj_len.to_bytes(1, 'little'))


def run(input_filename, output_filename):
    matrix, line = tc.create_tables(input_filename)
    encode(input_filename, output_filename, matrix, line)

    return matrix, line

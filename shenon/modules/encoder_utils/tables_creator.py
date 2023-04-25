import math
from fractions import Fraction


def analyze_file(input_filename, matrix, line):
    with open(input_filename, "rb") as input_file:
        first_byte = input_file.read(1)
        if not first_byte:
            return
        first_byte = int.from_bytes(first_byte, 'little')

        while True:
            if first_byte in line.keys():
                line[first_byte] += 1
            else:
                line[first_byte] = Fraction(1)
            
            second_byte = input_file.read(1)
            if second_byte:
                second_byte = int.from_bytes(second_byte, 'little')
            else:
                break

            if first_byte in matrix.keys():
                if second_byte in matrix[first_byte].keys():
                    matrix[first_byte][second_byte] += 1
                else:
                    matrix[first_byte][second_byte] = Fraction(1)
            else:
                matrix[first_byte] = {second_byte: Fraction(1)}

            first_byte = second_byte


def shannon_algo(line, line_sum, table):
    def fraction_to_bin(fraction, bin_len):
        result = ''

        for i in range(bin_len):
            fraction *= 2
            result += '0' if fraction < 1 else '1'
            fraction %= 1

        return result

    prob_sum = 0
    for i in range(len(line)):
        line[i] = list(line[i])
        prob = line[i][1] / line_sum
        code_len = math.ceil(-math.log2(prob)) if prob != 1 else 1
        code = fraction_to_bin(prob_sum, code_len)
        prob_sum += prob
        line[i][1] = code

    for i in range(len(line)):
        code = line[i][1]

        for j in range(len(line[i][1]) - 1):
            cut = True
            short_code = code[:-1]

            for k in range(len(line)):
                if i != k and line[k][1].find(short_code) == 0:
                    cut = False
                    break

            if cut:
                code = short_code
            else:
                break

        table[line[i][0]] = code


def lines_to_codes(matrix, line):
    for first_byte in matrix.keys():
        line_sum = sum(matrix[first_byte].values())
        shannon_algo(
            sorted(list(matrix[first_byte].items()), key=lambda x: x[1], reverse=True),
            line_sum,
            matrix[first_byte]
        )

    line_sum = sum(line.values())
    shannon_algo(
        sorted(list(line.items()), key=lambda x: x[1], reverse=True),
        line_sum,
        line
    )


def create_tables(input_filename):
    bigram_matrix = {}
    first_byte_line = {}

    analyze_file(input_filename, bigram_matrix, first_byte_line)
    lines_to_codes(bigram_matrix, first_byte_line)

    return bigram_matrix, first_byte_line

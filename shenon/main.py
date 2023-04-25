from modules import encoder as enc, decoder as dec
import time

INPUT_FILE = '1.txt'
ENCODED_FILE = 'encoded.txt'
DECODED_FILE = 'decoded.txt'


if __name__ == '__main__':
    start_time = time.process_time()
    matrix, line = enc.run(INPUT_FILE, ENCODED_FILE)
    dec.run(ENCODED_FILE, DECODED_FILE, matrix, line)
    print("--- %s seconds ---" % (time.process_time() - start_time))

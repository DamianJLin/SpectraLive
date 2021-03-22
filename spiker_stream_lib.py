import numpy as np


def read_arduino(ser, input_buffer_size):
    data = ser.read(input_buffer_size)
    out = [(int(data[i])) for i in range(0, len(data))]
    return out


def process_data(data):
    data_in = np.array(data)
    result = []
    i = 1
    while i < len(data_in)-1:
        if data_in[i] > 127:
            # Found beginning of frame
            # Extract one sample from 2 bytes
            intout = (np.bitwise_and(data_in[i], 127))*128
            i += 1
            intout = intout + data_in[i]
            result = np.append(result, intout)
        i += 1
    return result

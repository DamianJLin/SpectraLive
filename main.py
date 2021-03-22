import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import spiker_stream_lib as ssl

# Read example data
baud_rate = 230400
cport = 'COM3'  # Set the correct port before you run it.
ser = serial.Serial(port=cport, baudrate=baud_rate)

# Take continuous data stream
inputBufferSize = 10000  # keep in the range [2000, 20000]
ser.timeout = inputBufferSize / 20000.0  # set read timeout, 20000 is one second
ser.set_buffer_size(rx_size=inputBufferSize)

total_time = 20.0
max_time = 10.0
N_loops = int(20000.0 / inputBufferSize * total_time)

T_acquire = inputBufferSize / 20000.0  # length of time that data is acquired for
N_max_loops = int(max_time / T_acquire)  # total number of loops to cover desire time window

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
plt.ion()
fig.show()
fig.canvas.draw()

for k in range(0, N_loops):
    data = ssl.read_arduino(ser, inputBufferSize)
    data_temp = ssl.process_data(data)
    if k <= N_max_loops:
        if k == 0:
            data_plot = data_temp
        else:
            data_plot = np.append(data_temp, data_plot)
        t = (min(k + 1, N_max_loops)) * inputBufferSize / 20000.0 * np.linspace(0, 1, data_plot.size)
    else:
        data_plot = np.roll(data_plot, len(data_temp))
        data_plot[0:len(data_temp)] = data_temp
    t = (min(k + 1, N_max_loops)) * inputBufferSize / 20000.0 * np.linspace(0, 1, data_plot.size)

    ax1.clear()
    ax1.set_xlim(0, max_time)
    plt.xlabel('time [s]')
    ax1.plot(t, data_plot)
    fig.canvas.draw()
    plt.show()


# close serial port if necessary
if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()

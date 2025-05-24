import serial

SERIAL_PORT = '/dev/ttyACM0'

def open_gate(entry=True):
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
    cmd = 'OPEN_ENTRY' if entry else 'OPEN_EXIT'
    ser.write((cmd + '\n').encode())
    ack = ser.readline().decode().strip()
    ser.close()
    return ack
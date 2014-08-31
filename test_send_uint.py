import serial
import argparse

parser = argparse.ArgumentParser(description='Kryptoradio Test #1.')
parser.add_argument('device', type=str, nargs=1, help='Serial device')
args = parser.parse_args()

portname = args.device[0]
print("Using serial port device '"+portname+"'.")

try:
    ser = serial.Serial(portname, 9600, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)
except serial.serialutil.SerialException, ex:
    print(str(ex))
    quit()

while 1:
    for x in range(0,255):
        ser.write(chr(x))


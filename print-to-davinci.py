import time, serial, sys

ser = serial.Serial(
  port=sys.argv[1],
  baudrate=115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS
)
ser.isOpen()

def toHexString(text):
  return ' '.join(x for x in str(text))

def printOutputIfAvailable():
  time.sleep(1) # wait one second before attempting to read response
  out = ""
  while ser.inWaiting() > 0:
    out += ser.read(ser.inWaiting()).decode('utf-8')
  if out != '':
    print(">> " + toHexString(out))
    print(">> " + out)

### STATUS INFORMATION THAT XYZware polls periodically
ser.write(bytes("XYZ_@3D:" + '\n', 'utf-8'))
printOutputIfAvailable()
ser.write(bytes("XYZ_@3D:6" + '\n', 'utf-8'))
printOutputIfAvailable()
ser.write(bytes("XYZ_@3D:5" + '\n', 'utf-8'))
printOutputIfAvailable()
ser.write(bytes("XYZ_@3D:8" + '\n', 'utf-8'))
printOutputIfAvailable()

### Check printer is ready to offline print from SD card?
ser.write(bytes("XYZ_@3D:4" + '\n', 'utf-8'))
printOutputIfAvailable()


### Send gcode to printer
with open(sys.argv[2], 'rb') as fin:
    gcode = fin.read()
    gcode = str.replace(gcode.decode('utf-8'), '\n', '\r\n') # XYZware includes carriage feed
    gcode = bytearray(gcode, 'utf-8')
    gcode.append(0x00);
    gcode.append(0x00);
    gcode.append(0xB9); # some sort of checksum? how to calculate this?
    gcode.append(ord('.'));
    m1_gcode = bytearray("M1:MyTest,711,0.3.16,EE1_OK,EE2_OK", 'utf-8') + gcode
    print(' '.join(x for x in str(m1_gcode)))
    
    ser.write(bytes("M1:MyTest,711,0.3.16,EE1_OK,EE2_OK", 'utf-8'))
    ser.flush()
    ser.write(gcode)
    ser.flush()
    printOutputIfAvailable()

ser.write(bytes("XYZ_@3D_S10_1" + '\n', 'utf-8'))

# while(True):
#   printOutputIfAvailable()

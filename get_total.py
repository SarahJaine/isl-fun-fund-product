import time

import requests
import serial
from serial.tools.list_ports_posix import comports


iterator = sorted(comports())
for n, (port, desc, hwid) in enumerate(iterator, 1):
    if 'Bluetooth' in port:
        continue
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(1)
        print("ser is:", ser)
    except Exception as e:
        print(e)


domain = 'https://funfund.isl.co/totals/'
value_old = None

while True:
    try:
        r = requests.get(domain)

        if r.status_code != 200:
            print('Requested resource returned {0}'.format(r.status_code))
        else:
            return_value = r.json()['value']
            value_new, decimals = return_value.split('.')
            if value_new != value_old:
                ser.write('{}'.format(value_new).encode('utf-8'))
                ser.flush()
                value_old = value_new
                print(value_old)

    except Exception as e:
        print(e)
        break

    time.sleep(5)


ser.close()

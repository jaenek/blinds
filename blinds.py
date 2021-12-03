from machine import Pin
import time

ID = open(id).read().strip()

xciver = Pin(13, Pin.OUT)
timing = {
    -1: [4716, 1384],
    0: [700, 330],
    1: [330, 700],
}

SYNC = -1
def _send(type):
    xciver.value(1)
    time.sleep_us(timing[type][0])
    xciver.value(0)
    time.sleep_us(timing[type][1])

def send(bits, len):
    for i in range(len-1, -1, -1):
        if bits & (1<<i):
            _send(1)
        else:
            _send(0)

def send_command(cmd, blind_nr):
    if blind_nr < 0 or blind_nr > 15:
        print('ERROR: blind_nr must be between 0 and 15')
        return False

    if cmd not in ['up', 'down', 'stop']:
        print('ERROR: no such command "%s"' % cmd)
        return False

    if cmd == 'up':
        _send(SYNC)
        send(ID, 28)
        send(15 - blind_nr, 4)
        send(0xEE, 8)
    elif cmd == 'down':
        _send(SYNC)
        send(ID, 28)
        send(15 - blind_nr, 4)
        send(0xCC, 8)
    elif cmd == 'stop':
        _send(SYNC)
        send(ID, 28)
        send(15 - blind_nr, 4)
        send(0xAA, 8)

    time.sleep_ms(10)

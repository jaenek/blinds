import network, re, socket, time
from blinds import send_command

# wifi
station = network.WLAN(network.STA_IF)

station.active(True)
if not station.isconnected():
    station.connect('Whyfi', 'ef21kre58drz&')

while station.isconnected() == False:
    pass

print(station.ifconfig())

# query string parse
def qs_parse(qs):
    pairs = qs.split('?')
    if len(pairs) == 1:
        return {}
    pairs = pairs[1].split('&')
    params = {}
    for pair in pairs:
        key, value = pair.split('=')
        params[key] = value
    return params

# server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request, 'utf-8')
        method = request.split()[0]
        query = request.split()[1]
        print('[%s] %s: %s' % (method, str(addr), query))
        response = open('index.html').read()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        params = qs_parse(query)
        try:
            print('sending commmand "%s" to blind "%s"' % (params['cmd'], params['blind_nr']))
            send_command(params['cmd'], int(params['blind_nr']))
            send_command(params['cmd'], int(params['blind_nr']))
            send_command(params['cmd'], int(params['blind_nr']))
        except KeyError:
            print('dupa')
            pass

    except OSError as e:
        conn.close()
        print('Connection closed')

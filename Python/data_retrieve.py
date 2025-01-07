import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#s.connect(('172.20.241.9', 20000))
#s.sendall(b'22\n')
s.settimeout(20)
try:
    s.connect(('172.20.241.9', 20000))
    s.sendall(b'22\n')
except socket.timeout:
    print("Connection timed out.")

chunks = []
while True:
    data = s.recv(1024)
    if len(data) == 0:
        break
    chunks.append(data.decode('utf-8'))

for i in chunks:
    print(i, end = '')
    with open('test.txt', 'w') as f:
        f.write(i)

s.close()

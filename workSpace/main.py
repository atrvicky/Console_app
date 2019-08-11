import boot
import usocket as socket
import ubinascii

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)
boot.log('server enabled on port 80')

while True:
  conn, addr = sock.accept()
  boot.log(addr)
  boot.log('incoming from: %s' % str(addr[0]))
  
  request = str(conn.recv(1024))
  boot.log('req: %s' % request)
  
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/plain\n')
  conn.send('Connection: close\n\n')
  conn.send('Access-Control-Allow-Origin: *')
  conn.sendall('Hello!')
  conn.close()

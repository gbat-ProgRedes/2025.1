import socket

HOST = '10.25.1.189'
PORT = 12345

tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcpSock.bind((HOST, PORT))
tcpSock.listen(5)

while True:
    print ('Esperando conexão ....')
    tcpCon, client = tcpSock.accept()
    print (f'Conexao de {client}')
    for _ in range(5):
        msg = tcpCon.recv(1024)
        print (f'recebi {msg.decode()} -> enviei {msg.decode()}')
        tcpCon.send(msg)
    tcpCon.close()
    
tcpSock.close()

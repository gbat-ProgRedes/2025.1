import socket

PORT = 50000
SERVER = ('10.27.1.120', PORT)

sockClient = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        msg = input ("Digite msg:")
        sockClient.sendto(msg.encode(), (SERVER))
        source, data = sockClient.recvfrom(512)
        print (source.decode())
    except Exception as e:
        print (f"Erro. Processamento de mensagem.", e)          
socket.close()

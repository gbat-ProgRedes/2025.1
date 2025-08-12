import socket, threading, random, sys

PORT = 50000
SERVER = 'localhost'

def trataUsuario():
    totMsgs = random.randint(1, 5)
    nMsg = 1
    try:
        while nMsg <= totMsgs:
            msg = input (f"Digite msg ({nMsg}): ")
            if msg:
                sockClient.send((f"msg {nMsg} -> "+msg).encode())
            nMsg += 1
        sockClient.close()
    except Exception as e:
        print ("Fechando o programa porque o servidor saiu abruptamente.", e)

def trataServidor():
    try:
        while True:
            msg = sockClient.recv(4096)
            print (msg.decode())
    except Exception as e:
        print ("Fechando o programa porque:", e)
        print ("   1. limite de msgs suportado alcancado; ou ...")
        print ("   2. o servidor caiu abruptamente.")
    
sockClient = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sockClient.connect((SERVER, PORT))

tUsuario  = threading.Thread(target=trataUsuario)
tServidor = threading.Thread(target=trataServidor)

tServidor.start()
tUsuario.start()

tServidor.join()
tUsuario.join()
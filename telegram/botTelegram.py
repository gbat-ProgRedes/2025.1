import socket, ssl, json

TOKEN = "SEU TOKEN"
HOST  = "api.telegram.org"
PORT  = 443

def conn_to():
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((HOST, PORT))
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose)
    return context.wrap_socket(sock_tcp, server_hostname=HOST)

def send_get (sock_tcp, cmd):
    resource = "/bot"+TOKEN+"/"+cmd
    sock_tcp.send (("GET "+resource+" HTTP/1.1\r\n"+
                    "Host: "+HOST+"\r\n"+
                    "\r\n").encode("utf-8"))
        
def get_reponse(sock_tcp):
    answer = sock_tcp.recv(4096)
    header_body = answer.split(b"\r\n\r\n")
    headers, body = header_body[0].decode().split("\r\n"), header_body[1]

    status_line = headers[0]
    if status_line.split()[1] == "200":
        for header in headers[1:]:
            field_value = header.split(":")
            if field_value[0] == "Content-Length":
                to_read = int (field_value[1])
                break
    
        to_read -= len(body)
        while to_read > 0:
            segment = sock_tcp.recv(4096)
            body += segment
            to_read -= len(segment)
    
        return (status_line, headers[1:], json.loads(body.decode()))    
    return (None, None, None)

def get_updates():
    sock_tcp = conn_to()
    send_get(sock_tcp, "getUpdates")
    status_line, headers, body = get_reponse(sock_tcp)
    
    for update in body["result"]:
        print (update["message"]["chat"]["first_name"], "->", update["message"]["text"])

get_updates()

import socket, ssl, json, time
import mytokens

HOST  = "api.telegram.org"
PORT  = 443

def conn_to():
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((HOST, PORT))
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose)
    return context.wrap_socket(sock_tcp, server_hostname=HOST)

def send_get (sock_tcp, resource, headers):
    sock_tcp.send (("GET "+resource+" HTTP/1.1\r\n"+
                    headers+
                    "\r\n").encode("utf-8"))
        
def send_post (sock_tcp, resource, headers, body): 
    body = body.encode("utf-8")
    sock_tcp.send (("POST "+resource+" HTTP/1.1\r\n"+
                   "Content-Length: "+str(len(body))+"\r\n"+headers+
                   "\r\n").encode("utf-8"))
    sock_tcp.send(body)
    
def get_response(sock_tcp):
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

def get_updates(sock_tcp, offset = 0):
    cmd = f"getUpdates?offset={offset}"
    resource = "/bot"+mytokens.TELEGRAM_TOKEN+"/"+cmd
    headers = "Host: "+HOST+"\r\n"
    send_get(sock_tcp, resource, headers)
    status_line, headers, body = get_response(sock_tcp)    
    return body["result"]

def show_update(update):
    print (update["message"]["chat"]["first_name"], "->", update["message"]["text"])
    
def answer_update(update):
    sock_tcp = conn_to()
    chat_id  = update["message"]["chat"]["id"]
    
    answer = input ("Sua resposta: ")
    body = '{"chat_id":'+str(chat_id)+', "text":"'+answer+'"}'
    
    cmd = "/sendMessage"
    resource = "/bot"+mytokens.TELEGRAM_TOKEN+cmd
    headers = ("Content-Type: application/json\r\n"+
               "Host: "+HOST+"\r\n")
    send_post(sock_tcp, resource, headers, body)
    get_response(sock_tcp)
    sock_tcp.close()
    return update["update_id"]

def main():
    sock_tcp = conn_to()
    print ("Aceitando updates ....")
    last_update = 0
    while True:
        updates = get_updates(sock_tcp, last_update+1)
        for update in updates:
            show_update(update)
            last_update = answer_update(update)
        print ("-------------")
        time.sleep(2)
    sock_tcp.close()
    
main()
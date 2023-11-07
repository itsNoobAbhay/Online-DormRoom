import socket
import pickle
import threading

def broadcast(client_conn, clients, msg):
    try:
        for c in clients:
            if c != client_conn:
                c.send(msg)
                print(f'BROADCAST TO {c} SUCCESSFULLY!!')
            
            else:
                print(f'CLIENT NOT FOUND!')
    except Exception as e:
        print(f'ERROR IN BROADCASTING MESSAGES ! : {e}')


def handle_client(client_conn, client_addr, clients):
    try:
        while True:
            msg = client_conn.recv(2048)
            if not msg:
                break  # The client has disconnected

            msg_dis = pickle.loads(msg)
            print(msg_dis)

            if len(clients) > 1:
                broadcast(client_conn, clients, msg)

    except ConnectionAbortedError as e:
        print(f'CONNECTION ABORTED BY CLIENT: {client_addr[0]}: {e}')
        
    except ConnectionRefusedError as e:
        print(f'CONNECTION REFUSED BY CLIENT: {client_addr[0]}: {e}')
        
    except EOFError as e:
        print(f'CLIENT DISCONNECTED: {client_addr[0]}: {e}')
        
    except Exception as e:
        print(f'UNKNOWN ERROR IN RECEIVING DATA: {client_addr[0]}: {e}')
        
    finally:
        remove_client(client_conn)
            

def remove_client(client_conn):
    clients.remove(client_conn)
    
def run(server, clients):
    
    while True:
        try:
            client_conn, client_addr = server.accept()
            print(f'NEW CONNECTIONS FROM : {client_conn} : {client_addr[0]}')
            clients.append(client_conn)
            client_thread = threading.Thread(target= handle_client, args= (client_conn, client_addr, clients))
            client_thread.start()
            
        except Exception as e:
            print(f'ERROR IN ACCEPTING CLIENTS : {e}')
    

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5050
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print(f'SERVER HAS STARTED !!')
print(f'SERVER IS LISTENING ON {SERVER_IP} : {SERVER_PORT}')

run(server, clients)

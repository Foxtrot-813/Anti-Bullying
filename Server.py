import socket
import threading

host = '127.0.0.1'
port = 55550
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
online_admins = []
admins_id = []
online_users = []
users_id = []
reports = []


def forward_to_user(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "CRpa7Pf6@HMs^AH1z*8G":
                print("Stop request received")
                client.send("8@!gwYY$oK7eTV5aRWjg".encode('ascii'))
            if message.decode('utf-8') == "*In#8feAG7hJR2bm3fS":
                print("New report received.")
                for i in range(6):
                    info = client.recv(1024).decode('utf-8')
                    print(info, end='\n')

            if len(online_admins) > 0:
                online_admins[0].send(message)
        except:
            index = online_users.index(client)
            online_users.remove(client)
            print(f"Closing connection with: {client}")
            client.close()
            id_number = users_id[index]
            users_id.remove(id_number)
            print(f"User with ID: {id_number} has left the session.")
            print("=" * 80)
            break


def forward_to_admin(client):
    while True:
        try:
            message = client.recv(1024)
            if len(online_users) > 0:
                online_users[0].send(message)
        except:
            index = online_admins.index(client)
            online_admins.remove(client)
            print(f"Closing connection: {client}")
            client.close()
            id_number = admins_id[index]
            admins_id.remove(id_number)
            print(f"User with ID: {id_number} has left the session.")
            print("=" * 80)
            break


def handle_connections():
    while True:
        client, address = server.accept()
        print(f'Connected to {str(address)}')
        client.send('ID'.encode('ascii'))
        user_id = client.recv(1024).decode('ascii')

        if user_id == '#007':
            admins_id.append(user_id)
            online_admins.append(client)
            threading.Thread(target=forward_to_admin, args=(client,)).start()
        else:
            users_id.append(user_id)
            online_users.append(client)
            threading.Thread(target=forward_to_user, args=(client,)).start()

        print(f"Connection established.\nUser ID: {user_id}")
        print("=" * 80)


if __name__ == '__main__':
    print("Server is listening ...")
    handle_connections()

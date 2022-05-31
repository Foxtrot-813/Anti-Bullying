import socket
import threading

host = '127.0.0.1'
port = 55550
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
users_socket = []
users_id = []
admins_socket = []
admins_id = []


def handle_user(client):
    while True:
        try:
            message = client.recv(1024)
            for admin in admins_socket:
                admin.send(message)

        except:
            index = users_socket.index(client)
            users_socket.remove(client)
            print(f"Closing connection: {client}")
            client.close()
            id_number = users_id[index]
            users_id.remove(id_number)
            print(f"User with ID: {id_number} has left the session.")
            break


def handle_admin(client):
    while True:
        try:
            message = client.recv(1024)
            for user in users_socket:
                user.send(message)
        except:
            index = admins_socket.index(client)
            admins_socket.remove(client)
            print(f"Closing connection: {client}")
            client.close()
            id_number = admins_id[index]
            admins_id.remove(id_number)
            print(f"User with ID: {id_number} has left the session.")
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected to {str(address)}')
        client.send('ID'.encode('ascii'))
        user_id = client.recv(1024).decode('ascii')

        if user_id == '#007':
            admins_id.append(user_id)
            admins_socket.append(client)
            threading.Thread(target=handle_admin, args=(client,)).start()
        else:
            users_id.append(user_id)
            users_socket.append(client)
            threading.Thread(target=handle_user, args=(client,)).start()

        print(f"Connection established.\nUser ID: {user_id}")
        client.send('Connected to the server!'.encode('ascii'))


print("Server is listening ...")
receive()

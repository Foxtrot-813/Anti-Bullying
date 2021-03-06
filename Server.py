import socket
import threading
import sqlite3


def connect_db():
    sql = '''CREATE TABLE IF NOT EXISTS Reports(
                     ReportID INTEGER PRIMARY KEY AUTOINCREMENT,
                     CaseNr TEXT NOT NULL,
                     Name TEXT NOT NULL,
                     Email TEXT NOT NULL,
                     Description TEXT NOT NULL);'''
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute(sql, )
    conn.commit()
    conn.close()


connect_db()
host = '127.0.0.1'
port = 55550
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
online_admins = []
admins_id = []
online_users = []
users_id = []


def forward_to_admin(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "CRpa7Pf6@HMs^AH1z*8G":
                print("Stop request received")
                client.send("8@!gwYY$oK7eTV5aRWjg".encode('ascii'))

            if message.decode('utf-8') == "*In#8feAG7hJR2bm3fS":
                case = {'nr': '', 'name': '', 'email': '', 'incident': ''}
                print("New report received.")
                for k, v in case.items():
                    case[k] = client.recv(1024).decode('utf-8')
                sql = '''INSERT INTO Reports
                                (CaseNr, Name, Email, Description)
                                VALUES (?, ?, ?, ?)'''
                conn = sqlite3.connect('reports.db')
                cursor = conn.cursor()
                cursor.execute(sql, (case['nr'], case['name'], case['email'], case['incident']))
                conn.commit()
                conn.close()
                print("Successful.")

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


def forward_to_user(client):
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
        client.send('Y4mAB<3sr{Rp9!xTZ2yf'.encode('ascii'))
        user_id = client.recv(1024).decode('ascii')

        if user_id == '#007':
            admins_id.append(user_id)
            online_admins.append(client)
            threading.Thread(target=forward_to_user, args=(client,)).start()
        else:
            users_id.append(user_id)
            online_users.append(client)
            threading.Thread(target=forward_to_admin, args=(client,)).start()

        print(f"Connection established.\nUser ID: {user_id}")
        print("=" * 80)


if __name__ == '__main__':
    print("Server is listening ...")
    handle_connections()

import socket
import threading

admin_id = f"#007"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55550))

stop_thread = False


def receive():
    while True:
        global stop_thread
        if stop_thread is True:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'ID':
                client.send(admin_id.encode('ascii'))
            else:
                print(message)
        except ValueError:
            print(ValueError)
            client.close()
            break


def write():
    while True:
        if stop_thread is True:
            break
        try:
            message = f"{input('')}"
            client.send(message.encode('ascii'))
        except ValueError:
            print("Unexpected error!")
            print(ValueError)


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
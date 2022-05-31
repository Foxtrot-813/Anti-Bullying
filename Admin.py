import socket
import threading

host = '127.0.0.1'
port = 55550
admin_id = "#007"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

stop_conversation = False


def received_msg():
    while True:
        global stop_conversation
        if stop_conversation is True:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Y4mAB<3sr{Rp9!xTZ2yf':
                client.send(admin_id.encode('ascii'))
            if message == "CRpa7Pf6@HMs^AH1z*8G":
                print("User has left the session.")
                print("=" * 80)
            if message != "Y4mAB<3sr{Rp9!xTZ2yf" and message != "CRpa7Pf6@HMs^AH1z*8G":
                print(f"Received: {message}")
        except ValueError:
            client.close()
            print(ValueError)
            break


def send_msg():
    while True:
        if stop_conversation is True:
            break
        try:
            message = input('')
            client.send(message.encode('ascii'))
        except ValueError:
            print("Unexpected error!")
            print(ValueError)


if __name__ == '__main__':
    threading.Thread(target=received_msg).start()
    threading.Thread(target=send_msg).start()
    print("Waiting for incoming connections....")

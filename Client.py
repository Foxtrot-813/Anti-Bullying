import re
import random
import socket
import threading
from time import sleep
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

new_id = f"#{random.randint(1000, 9999)}"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

from_admin = ['']
from_user = ['']


class MainWindow(Screen):
    chat = ObjectProperty(None)


class SecondWindow(Screen):
    stop_conversations = False

    def connect_to_server(self):
        client.connect(('127.0.0.1', 55550))
        client.send(new_id.encode('ascii'))
        self.start_chat.disabled = True
        self.send_btn.disabled = False
        self.message_text.disabled = False
        self.message_text.hint_text = "Write a message."
        self.start_chat.text = "Connected"
        self.start_chat.background_color = (0, 1, 0, 3)
        self.exit_chat.background_color = (1.5, 0, 0, 1)
        threading.Thread(target=self.received).start()
        # threading.Thread(target=self.write).start()

    def received(self):
        while True:
            if self.stop_conversations is True:
                print("Stopped")
                break
            try:
                message = client.recv(1024).decode('ascii')
                if message == "8@!gwYY$oK7eTV5aRWjg":
                    print("Stop request acknowledged.")
                    self.stop_conversations = True
                if message == "ID":
                    pass
                if message != "8@!gwYY$oK7eTV5aRWjg" and message != "ID":
                    self.chat_box.data.append({"text": f"Server: {message}", "halign": "left"})
            except ValueError:
                print(ValueError)
                client.close()
                break

    def write(self):
        try:
            message = self.message_text.text
            if message.strip(" ") != "":
                self.message_text.text = ""
                client.send(message.encode('ascii'))
                self.chat_box.data.append({"text": f"You: {message}", "halign": "right"})
        except ValueError:
            print(ValueError)
            client.close()

    # def reset_status(self):
    #     self.start_chat.disabled = False
    #     self.send_btn.disabled = True
    #     self.message_text.disabled = True
    #     self.message_text.hint_text = ""
    #     self.start_chat.text = "Start Chatting"
    #     self.start_chat.background_color = (1, 1, 1, 1)
    #     self.exit_chat.background_color = (1, 1, 1, 1)

    @staticmethod
    def leave_chat():
        client.send("CRpa7Pf6@HMs^AH1z*8G".encode('ascii'))


class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    pass


class ReportWindow(Screen):
    @staticmethod
    def connect_server():
        global conn
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('127.0.0.1', 55550))
        conn.send(new_id.encode('ascii'))
    incidents = []
    regular_expression = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def email_validator(self, email):
        if re.fullmatch(self.regular_expression, email):
            return True

    def submit_form(self, name, email, incident):
        if self.email_validator(email) is True:
            if name != "" and incident != "":
                global conn
                info = [new_id, name, email, incident]
                conn.send("*In#8feAG7hJR2bm3fS".encode('ascii'))
                for i in info:
                    conn.send(i.encode('ascii'))
                    sleep(.01)
                conn.close()
                self.user_name.text = ""
                self.user_email.text = ""
                self.user_desc.text = ""
                self.feedback.text = ""
            else:
                self.feedback.text = "Please enter the remaining information."
        elif name == "" and incident == "":
            self.feedback.text = "Please enter the required information."
        else:
            self.feedback.text = "Invalid Email"
            self.user_email.text = ""

    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("gui1.kv")


class ChatApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    ChatApp().run()

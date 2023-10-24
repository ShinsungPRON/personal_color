import configparser
import socket
import json
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "controller.conf"))

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((config['DEFAULT']['server'], int(config['DEFAULT']['port'])))

soc.send(config['DEFAULT']['clientName'].encode())

while True:
    command = json.loads(soc.recv(256).decode())
    print(command)

    if command['action'] == "enable":
        if command['args'] == 'gacha':
            with open('gacha', "w") as f:
                f.write("true")

    if command['action'] == 'disable':
        if command['args'] == 'gacha':
            with open("gacha", 'w') as f:
                f.write("false")
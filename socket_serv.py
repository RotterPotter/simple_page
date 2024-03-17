import socket
import json
import datetime



SERVER_IP = '0.0.0.0'
SERVER_PORT = 3000
BYTESIZE = 1024
DECODER = 'utf-8'

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind((SERVER_IP, SERVER_PORT))

    while True:
        try:
            message, address = server_socket.recvfrom(BYTESIZE)
            message_list = message.decode(DECODER).split('&')
            data = {}
            for el in message_list:
                spl = el.split("=")
                data[spl[0]] = spl[1]
            write_json(data)
        except KeyboardInterrupt:
            server_socket.close()

def write_json(data:dict):
    data = {str(datetime.datetime.now()): data}
    data = json.dumps(data)
    with open('./storage/data.json', 'a') as file:
        file.write(data)

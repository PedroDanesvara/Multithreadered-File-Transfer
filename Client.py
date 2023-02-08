import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4505
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_DATA_PATH = 'server_data'


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd = data.split('@')[0]
        msg = data.split('@')[1]

        if cmd == 'OK':
            print(f'{msg}')
        elif cmd == '!DESCONECTAR':
            print(f'{msg}')
            break

        data = input('>>> ')
        data = data.split(' ')
        cmd = data[0]

        if cmd == 'HELP':
            client.send(cmd.encode(FORMAT))

        elif cmd == 'LOGOUT':
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == 'LIST':
            client.send(cmd.encode(FORMAT))

        elif cmd == 'UPLOAD':
            path = data[1]
            with open(f'{path}', 'r') as f:
                text = f.read()
            filename = path.split('/')[-1]
            send_data = f'{cmd}@{filename}@{text}'
            client.send(send_data.encode(FORMAT))

        elif cmd == 'DELETE':
            client.send(f'{cmd}@{data[1]}'.encode(FORMAT))

        elif cmd == 'DOWNLOAD':
            client.send(f'{cmd}@{data[1]}'.encode(FORMAT))
            data = client.recv(SIZE).decode(FORMAT).split('@')
            name = data[2]
            text = data[3]

            filepath = os.path.join('client_data', name)
            with open(filepath, 'w') as f:
                f.write(text)

    print('Desconectado do servidor.')
    client.close()


if __name__ == '__main__':
    main()

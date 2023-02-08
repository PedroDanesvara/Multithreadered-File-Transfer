import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4505
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
SERVER_DATA_PATH = 'server_data'


def handle_client(conn, addr):
    print(f'[NOVA CONEXÃO] {addr} conectado!')
    conn.send('OK@Bem vindo ao servidor de arquivos!'.encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split('@')
        cmd = data[0]

        if cmd == 'HELP':
            send_data = 'OK@'
            send_data += 'LIST: Lista todos os arquivos no servidor.\n'
            send_data += 'UPLOAD <path>: Faz o envio de um arquivo ao servidor.\n'
            send_data += 'DELETE <filename>: Deleta um arquivo do servidor.\n'
            send_data += 'LOGOUT: Desconecta do servidor.\n'
            send_data += 'DOWNLOAD: Baixa um arquivo do servidor.\n'
            send_data += 'HELP: Lista todos os comandos.'

            conn.send(send_data.encode(FORMAT))
        elif cmd == 'LOGOUT':
            break

        elif cmd == 'LIST':
            files = os.listdir(SERVER_DATA_PATH)
            send_data = 'OK@'

            if len(files) == 0:
                send_data += 'O diretório do servidor está vazio'
            else:
                send_data += '\n'.join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == 'UPLOAD':
            name = data[1]
            text = data[2]

            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, 'w') as f:
                f.write(text)

            send_data = 'OK@Arquivo enviado.'
            conn.send(send_data.encode(FORMAT))

        elif cmd == 'DELETE':
            files = os.listdir(SERVER_DATA_PATH)
            send_data = 'OK@'
            filename = data[1]

            if len(files) == 0:
                send_data += 'O diretório do servidor está vazio'
            else:
                if filename in files:
                    os.remove(f'{SERVER_DATA_PATH}/{filename}')
                    send_data += 'Arquivo deletado.'
                else:
                    send_data += 'Arquivo não encontrado.'
            conn.send(send_data.encode(FORMAT))

        elif cmd == 'DOWNLOAD':
            files = os.listdir(SERVER_DATA_PATH)
            send_data = 'OK@'
            path = data[1]

            if len(files) == 0:
                send_data += 'O diretório do servidor está vazio'
            else:
                if path in files:
                    send_data += 'Arquivo baixado.'
                    with open(f'{SERVER_DATA_PATH}/{path}', 'r') as f:
                        text = f.read()
                    filename = path.split('/')[-1]
                    send_data += f'@{filename}@{text}'
                    conn.send(send_data.encode(FORMAT))
                else:
                    send_data += 'Arquivo não encontrado.'
            conn.send(send_data.encode(FORMAT))
    print(f'[DESCONECTADO] {addr} desconectado.')


def main():
    print('[INICIANDO] O servidor está iniciando...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print('[ESCUTANDO] O servidor está escutando...')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    main()

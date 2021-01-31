import socket
import threading
from websocket import create_connection


client = ws.create_connection("ws://runclient:8080/ws")
nickname = input("Choose your nickname: ")
cid = client.send(f'/nickname {nickname}')


def receive():
    while True:
        try:
            message = client.recv()
            if message == 'NICKNAME':
                client.send(nickname)
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    # Для отправки сообщения:
    # 1. отдельные пользователи - указываем ники (@user1,@user2 сообщение)
    # 2. Все пользователя - сообщение
    # Команды:
    # /userlist - список участников чата

    while True:
        message = '{}'.format(input(''))
        client.send(message)


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

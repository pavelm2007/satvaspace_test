import re
import time
import base64
import datetime

from autobahn.twisted import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor


class CommandAction:
    # Класс обработки команд чата
    re_command = re.compile(r'^\/userlist|\/nickname')

    def __init__(self, *args, **kwargs):
        self.username = None

    def setUserName(self, username):
        self.username = username
        self.factory.register_username(self, username)

    def fetchCommand(self, payload):
        result = self.re_command.match(payload)
        return result.group() if result else None

    def is_command(self, payload):
        return bool(self.fetchCommand(payload))

    def getCommandParams(self, payload):
        result = self.re_command.sub('', payload).strip()
        return result

    def execCommand(self, action, params):
        if action == '/nickname':
            self.username = params
            self.factory.register_username(self, username=params)
        elif action == '/userlist':
            self.factory.sendUserList(self)

    def execute_command_action(self, data):
        cmd = self.fetchCommand(data)
        params = self.getCommandParams(data)
        self.execCommand(action=cmd, params=params)


class UserAction:
    # Класс обработки сообщений пользователя
    re_users = re.compile(r'^\@\w+(?=(,?))(?:\1\@\w+)+|^\@\w+')

    def getUserMsg(self, payload):
        result = self.re_users.sub('', payload).strip()
        return result

    def fetchUsers(self, payload):
        # Получаем список пользователей для кого предназзначено сообщение, 
        # если пользователей нет, то всем участникам чата
        result = None
        users = self.re_users.match(payload)

        if users:
            result = list(
                map(
                    lambda x: x[1:].strip(), users.group().split(',')
                )
            )

        return result

    def execute_user_action(self, data):
        users = self.fetchUsers(data)
        message = self.getUserMsg(data)
        self.factory.sendMessage(sender=self, usernames=users, msg=message)


class ChatServerProtocol(CommandAction, UserAction, WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onClose(self, wasClean, code, reason):
        self.factory.unregister_username(self.username)
        self.factory.unregister(self)
        WebSocketServerProtocol.onClose(self, wasClean, code, reason)

    def onMessage(self, payload, isBinary):
        data = payload.decode()

        if self.is_command(data):
            self.execute_command_action(data)
        else:
            self.execute_user_action(data)


class ChatServerFactory(WebSocketServerFactory):

    def __init__(self, uri):
        WebSocketServerFactory.__init__(self, uri)
        self.clients = []
        self.users = {}
        self.sendTimeLoop()

    def sendTimeLoop(self):
        # Каждые 10 сек. отсылаем текущее время в чат
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self.sendMessage(sender=None, usernames=None, msg=now)
        reactor.callLater(10, self.sendTimeLoop)

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def register_user(self, username: str, client):
        self.users[username] = client

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def register_username(self, client, username):
        self.users[username] = client

    def unregister_username(self, username):
        self.users.pop(username, None)

    def sendUserList(self, client):
        msg = ','.join(self.users.keys())
        client.sendMessage(msg.encode('utf8'))

    def getClientsByUserNames(self, sender, usernames):
        # Получаем список клиентов, которым необзодимо отправить сообщение. 
        # Отправителя сообщения исключем из списка рассылки.
        clients = self.clients.copy()

        if usernames:
            user_keys = set(usernames).intersection(self.users.keys())
            clients = list(
                map(
                    lambda k: self.users[k],
                    user_keys
                )
            )
        
        if sender:
            clients.remove(sender)

        return clients

    def sendMessage(self, sender, usernames, msg):
        clients = self.getClientsByUserNames(sender, usernames=usernames)

        for c in clients:
            c.sendMessage(msg.encode('utf8'))

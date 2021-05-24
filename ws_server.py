import time

import slixmpp
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler


host = 'matrix.evarun.ru'
password = '123456'


class SendMsgBot(slixmpp.ClientXMPP):
    send_message_to = f'hyyudu2@{host}'

    def __init__(self, login, password):
        jid_name = f'{login}@{host}'
        super().__init__(jid_name, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.send_message_to, mbody='Im alive!')

    def send_to_server(self, message: str) -> None:
        self.send_message(mto=self.send_message_to, mbody=message)

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            time.sleep(0.1)
            print(f'Received from Jabber: {msg["body"]}')
            msg.reply("Thanks for sending:\n%s" % msg['body']).send()


class JabberWebSocketHandler(WebSocketHandler):
    bot: SendMsgBot = None

    def connect_to_jabber(self, login, password) -> None:
        bot = SendMsgBot(login, password)
        bot.register_plugin('xep_0030')  # Service Discovery
        bot.register_plugin('xep_0199')  # XMPP Ping
        bot.connect()
        bot.process(forever=True)
        self.bot = bot

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(f'Recvd: {message}')
        result = self.process_message(message)
        self.write_message(result)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

    def process_message(self, message) -> str:
        if message.startswith('login '):
            return self.cmd_login(message)
        else:
            self.cmd_command(message)

    def cmd_login(self, message) -> str:
        if self.bot and self.bot.authenticated:
            return 'Вы уже залогинены'
        else:
            _, login, password, *_ = message.split(' ')
            self.connect_to_jabber(login, password)
            return 'Подключение успешно'

    def cmd_command(self, message):
        self.bot.send_to_server(message)


if __name__ == '__main__':
    app = Application([
        (r"/websocket", JabberWebSocketHandler),
    ])
    app.listen(8900)
    IOLoop.current().start()

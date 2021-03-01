import asyncio
import time

import slixmpp


host = 'matrix.evarun.ru'
jid_name = f'hyyudu@{host}'
jid_name2 = f'hyyudu2@{host}'
password = '123456'


class SendMsgBot(slixmpp.ClientXMPP):

    def __init__(self, jid_name, password):
        super().__init__(jid_name, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        bot.send_message(mto=jid_name2, mbody='Блабла>')
        print('send 1')
        await asyncio.sleep(5)
        bot.send_message(mto=jid_name2, mbody='Блабла 2')
        print('send 2')
        await asyncio.sleep(5)
        bot.send_message(mto=jid_name2, mbody='Блабла 3')
        print('send 3')


    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            time.sleep(0.1)
            print(msg)
            print(msg['body'])
            msg.reply("Thanks for sending:\n%s" % msg['body']).send()


# by_xmpp()
bot = SendMsgBot(jid_name, password)
bot.register_plugin('xep_0030')  # Service Discovery
bot.register_plugin('xep_0199')  # XMPP Ping
bot.connect()
bot.process(forever=False)


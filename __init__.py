
#!/usr/bin/env python

'''Using Webhook and self-signed certificate'''

# This file is an annotated example of a webhook based bot for
# telegram. It does not do anything useful, other than provide a quick
# template for whipping up a testbot. Basically, fill in the CONFIG
# section and run it.
# Dependencies (use pip to install them):
# - python-telegram-bot: https://github.com/leandrotoledo/python-telegram-bot
# - Flask              : http://flask.pocoo.org/
# Self-signed SSL certificate (make sure 'Common Name' matches your FQDN):
# $ openssl req -new -x509 -nodes -newkey rsa:1024 -keyout server.key -out server.crt -days 3650
# You can test SSL handshake running this script and trying to connect using wget:
# $ wget -O /dev/null https://$HOST:$PORT/

from flask import Flask, request
from twx.botapi import TelegramBot, ReplyKeyboardMarkup


# CONFIG
TOKEN    = open("/home/aleksart/telegramBot/token").readline()
HOST     = 'aleksart.me' # Same FQDN used when generating SSL Cert
PORT     = 443
CERT     = '/home/aleksart/openssl/sert.pem'
CERT_KEY = '/home/aleksart/openssl/sert.key'

print(TOKEN)
print('test')
bot = TelegramBot(TOKEN)
app = Flask(__name__)
context = (CERT, CERT_KEY)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/'+TOKEN, methods=['POST'])
def webhook():
    message = json.loads(request.data)
    if message['message']['text'] == '/ping':
        bot.send_message(message['message']['chat']['id'], 'Pong!').wait()
    return 'ok'


def setWebhook():
    webhook_url = 'https://%s:%s/%s' % (HOST, PORT, TOKEN)
    print(webhook_url)
    bot.set_webhook(url=webhook_url,
                   certificate=open(CERT, 'rb'))
    bot.update_bot_info().wait()
    print(bot)

if __name__ == '__main__':
    # setWebhook()

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)
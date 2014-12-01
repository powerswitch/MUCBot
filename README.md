MUC Transport Bot
=================
XMPP Bot to connect users to Multi User Chat whose client doesn't support it.


#### Usage on server side

edit the `config.ini` to your convenience and then run
```
$ python2.7 muc.py
```
You need to create a separate XMPP account for the bot.

#### Usage on client side
Send messages to the bot to send them to the MUC.
You'll receive every MUC message as a private message from the bot.

#### Dependencies:
* xmpppy
* configobj

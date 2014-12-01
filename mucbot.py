#!/usr/bin/python2
# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xmpp
import time,os
from configobj import ConfigObj
from xml.sax.saxutils import escape

def messageCB(session,message):
    """
    handle messages
    """
    if not message.getBody():
        return # abort on empty message
    
    frm = message.getFrom()
    if frm.getNode()+"@"+frm.getDomain() == chatroom:
        # Message from chatroom
        msg = xmpp.Message(
            to=tojid,
            body=escape(frm.getResource()+": "+message.getBody()),
            typ="chat",
            frm=username
        )
        client.send(msg)
    else:
        msg = xmpp.Message(
            to=chatroom,
            body=escape(message.getBody()),
            typ="groupchat",
            frm=username
        )
        client.send(msg)

# load config
conf = ConfigObj("config.ini")

credentials = conf["credentials"]
username    = credentials["username"]
password    = credentials["password"]
chat        = conf["chat"]
nickname    = chat["nickname"]
chatroom    = chat["chatroom"]
botjid      = conf["bot"]
tojid       = botjid["tojid"]

# Create XMPP client and connect
client = xmpp.Client(xmpp.JID(username).getDomain())
connection = client.connect()

if not connection:
    print("Unable to connect to server {}, aborting!".format(server))
    sys.exit(1)

if connection != "tls":
    print("Warning: unable to estabilish secure connection - TLS failed!")
    
auth = client.auth(xmpp.JID(username).getNode(), password)
if not auth:
    print("Unable to authorize on {} - check login/password. Aborting!".format(server))
    sys.exit(1)

if auth != 'sasl':
    print("Warning: unable to perform SASL auth os {}. Old authentication method used!".format(server))

# register message handler
client.RegisterHandler('message',messageCB)
#client.RegisterHandler('presence',presenceCB)
    
# init
client.sendInitPresence()

# connect to muc
muc = xmpp.Presence(to='{}/{}'.format(chatroom,nickname))
muc.setTag('x', namespace=xmpp.NS_MUC).setTagData('password','')
muc.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
client.send(muc)

print("Bot started.")
while 1:
    client.Process(1)

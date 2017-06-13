import json
import os

import telepot
import time
from telepot.loop import MessageLoop

def save_status(obj):
    with open('groups.json', 'w') as f:
        f.write(json.dumps(obj))

def save_allowed(list):
    with open('allowed.json', 'w') as f:
        f.write(json.dumps(list))

if not os.path.isfile('groups.json'):
    save_status({})

if not os.path.isfile('allowed.json'):
    save_allowed([])

chats = None
allowed = None

with open('groups.json', 'r') as f:
    chats = json.load(f)

with open('allowed', 'r') as f:
    allowed = json.load(f)


def handle(msg):
    if msg['from']['id'] in allowed:
        content_type, chat_type, chat_id = telepot.glance(msg)
        txt = ""
        if 'text' in msg:
            txt = txt + msg['text']
        elif 'caption' in msg:
            txt = txt + msg['caption']
        if txt != "":
            if "/add" == txt[:4]:
                txt_split = txt.strip().split(" ")
                if len(txt_split) == 2 and "#" == txt_split[1][0]:
                    tag = txt_split[1].lower()
                    name = ""
                    if msg['chat']['type'] == "private":
                        name = name + "Chat personal con " + msg['chat']['first_name'] + ((" " + msg['chat']['last_name']) if 'last_name' in msg['chat'] else "")
                    else:
                        name = msg['chat']['title']
                    chats[tag] = {'id': chat_id, 'name': name}
                    bot.sendMessage(chat_id, name + " agregado con el tag " + tag)
                    save_status(chats)
                else:
                    bot.sendMessage(chat_id, "Formato incorrecto. Debería ser _/add #{tag}_", parse_mode="Markdown")
            elif "/rm" == txt[:3]:
                txt_split = txt.strip().split(" ")
                if len(txt_split) == 2 and "#" == txt_split[1][0]:
                    tag = txt_split[1].lower()
                    if tag in chats:
                        if chats[tag]['id'] == chat_id:
                            del chats[tag]
                            bot.sendMessage(chat_id, "Tag "+tag+" borrado de la lista.")
                            save_status(chats)
                            return
                        else:
                            bot.sendMessage(chat_id, "No puedes eliminar el tag de un chat desde un chat distinto al que lo posee.")
                    else:
                        bot.sendMessage(chat_id, "Tag no existe en la lista")
                else:
                    bot.sendMessage(chat_id, "Formato incorrecto. Debería ser _/rm #{tag}_", parse_mode="Markdown")

            elif "/taglist" ==  txt.strip()[:8]:
                tags_names = []
                for tag, chat in chats.items():
                    tags_names.append( (tag, chat['name']))
                response = "<b>lista de Tags</b>"
                for (tag, name) in sorted(tags_names):
                    response = response + "\n<b>" + tag + "</b>: <i>" + name + "</i>"
                bot.sendMessage(chat_id, response, parse_mode="HTML")
            elif "/myid" == txt.strip()[:5]:
                bot.sendMessage(chat_id, "ID recogido a "+msg['from']['first_name']+"!")
                print(msg['from']['first_name'] + " " + (msg['from']['last_name'] if 'last_name' in msg['from'] else "") + ": " +str(msg['from']['id']))
            elif "#" == txt[0]:
                txt_split =txt.strip().split(" ")
                i = 0;
                tags = []
                while i < len(txt_split) and txt_split[i][0] == "#":
                    tags.append(txt_split[i].lower())
                    i+=1
                if i != len(txt_split) or 'reply_to_message' in msg:
                    approved = []
                    for tag in tags:
                        if tag in chats:
                            if chats[tag]['id'] != chat_id:
                                approved.append(chats[tag]['name'])
                                bot.forwardMessage(chats[tag]['id'], chat_id, msg['message_id'])
                                if 'reply_to_message' in msg:
                                    bot.forwardMessage(chats[tag]['id'], chat_id, msg['reply_to_message']['message_id'])
                    if len(approved) > 0:
                        bot.sendMessage(chat_id, "Texto enviado a <i>" + ", ".join(approved) + "</i>", parse_mode="HTML")
                    else:
                        bot.sendMessage(chat_id, "No se pudo enviar mensaje a ningún chat")
                else:
                    bot.sendMessage(chat_id, "No puedo enviar un mensaje solo con tags")

bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
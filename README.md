# telegram-forward-bot
Simple Telegram Bot for forwarding messages easily between various related channels and groups.

This bot allows you to automatically forward messages between different channels. We use it on our Student Comitee because we have like 15 different Telegram groups for each commission we are working on. Then, if we want some commission receives some important information, we can automatically forward to them using _hashtags_ at the beggining of the message (or the caption of a media file).

Made with latest version of telepot at the time (12.0) and for Python 3.5.2. And shared with a MIT license.

## How to install

We will assume you and your friends have Telegram accounts and several telegram chats.

First, you need to create a Telegram bot. Talk with the [BotFather](https://t.me/botfather) and ask it for a bot (and its respective token)

Then, you need to rename the file config-sample.json to config.json. Add in `token` property your bot's token.

Also, its very encouraged to set a password for registering to use the bot. If you don't set a password. Any person could use it and forward messages between your channels.

The next part is to install in your server the requirements of the bot using `pip3 install -r requirements.txt`.

finally, configure the bot, adding it on all the groups you want to connect

## How to use

1. You need to add yourself to the authorized list of the bot typing `/addme {password}`, where the password is the string set on bot configuration (see previous section for more details).
1. If you want to delete your permissions from the bot, you can type `/rmme`. Then you won't be able to send commands to te bot (except for `/addme`)
1. You can use `/taglist` for a list of tags registered to the bot, and the group/channel/private chat's names
1. You cand add a tag to a group using `/add #{tag}`. You can remove the tag using `/rm #{tag}`.
1. If you want to send a message/file/image/other to another group, you should add the tags **at the start** of the message or caption. you can add more than one tag if you want to.
1. You can forward a message by replying to it with the desired tags. Both messages will be forwarded.

## Some considerations

Some details about the implementation:

1. you can't forward a message to the same chat you wrote it. The bot will warn you and reject to do that if you try to do it.
1. Each chat can have more than 1 tag. That's very useful if you have various names for your chats, but if you write several times the same tag, or tags that point to the same group, you will have several forwardings to that chat. I plan to correct this some day. (It's not hard but I'm very busy right now).
1. Any person registered as authorized with the bot can add tags for the chat or another chats. The use of this bot assumes you have authorized users in your chats that you trust. Also, any person registered to the bot can forward messages to any group using the tags.




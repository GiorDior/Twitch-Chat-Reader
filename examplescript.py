# author: Giorgio
# date: 09.05.2024
# topic: Twitch-Chat-Reader
# version: 1.1
# repo: https://github.com/Giooorgiooo/Twitch-Chat-Reader


from twitchchatreader import TwitchChatReader
from twitchchatreaderevents import CommentEvent, ConnectEvent

reader: TwitchChatReader = TwitchChatReader("jynxzi")


# executes when a connection is established
@reader.on("connect")
def on_connect(event: ConnectEvent):
    print("Connection established!")

# executes when a comment is received
@reader.on("comment")
def on_connect(event: CommentEvent):
    print(event.user.name, "|", event.comment)
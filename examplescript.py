from chatreader import TwitchChatReader
from chatreaderevents import CommentEvent, ConnectEvent

reader = TwitchChatReader("kyootbot")

@reader.on("connect")
def on_connect(event: ConnectEvent):
    print("Connection established!")

@reader.on("comment")
def on_connect(event: CommentEvent):
    # print(f"{event.user} -> {event.comment}")
    print(event.user.name, "|", event.comment)
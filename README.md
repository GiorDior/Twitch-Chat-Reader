# Twtich Chat Reader

This is a simple Python program that extracts and reads messages (only latin chars) from a twitch chat.

I thank all people who use this for their project. I love to contribute to the community. However, please credit me by using the GitHub project link.

## Usage

To use this, you need Python 3.6+, the [**Chrome browser**](https://www.google.com/intl/en_en/chrome/) and all of the required packages installed.
To install the required packages, run: 
<br>`pip3 install selenium requests bs4` or `pip3 install -r requirements.txt`

### Importing the script
1. Place `twitchchatreader.py` iand `twitchchatreaderevents.py` nto your directory
2. Import the `TwitchChatReader` class like this: `from twitchchatreader import TwitchChatReader`

## Events
This script is based on events. This means that whenever an event is called, a function is executed. You have to define this function yourself at first. Here is an example:
```
@reader.on("comment")
def on_comment(event: CommentEvent):
    print(event.user.name, "|", event.comment)
```
Here is an [example script](https://github.com/GiorDior/Twitch-Chat-Reader/blob/main/examplescript.py).
<br>
Always make sure that:
1. the decorator `@reader.on(event_name)` is added before the definition of the function 
2. you have an event parameter in your function

event_name | description | attributes
--- | --- | ---
`"connect"`| Called when the browser connects to the Twitch chat. | none
`"comment"`| Called when a new comment is written in Twitch chat. | event.comment, event.user.name

# Twtich Chat Reader

This is a simple Python program that extracts, reads and saves messages from a twitch chat.

I thank all people who use this for their project. I love to contribute to the community. However, please credit me by using the GitHub project link.

## Usage

To use this, you need Python 3.7+, the [**Chrome browser**](https://www.google.com/intl/en_en/chrome/) and all of the required packages installed.
To install the required packages, run: 
<br>`pip3 install selenium` or `pip3 install requirements.txt`

### Importing the script
1. Place `tchatreader.py` into your directory
2. Import the `TwitchChatReader` class like this: `from tchatreader import TwitchChatReader`

### Printing messages to the console
1. Import the script following the steps above
2. Creating a new instance of the class `TwitchChatReader`: `reader = TwitchChatReader(CHANNELNAME)
3. To print messages, call the `print(find_new_messages())`

I provided an [example script](https://github.com/GiorDior/Twitch-Chat-Reader/blob/main/examplescript.py).
Note: `find_new_messages()` returns a list of all new messages in this format: `[AUTHOR, MESSAGE]`.
If there is no new message, only an empty list is returned.

### Saving messages to a txt file
1. Import the script following the steps above
2. Creating a new instance of the class `TwitchChatReader`: `reader = TwitchChatReader(CHANNELNAME)
3. Call `find_new_messages()` method to update the list of messages.
4. Call `save_messages()` to save all messages that were found by the previous method.
<br> I provided examples of log files at [/logsamples/](https://github.com/GiorDior/Twitch-Chat-Reader/tree/main/logsamples).

### Note
- Messages that cannot be decrypted by Python (unknown characters) are not stored anywhere in any way.
- Messages that might have shown up but have been removed by the Twitch chat system (because they were too old) will not come up when `find_new_messages()` is called

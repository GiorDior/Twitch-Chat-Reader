from tchatreader import TwitchChatReader
import time

# creating a new obejct
reader = TwitchChatReader("Chess")

# waiting 10 seconds for some messages to come 
time.sleep(10)

# finding all new messages that appeared
reader.find_new_messages()

# saving messages to a specified directory
reader.save_messages("logsamples/")

# author: GiorDior aka Giorgio
# date: 12.06.2023
# topic: Twitch-Chat-Reader
# version: 1.0

import codecs
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TwitchChatReader:
    def __init__(self, twitch_channel: str) -> None:
        """
        Initializes an instance of TwitchChatReader.

        Args:
            twitch_channel (str): The name of the Twitch channel to read the chat from.
        """
        now = datetime.now()
        self._date_and_time = now.strftime("%d-%m-%Y_%H-%M-%S")

        # list that stores all messages as WebElements
        self.messages = []

        self.twitch_channel = twitch_channel

        # starting up chrome to connect to the twitch chat
        self.connect_to_chat()

    def _can_encode(self, string: str) -> bool:
        """
        Checks if a string can be encoded using the 'charmap' encoding.

        Args:
            string (str): The string to check.

        Returns:
            bool: True if the string can be encoded, False otherwise.
        """
        try:
            codecs.encode(string, 'charmap')
            return True
        except UnicodeEncodeError:
            return False
    
    def connect_to_chat(self):
        """
        Connects to the Twitch chat for the specified channel using Selenium web driver.
        """
        # Set up the Selenium web driver (ensure you have the appropriate driver for your browser)
        self._driver = webdriver.Chrome()

        # Navigate to the Twitch chat URL
        self._driver.get(f"https://www.twitch.tv/{self.twitch_channel}/chat")
        
        # Wait until the website startup
        wait = WebDriverWait(self._driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        print(f"Connection established to {self.twitch_channel}'s chat!")

    def find_new_messages(self) -> list:
        """
        Finds new chat messages that appeared since the last time this method was called.

        Returns:
            list: A list of new messages in the format [author, messagecontent].
        """
        new_messages = []

        # Find elements of chat messages
        chat_messages = self._driver.find_elements(By.CSS_SELECTOR, '.chat-line__message')

        # Check if messages are new messages
        for message in chat_messages:
            if message not in self.messages and message.text != "" and self._can_encode(message.text):
                self.messages.append(message)
                new_messages.append([self.get_author(message_element=message), self.get_message_content(message_element=message)])
        return new_messages
    
    def get_author(self, message_element) -> str:
        """
        Extracts the author from a message element.

        Args:
            message_element: The message element.

        Returns:
            str: The author of the message.
        """
        if ("\n" in message_element.text):
            irregular_text = message_element.text.replace("\n", "\\n")
            parts = irregular_text.split("\\n")
            new_text = ""
            for i, part in enumerate(parts):
                if i != 0:
                    new_text += part
            author = new_text.split(": ")[0]
        else:
            author = message_element.text.split(": ")[0]
        return author

    def get_message_content(self, message_element) -> str:
        """
        Extracts the content of a message element.

        Args:
            message_element: The message element.

        Returns:
            str: The content of the message.
        """
        message_text = message_element.text

        if ("\n" in message_element.text):
            irregular_text = message_element.text.replace("\n", "\\n")
            parts = irregular_text.split("\\n")
            new_text = ""
            for i, part in enumerate(parts):
                if i != 0:
                    new_text += part
            message_text = new_text

        parts = message_text.split(": ")

        content = ""
        for i, part in enumerate(parts):
            if not i == 0:
                content += part

        return content

    def save_messages(self, directory: str = ""):
        """
        Saves all messages from self.messages to a text file.

        Args:
            directory (str, optional): The directory to save the chat log file. Defaults to the current directory (DIRECTORY/).
        """
        file = open(f"{directory}chatlog_{self.twitch_channel}_{self._date_and_time}.txt", "w")
        for message in self.messages:
            try:
                file.write(message.text + "\n")
            except:
                pass
        file.close()

        print(f"Log successfully saved to {directory}")

# author: Giorgio
# date: 09.05.2024
# topic: Twitch-Chat-Reader
# version: 1.1
# repo: https://github.com/Giooorgiooo/Twitch-Chat-Reader

import codecs
from selenium.webdriver.remote.webelement import WebElement

class ConnectEvent:
    def __init__(self) -> None:
        pass

class CommentEvent:
    def __init__(self, message: WebElement, func) -> None:
        """
        Create a new CommentEvent object.

        Args:
            message (WebElement): The message element.
            func: the function that is called due to the event.
        """
        from twitchchatreader import User

        self.user = User(self._get_user(message))
        self.comment = self._get_comment(message)

        if not self.user.name == "" and not self.comment == "" and self._can_encode(self.user.name) and self._can_encode(self.comment):
            func(self)
    
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
        
    def _get_user(self, message: WebElement) -> str:
        """
        Extracts the author from a message element.

        Args:
            message_element: The message element.

        Returns:
            str: The author of the message.
        """
        if ("\n" in message.text):
            irregular_text = message.text.replace("\n", "\\n")
            parts = irregular_text.split("\\n")
            new_text = "".join(parts[1:])
            user = new_text.split(": ")[0]
        else:
            user = message.text.split(": ")[0]
        return user

    def _get_comment(self, message: WebElement) -> str:
        """
        Extracts the content of a message element.

        Args:
            message_element: The message element.

        Returns:
            str: The content of the message.
        """
        message_text = message.text

        if ("\n" in message.text):
            irregular_text = message.text.replace("\n", "\\n")
            parts = irregular_text.split("\\n")
            message_text = "".join(parts[1:])

        parts = message_text.split(": ")

        content = "".join(parts[1:])

        return content

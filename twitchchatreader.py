import requests
import threading
import codecs
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from chatreaderevents import *

class User:
    def __init__(self, name: str) -> None:
        self.name = name

class TwitchChatReader:
    def __init__(self, twitch_channel: str) -> None:
        """
        Initializes an instance of TwitchChatReader.

        Args:
            twitch_channel (str): The name of the Twitch channel to read the chat from.
        """
        self.twitch_channel = twitch_channel
        
        if not self._user_exists(self.twitch_channel):
            print(f"Error: The Twitch user '{self.twitch_channel}' does not exist") 
            exit()

        self.previous_message = None
        self._connected = False
        self._connect_to_chat()

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
        
    def _connect_to_chat(self) -> None:
        """
        Connects to the Twitch chat for the specified channel using Selenium web driver.
        """
        self._driver = Chrome()
        self._driver.get(f"https://www.twitch.tv/{self.twitch_channel}/chat")

        wait = WebDriverWait(self._driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self._connected = True

        # delete irrelevant content from the page
        irrelevant_content = [".consent-banner", ".chat-input__textarea", ".chat-input__buttons-container"]
        for content in irrelevant_content:
            element = self._driver.find_element(By.CSS_SELECTOR, content)
            self._driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)

        # self._driver.execute_script("document.body.style.zoom='25%'")

    def _user_exists(self, user: str) -> bool:
        """
        Checks if a Twitch user exists.

        Args:
            user (str): The Twitch username.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        exists = False
        url = f"https://www.twitch.tv/{user}"
        for i in range(10):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if user.lower() in soup.prettify().lower():
                exists = True
        return exists

    def _find_new_message(self) -> list[WebElement]:
        """
        Finds new chat messages that appeared since the last time this method was called.

        Returns:
            list: A list of new messages in the format [user, messagecontent].
        """
        new_messages = []
        chat_messages = self._driver.find_elements(By.CSS_SELECTOR, '.chat-line__message')

        if len(chat_messages) > 0:
            def get_message_number(message):
                return int(str(message).split("_")[-1].split('"')[0])

            for message in chat_messages:
                try:
                    # checking if the message is new and valid (only latin)
                    if self.previous_message is None or get_message_number(message) > get_message_number(self.previous_message)\
                        and not message.text == "" and self._can_encode(message.text):
                        # adding the new message
                        new_messages.append(message)
                        self.previous_message = message
                except StaleElementReferenceException:
                    chat_messages = self._driver.find_elements(By.CSS_SELECTOR, '.chat-line__message')

        return new_messages

    def _comment_event_loop(self, func) -> None:
        """
        Event loop for processing new comments.

        Args:
            func (function): The function to be executed for each new comment.
        """
        while True:
            new_messages = self._find_new_message()
            for message in new_messages:
                try:
                    CommentEvent(message, func)
                except StaleElementReferenceException:
                    pass

    def _connect_event_loop(self, func) -> None:
        """
        Event loop for processing new comments.

        Args:
            func (function): The function to be executed for each new comment.
        """
        while True:
            if self._connected:
                func(ConnectEvent)
                return

    def on(self, event_name: str):
        """
        Decorator for registering event handlers.

        Args:
            event_name (str): The name of the event to register the handler for.

        Returns:
            function: The decorator function.
        """
        def wrapper(func):
            if event_name == "comment":
                threading.Thread(target=self._comment_event_loop, args=(func,)).start()
            if event_name == "connect":
                threading.Thread(target=self._connect_event_loop, args=(func,)).start()
            return func

        return wrapper

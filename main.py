# -*- coding:utf-8 -*-

"""

Author: Joel Ermantraut
File: main.py
Desc: Main file of project.

"""

"""

Site Structure:

_3Pwfx: Chat selector class 
    _22mTQ: Image
    _1C6Zl: Name and last message
        _1c_mC:
            _3Tw1q:
                _3es8f:
                    span: name 

_2AuNk:
    _3SvgF:
        DuUXI:
            _1awRl copyable-text selectable-text: Input

_1yHR2:
    Barcode

"""


from automation_scripts.web_scrapping import WebScrapper
from automation_scripts.mouse_control import MouseControl
import time

class WhatsMatic(object):
    """App to control WhatsApp and automate it."""
    def __init__(self):
        self.list_of_chats_element = "._3soxC"
        self.chat_button_element = "._3Pwfx"
        self.chat_element = "._3Pwfx ._1C6Zl ._3es8f span"
        self.input_element = "._2AuNk ._1awRl"
        self.barcode_element = "._1yHR2"
        self.init() 

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            "/home/joel/Apps/chromedriver",
            "https://web.whatsapp.com"
        )

        self.mouse = MouseControl()

        self.wait_for_scan()

        time.sleep(2)

    def wait_for_scan(self):
        """
        When WhatsApp is open, the barcode is shown.
        This functions waits after it is scanned.
        """
        while self.driver.get_elements(self.barcode_element):
            time.sleep(1)

    def is_element(self, attribute, value, elements):
        """
        Searches an element with the given properties.
        """
        for element in elements:
            chat_properties = self.driver.get_all_properties(element)[0]

            if value in chat_properties.values():
                return element

        return None

    def search_chat(self, name):
        """
        Search for a chat with the name given and returns the element.

        Elements cannot be accessed if they are not loaded. Though, the
        script will scroll up to last element be the same as the last scrolled
        last element.
        """
        self.mouse.mouse_move((30, 400))
        # Moves mouse to list of chats to scroll

        list_of_chats = self.driver.get_elements(self.list_of_chats_element)[0]
        an_element = self.driver.get_elements(self.chat_button_element)[0]
        iters = list_of_chats.size['height'] // (an_element.size['height'] * 6) 

        for i in range(iters):
            elements = self.driver.get_elements(self.chat_element)
            element = self.is_element('title', name, elements)
            if element:
                return element

            self.mouse.scroll(1, True) # 1% of height
            time.sleep(1)

        return None

    def close(self):
        """
        Closes driver.
        """
        self.driver.quit()

def main():
    whatsmatic = WhatsMatic()

    print(whatsmatic.search_chat('Danilo Coletto'))

if __name__ == "__main__":
    main()

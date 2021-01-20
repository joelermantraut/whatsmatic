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

"""

BUGS:

1) No reconoce los grupos.
3) Habria que modificar las librerias y reescribir segun corresponda.

"""

from automation_scripts.web_scrapping import WebScrapper
from automation_scripts.mouse_control import MouseControl
from automation_scripts.files_use import FileUse
from time import sleep
import argparse

class WhatsMatic(object):
    """App to control WhatsApp and automate it."""
    def __init__(self, files_path=""):
        self.side_element = "._2ruyW"
        self.list_of_chats_element = "._3soxC"
        self.header_element = "._2O84H"
        self.search_bar_element = "._1Ra05"
        self.chat_button_element = "._3Pwfx"
        self.chat_element = "._3Pwfx ._1C6Zl ._3es8f span"
        self.input_element = "._2AuNk ._1awRl"
        self.barcode_element = "._1yHR2"
        self.notification_message_element = "._3Aa1y"
        self.chat_per_page = 5
        self.files_path = files_path
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

        self.files = FileUse()

        self.wait_for_scan()
        self.wait_for_notification_message()

        sleep(2)

    def wait_for_scan(self):
        """
        When WhatsApp is open, the barcode is shown.
        This functions waits after it is scanned.
        """
        while self.driver.get_elements(self.barcode_element):
            sleep(1)

    def wait_for_notification_message(self):
        """
        After a while, WhastApp generates a notification message
        over the chat box that produce problem with elements
        attachment.
        """
        while not self.driver.get_elements(self.notification_message_element):
            sleep(1)

        self.driver.scripting("return document.\
                getElementsByClassName('{}')[0].remove();".format(self.notification_message_element[1:]))
        # And removes it

    def is_element(self, attribute, value, elements):
        """
        Searches an element with the given properties.
        """
        for element in elements:
            chat_properties = self.driver.get_all_properties(element)[0]

            if value in chat_properties.values():
                return element

        return None

    def get_number_of_chats(self):
        """
        Gets the number of times that it must do scroll to
        see all contacts of chat list.
        """

        side = self.driver.get_elements(self.side_element)[0]
        header = self.driver.get_elements(self.header_element)[0]
        search_bar = self.driver.get_elements(self.search_bar_element)[0]
        list_of_chats = self.driver.get_elements(self.list_of_chats_element)[0]

        side_size = side.size['height']
        header_size = header.size['height']
        search_bar_size = search_bar.size['height']
        list_of_chats_size = list_of_chats.size['height']

        list_of_chat_show_height = side_size - header_size - search_bar_size

        iters = list_of_chats_size // list_of_chat_show_height + 1
        # Plus one because the division will trunk the value

        return list_of_chat_show_height, iters

    def get_contacts(self):
        """
        Gets the list of chat contacts.

        Take care that this function don't take care of contacts
        registered that where not writted.
        """
        contacts = []

        self.mouse.mouse_move((30, 450))
        # Moves mouse to list of chats to scroll

        side_height, iters = self.get_number_of_chats()

        for i in range(iters):
            elements = self.driver.get_elements(self.chat_element)
            for element in elements:
                title = self.driver.get_all_properties(element)[0]['title']
                print(title)

                if title not in contacts:
                    contacts.append(title)

            self.mouse.scroll(side_height) # 1% of height
            sleep(1)
            # Scrolling in Selenium is not working as it must.
            # So, it preferable to use another tool.

        return contacts

    def get_groups(self):
        """
        Returns a list of created groups.
        """
        self.files.list_all(self.files_path)

        return self.files.list_files(r'.*.wmg')

    def search_chat(self, name):
        """
        Search for a chat with the name given and returns the element.

        Elements cannot be accessed if they are not loaded. Though, the
        script will scroll up to last element be the same as the last scrolled
        last element.
        """
        self.mouse.mouse_move((30, 400))
        # Moves mouse to list of chats to scroll

        iters = self.get_number_of_chats()

        for i in range(iters):
            elements = self.driver.get_elements(self.chat_element)
            element = self.is_element('title', name, elements)
            if element:
                return element

            self.mouse.scroll(1, True) # 1% of height
            sleep(1)
            # Scrolling in Selenium is not working as it must.
            # So, it preferable to use another tool.

        return None

    def select_chat(self, chat_element):
        """
        Clicks on the chat element to select it.
        """
        self.driver.click_elements(chat_element)

    def write_on_chat(self, content):
        """
        Writes on a selected chat.
        """
        footer = self.driver.get_elements("footer")
        text_input = self.driver.get_elements("._1awRl", footer)

        self.driver.send_keys(text_input, [content])
        sleep(5)
        self.driver.send_keys(text_input, ["enter"])

    def send_to_group(self, group, message):
        """
        Receives a list of contacts, named as groups, and a message.
        Sends it to each member of the group.
        """
        for member in group:
            self.send_message(member, message)

    def send_message(self, contact, message):
        """
        Sends a message to a particular contact.
        """
        chat = self.search_chat(contact)
        self.select_chat(chat)

        self.write_on_chat(message)

    def create_a_group(self, name, contacts_list, contacts_index):
        """
        Receives a name, a contact list, and another list that indicates
        which of the contacts of contact list will be included in the group.

        Then creates a file, where stores the members of the group.
        """
        new_contact = list()

        for contact_index in range(len(contacts_list)):
            if contact_index in contacts_index:
                new_contact.append(contacts_list[contact_index])

        with open("{}.wmg", "w") as file:
            file.write(",".join(new_contact))

    def close(self):
        """
        Closes driver.
        """
        self.driver.quit()

def arg_parsing():
    """
    Function to parse arguments from CLI.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-l", "--list", help="list_contacts", action="store_true")
    parser.add_argument("-s", "--send", help="send a message to a contact")
    parser.add_argument("-m", "--message", help="takes the message")
    parser.add_argument("-g", "--group", help="creates a group", action="store_true")

    return parser.parse_args()

def take_action(args, whatsmatic):
    """
    Decides what to do with the args given.
    """
    if args.version:
        print("WhatsMatic version 1.0.0")
    elif args.list:
        if args.group:
            print("\n".join(whatsmatic.get_groups()))
        else:
            print("\n".join(whatsmatic.get_contacts()))
    elif args.send and args.message:
        whatsmatic.send_message(args.send, args.message)
    elif args.send:
        print("ERROR: Missing message parameter.")
    elif args.message:
        print("ERROR: Missing send parameter.")

def main():
    whatsmatic = WhatsMatic("/home/joel/whatsmatic")
    print(whatsmatic.get_groups())

    # args = arg_parsing()
    # take_action(args, whatsmatic)

    whatsmatic.close()

if __name__ == "__main__":
    main()

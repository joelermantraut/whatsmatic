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
from automation_scripts.files_use import FileUse
from time import sleep
import argparse
from os import remove, getcwd
from os.path import exists, expanduser
import sys

class WhatsMatic(object):
    """App to control WhatsApp and automate it."""
    def __init__(self, HOME):
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
        self.files_path = getcwd()
        if exists(self.files_path + "/chromedriver.txt"):
            with open(self.files_path + "/chromedriver.txt", "r") as file:
                self.chromedriver = file.readline()
        else:
            self.chromedriver = HOME + "/chromedriver"

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            self.chromedriver,
            "https://web.whatsapp.com"
        )

        self.mouse = MouseControl()

        self.files = FileUse()

        self.driver.maximize()
        self.wait_for_scan()
        self.wait_for_notification_message()

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

        groups = self.files.list_files(r'.*.wmg')
        if groups == 0:
            print("There are no groups.")
            exit()

        return groups

    def group_exists(self, group_name):
        """
        Checks if a group with that name was already created.
        """
        if group_name in self.get_groups():
            return True
        else:
            return False

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

        for index in range(len(contacts_list)):
            if str(index) in contacts_index:
                new_contact.append(contacts_list[index])

        with open("{}/{}".format(self.files_path, name), "w") as file:
            file.write(",".join(new_contact))

        return "{}/{}".format(self.files_path, name)

    def create_group_routine(self):
        """
        Routine to create a new group.
        """
        print("Insert group name: ")
        group_name = input()

        group_name += ".wmg"
        # Adds extension to filename

        if self.group_exists(group_name):
            print("Group already exists. Do you want to overwrite it: ")
            response = input()
            if response.lower() in ['y', 'yes']:
                print("Overwrote.")
            else:
                return False

        print("Contacts will be numerically list.")
        print("Write comma separated indexes of contacts to include.")
        contacts = self.get_contacts()
        for contact_index in range(len(contacts)):
            print("{}. {}".format(contact_index, contacts[contact_index]))

        print("Contact list: ")
        contact_list = input()
        self.create_a_group(group_name, contacts, contact_list.split(","))
        return True

    def remove_group_routine(self):
        """
        Shows routine to remove a group.
        """
        groups = self.get_groups()

        for group_index in range(len(groups)):
            print("{}. {}".format(group_index, groups[group_index]))

        print("Select a group: ")
        group_number = input()
        print("Remove group {}?".format(groups[int(group_number)]))
        response = input()
        if response.lower() in ['y', 'yes']:
            remove(groups[int(group_number)])
            print("Group removed.")

    def edit_group_routine(self):
        """
        Shows routine to edit a group.
        """
        groups = self.get_groups()

        for group_index in range(len(groups)):
            print("{}. {}".format(group_index, groups[group_index]))

        print("Select a group: ")
        group_number = input()

        print("Contacts will be numerically list.")
        print("Write comma separated indexes of contacts to include.")
        contacts = self.get_contacts()
        for contact_index in range(len(contacts)):
            print("{}. {}".format(contact_index, contacts[contact_index]))

        print("Contact list: ")
        contact_list = input()

        remove(groups[int(group_number)])
        group_name = groups[int(group_number)].split('/')[-1]
        self.create_a_group(group_name, contacts, contact_list.split(","))

    def manage_groups(self, option):
        """
        Interface to add/edit/remove groups.
        """
        if option == "1":
            print("Create a group.")
            self.create_group_routine()
        elif option == "2":
            print("Remove a group.")
            self.remove_group_routine()
        elif option == "3":
            print("Edit a group")
            self.edit_group_routine()
        else:
            print("Incorrect option.")
            exit()

    def close(self):
        """
        Closes driver.
        """
        self.driver.quit()

def arg_parsing(parser):
    """
    Function to parse arguments from CLI.
    """
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-l", "--list", help="list_contacts", action="store_true")
    parser.add_argument("-s", "--send", help="send a message to a contact")
    parser.add_argument("-m", "--message", help="takes the message")
    parser.add_argument("-g", "--group", help="manage groups")
    parser.add_argument("-c", "--chromedriver", help="sets default location of Chromedriver")

def take_action(parser, whatsmatic):
    """
    Decides what to do with the args given.
    """
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    # No argument given
    elif args.version:
        print("WhatsMatic version 1.0.0")
    elif args.list and args.group:
        print("\n".join(whatsmatic.get_groups()))
    elif args.send and not args.message:
        print("ERROR: Missing message parameter.")
    elif args.message and not args.send and not args.group:
        print("ERROR: Missing send parameter.")
    elif args.chromedriver:
        with open(whatsmatic.files_path + "/chromedriver.txt", "w") as file:
            file.write(args.chromedriver)
    else:
        # All functions that need WhatsMatic to open WhatsApp
        whatsmatic.init()

        if args.list:
            print("\n".join(whatsmatic.get_contacts()))
        elif args.send and args.message:
            whatsmatic.send_message(args.send, args.message)
        elif args.group:
            if args.message:
                whatsmatic.send_to_group(args.group, args.message)
            else:
                whatsmatic.manage_groups(args.group)

        whatsmatic.close()

def main():
    HOME = expanduser('~')
    whatsmatic = WhatsMatic(HOME)

    parser = argparse.ArgumentParser()
    arg_parsing(parser)
    take_action(parser, whatsmatic)

if __name__ == "__main__":
    main()

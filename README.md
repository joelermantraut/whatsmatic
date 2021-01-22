# whatsmatic
Whatsmatic is a CLI application with the purpose of automate use of WhatsApp. 

It includes functions like:
- Send a message to a particular contact.
- Send the same message to a list of contacts.
- Manage groups out of WhatsApp

## Usage
```
$ python main.py -h

usage: main.py [-h] [-v] [-l] [-s SEND] [-m MESSAGE] [-g GROUP]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program version
  -l, --list            list_contacts
  -s SEND, --send SEND  send a message to a contact
  -m MESSAGE, --message MESSAGE
                        takes the message
  -g GROUP, --group GROUP
                        manage groups
  -c CHROMEDRIVER, --chromedriver CHROMEDRIVER
                        sets default location of Chromedriver
```

Adittionally, you can mix commands. For example:

| Parameters | Function |
|-----------|------------|
| -m and -g | Send message to a group |
| -l and -g | List groups |

## To consider

 - Each time you want to do an action, you must login using QR code.
 - When it starts, waits up to notification message appears (over list of chats)
   and deletes it.
 - When it list contacts, WhatsApp window must be visible.
 - Default location of chromedriver is in HOME folder. It can be editted with a parameter.

## Spam
This app was developed using some of the automation_scripts, included in this repository.

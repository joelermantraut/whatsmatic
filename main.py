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

"""


from automation_scripts.web_scrapping import WebScrapper
import time

class WhatsMatic(object):
    """Class to control WhatsApp and automate it."""
    def __init__(self):
        self.init() 

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            "/home/joel/Apps/chromedriver",
            "https://web.whatsapp.com"
        )

        time.sleep(10)

        self.close()

    def close(self):
        """
        Closes driver.
        """
        self.driver.quit()

def main():
    whatsmatic = WhatsMatic()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

"""

Class to simplify the use of the mouse.

TODO:

    - Añadir las funciones de monitoreo.

"""

from pynput import mouse
from screeninfo import get_monitors

class MouseControl(object):
    """Class to simplify the use of the mouse"""

    def __init__(self):
        super(MouseControl, self).__init__()

        self.mouse_buttons = {
            'left': mouse.Button.left,
            'middle': mouse.Button.middle,
            'right': mouse.Button.right
        }
        self.transpose_button = {key: value for (value, key) in self.mouse_buttons.items()}
        self.on_move_f = None
        self.on_click_f = None
        self.on_scroll_f = None
        self.scrolling_distance = 60
        self.init()

    def init(self):
        """
        Runs some init functions.

         - Inits controller.
        """
        self.controller = mouse.Controller()

    def mouse_move(self, move=None, rel=False, drag=False, function=None, iters=1):
        """"
        Moves the mouse taking care of:

            - If receives a function, executes it before each cycle.
            - If rel, enables relative move.
            - If drag, moves the mouse with the left button pressed.
            - If move == None, return the current position of the mouse.
        """

        if move == None:
            return self.controller.position()

        if drag:
            self.controller.press(mouse.Button.left)
            if rel:
                self.controller.move(*move)
            else:
                self.controller.position = move

            self.controller.release(self.mouse_buttons['left'])

        if function:
            for i in range(iters):
                x, y = function()
                self.controller.position = (x, y)
        else:
            if rel:
                self.controller.move(*move)
            else:
                self.controller.position = move

    def click(self, button, clicks=1):
        """
        Click in the current position of the mouse. 
        """

        button = self.mouse_buttons[button]

        self.controller.click(button, clicks)

    def scroll(self, amount, percent=False):
        """
        Scrolls up or down.

         - If percent, moves that percent of the screen.
        """
        if percent:
            first_monitor_height = get_monitors()[0].height

            amount = int((amount / 100) * first_monitor_height)

        self.controller.scroll(0, -amount // self.scrolling_distance)

    # --------------------------------------------------
    # --------------- MOUSE MONITORING -----------------
    # --------------------------------------------------

    def on_move(self, x, y):
        """
        On move event.
        """

        if self.on_move_f != None:
            self.on_move_f(x, y)

    def on_click(self, x, y, button, pressed):
        """
        On click event.
        """
        button = self.transpose_button[button]

        if self.on_click_f != None:
            self.on_click_f(x, y, button, pressed)

    def on_scroll(self, x, y, dx, dy):
        """
        On scroll event.
        """
        if self.on_scroll_f != None:
            self.on_scroll_f(dx, dy)

    def start_listening(
            self,
            on_move=None,
            on_click=None,
            on_scroll=None,
            blocking=False
        ):
        """
        Function that configures the listening using
        arguments to set all properties.
        """

        self.on_move_f = on_move 
        self.on_click_f = on_click
        self.on_scroll_f = on_scroll

        if blocking:
            with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll
            ) as listener:
                listener.join()
        else:
            listener = mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll
            )
            listener.start()

def on_move_p(x, y):
    print(x, ':', y)

def on_click_p(x, y, button, pressed):
    print(x, ':', y, ':', button, ':', pressed)

def on_scroll_p(dx, dy):
    print(dx, ':', dy)

def main():
    mouse_controller = MouseControl()

    mouse_controller.start_listening(
            on_move=on_move_p,
            on_click=on_click_p,
            on_scroll=on_scroll_p,
            blocking=True)

if __name__ == "__main__":
    main()

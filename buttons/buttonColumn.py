from button import *


class ButtonColumn(object):

    def __init__(self, column_id, num_rows):
        self.column_id = column_id
        self.num_rows = num_rows
        self.buttons = []

    def check_event(self, event):
        for button in self.buttons:
            button.check_mouse_key_event(event)

    def add_button(self, button, start_row, end_row=-1):
        self.buttons.insert(start_row, button)
        self.__add_pointers__(self.column_id, start_row, end_row)

    def add_pointer(self, start_column, start_row, end_row=-1):
        self.buttons.insert(start_row, Button(None, pointer=(start_column, start_row)))
        self.__add_pointers__(start_column, start_row, end_row)

    def __add_pointers__(self, start_column, start_row, end_row):
        if end_row != -1:
            for i in range(start_row+1, end_row):
                self.buttons.insert(i, Button(None, pointer=(start_column, start_row)))

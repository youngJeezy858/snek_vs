from buttonColumn import *
from pygame.locals import *


class ButtonGrid(object):

    def __init__(self, num_columns, num_rows, controller_position=(0, 0)):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.columns = []
        for i in range(0, num_columns):
            self.columns.append(ButtonColumn(i, num_rows))
        self.controller_position = controller_position

    def add_button(self, button, start_column, start_row, end_column=-1, end_row=-1):
        self.columns[start_column].add_button(button, start_row, end_row)
        if end_column != -1:
            for i in range(start_column+1, end_column):
                self.columns[i].add_pointer(start_column, start_row, end_row)

    def check_controller_event(self, event):
        if event.type == JOYHATMOTION:
            x = self.controller_position[0] + event.value[0]
            y = self.controller_position[1] + event.value[1]
            if x > self.num_columns - 1:
                x = 0
            elif x < 0:
                x = self.num_columns - 1
            if y > self.num_rows - 1:
                y = 0
            elif y < 0:
                y = self.num_rows - 1
            # Rewind the animation of the previous button that the Controller was on
            old_button = self.columns[self.controller_position[0]].buttons[self.controller_position[1]]
            if old_button.animation_state == Button.PLAY_UNTIL_END or old_button.animation_state == Button.PAUSED_AT_END:
                old_button.animation_state = Button.REWIND_UNTIL_START
            # Find the position of the current button
            self.controller_position = self.find_controller_position(x, y)
        # Play animation of the button the Controller is currently on
        button = self.columns[self.controller_position[0]].buttons[self.controller_position[1]]
        button.animation_state = Button.PLAY_UNTIL_END
        # Check if the button should be activated
        button.check_controller_event(event)

    def check_mouse_key_event(self, event):
        for column in self.columns:
            column.check_event(event)

    def find_controller_position(self, x, y):
        button = self.columns[x].buttons[y]
        while button.pointer != (-1, -1):
            x = button.pointer[0]
            y = button.pointer[1]
            button = self.columns[x].buttons[y]
        return x, y

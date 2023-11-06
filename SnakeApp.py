from random import random, randrange

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector


class Playfield(FloatLayout):

    def __init__(self, **kwargs):
        '''initiate the playfield'''
        super(Playfield, self).__init__(**kwargs)

        #remove all existing widgets from previous game
        self.clear_widgets()

        #create chess board pattern on float layout
        self.rows = 20
        self.cols = 20
        self.widget_size = Window.size[0] / 20 - 2

        #add first fruit
        self.fruit = Fruit(grid_pos= (10,11))
        self.add_my_widget(self.fruit)

        # add head
        self.head = Head()
        self.add_my_widget(self.head)

        #start clock to move the head
        self.update_interval = 1.0
        self.move_head_clock = Clock.schedule_interval(lambda dt: self.move_head(self.head), self.update_interval)

        #start clock to make the game faster
        self.speed_up_clock = Clock.schedule_interval(lambda dt: self.speed_up(), 10)

    def add_my_widget(self, widget):
        '''add a new widget on the grid'''
        widget.pos = (widget.grid_pos[0] * (self.widget_size + 2) + 1, widget.grid_pos[1] * (self.widget_size + 2) + 1)
        widget.size_hint = (None, None)
        widget.size = (self.widget_size, self.widget_size)
        self.add_widget(widget)

    def move_head(self, widget):
        '''redraw the widget according to last position plus direction of motion'''
        direction = Vector(widget.direction)
        old_position_head = list(widget.grid_pos)
        old_position_last_body_part = list(self.children[0].grid_pos)

        #move the snake
        #exclude last child = fruit and next to last child = head
        if len(self.children) > 2:
            for i in range(0, len(self.children)-2):
                self.children[i].grid_pos = list(self.children[i+1].grid_pos)
                self.children[i].pos = (self.children[i].grid_pos[0] * (self.widget_size + 2) + 1, self.children[i].grid_pos[1] * (self.widget_size + 2) + 1)

        # move head
        widget.grid_pos[0] = old_position_head[0] + direction[0]
        widget.grid_pos[1] = old_position_head[1] + direction[1]
        widget.pos = (widget.grid_pos[0] * (self.widget_size + 2) + 1, widget.grid_pos[1] * (self.widget_size + 2) + 1)

        #game over if head leaves playfield
        if self.head_out_of_playfield(widget):
            self.restart_game()
            return

        #game over if head collides with body
        if self.body_collision():
            self.restart_game()
            return

        #add body part if fruit is collected
        if self.fruit_collision(widget):
            body = Body(grid_pos=old_position_last_body_part)
            self.add_my_widget(body)

            self.fruit.grid_pos = (randrange(0,19), randrange(0,19))
            self.fruit.pos = (self.fruit.grid_pos[0] * (self.widget_size + 2) + 1, self.fruit.grid_pos[1] * (self.widget_size + 2) + 1)
            return

        else:
            return

    def head_out_of_playfield(self, widget):
        '''Check if head is still within the playfield'''

        #TODO: Stop game once head is out of playfield
        if widget.x < 0 or widget.x > self.width:
            return True
        if widget.y < 0 or widget.y > self.height:
            return True
        else:
            return False

    def body_collision(self):
        '''Check if the head collides with the body'''
        #ignore last element(head) and next to last element(fruit)
        for element in self.children[:-2]:
            if self.children[-2].collide_widget(element):
                return True
        else:
            return False

    def speed_up(self):
        '''decrease the interval in which the head is moved one grid position'''
        self.update_interval = self.update_interval -0.1
        print(self.update_interval)
        self.move_head_clock.cancel()
        self.move_head_clock = Clock.schedule_interval(lambda dt: self.move_head(self.head), self.update_interval)

    def fruit_collision(self, widget):
        if widget.collide_widget(self.fruit):
            print('you hit the fruit')
            return True
        else:
            return False

    def restart_game(self):
        '''stop all clocks and restart the game'''
        self.move_head_clock.cancel()
        self.speed_up_clock.cancel()
        self.__init__()

class Head(Widget):

    def __init__(self, grid_pos = None, direction = None,  **kwargs):
        super(Head, self).__init__(**kwargs)

        #position head in middle of the screen
        if grid_pos is None:
            grid_pos = [10, 10]
        self.grid_pos = grid_pos

        #Clock starts instantly and head moves into a defined direction. Make it random if wanted
        if direction is None:
            direction = Vector(0,1)
        self.direction = direction

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        '''read the keycode and set the direction accordingly'''
        if keycode[1] == 'up':
            self.direction = (0, 1)
        if keycode[1] == 'down':
            self.direction = (0, -1)
        if keycode[1] == 'left':
            self.direction = (-1, 0)
        if keycode[1] == 'right':
            self.direction = (1, 0)

        return True

    def reset_game(self):
        #TODO: reset game
        pass

class Body(Widget):
    def __init__(self, grid_pos = None,**kwargs):
        super(Body, self).__init__(**kwargs)

        if grid_pos is None:
            grid_pos = [0,0]
        self.grid_pos = grid_pos

class Fruit(Widget):
    def __init__(self, grid_pos = None,**kwargs):
        super(Fruit, self).__init__(**kwargs)

        if grid_pos is None:
            grid_pos = [0,0]
        self.grid_pos = grid_pos

class SnakeApp(App):
    def __init__(self, **kwargs):
        super(SnakeApp, self).__init__(**kwargs)
        Window.size = (600, 600)

if __name__ == '__main__':
    SnakeApp().run()
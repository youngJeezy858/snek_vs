from gameSprite import *
from pygame.locals import *
import math
from snekTail import *


class Player(GameSprite):

    # Player IDs
    COMPUTER = -9999

    # Player states
    ALIVE = 0
    DEAD = 1

    def __init__(self, player_id, color, shade_id, dimensions, position, controller_id, movement_speed, x_add=0, y_add=-1):
        self.state = self.ALIVE
        self.player_id = player_id
        self.color = color
        self.shade_id = shade_id
        image = "images/player_" + color + "_" + str(self.shade_id) + ".png"
        self.font_color = (255, 255, 255)
        if color == "blue":
            self.font_color = (0, 0, 255)
        elif color == "red":
            self.font_color = (255, 0, 0)
        super(Player, self).__init__(image, dimensions, position)
        self.real_x = float(position[0])
        self.real_y = float(position[1])
        self.x_add = float(x_add)
        self.y_add = float(y_add)
        self.x_revert = float(x_add)
        self.y_revert = float(y_add)
        self.movement_speed = float(movement_speed)
        self.controller_id = controller_id
        self.a_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.d_pressed = True
        self.snek_length = 4
        self.state = self.ALIVE
        # Default invulnerability at start is 5s
        self.invulnerable = True
        self.invulnerable_time = 120
        self.tail_sprites = pygame.sprite.Group()
        self.tail = []
        self.pause_timer = int(self.dimensions[0] / self.movement_speed)
        self.movement_governor = [position]
        self.govenator_degree = 60
        self.stats_font = pygame.font.SysFont("monospace", 16)
        self.winner_font = pygame.font.SysFont("monospace", 32)
        self.winner_display = self.winner_font.render(self.color, True, self.font_color)
        self.stats = self.stats_font.render(self.color + ": " + str(len(self.tail_sprites)), True, self.font_color)
        for i in range(self.snek_length):
            self.add_tail()

    def check_event(self, event):
        # Parse keyboard action
        if self.controller_id == -1:
            # Evaluate key being pressed or released
            if event.type == KEYDOWN:
                pressed = True
            elif event.type == KEYUP:
                pressed = False
            else:
                return
            # Evaluate which key is being acted on
            if event.key == K_a:
                self.a_pressed = pressed
            elif event.key == K_d:
                self.d_pressed = pressed
            elif event.key == K_w:
                self.w_pressed = pressed
            elif event.key == K_s:
                self.s_pressed = pressed
            return
        # Parse left stick action
        if event.type == JOYAXISMOTION:
            # Disregard any input from other controllers
            if self.controller_id != event.joy:
                return
            if event.axis == 0:
                self.x_revert = self.x_add
                self.x_add = event.value
            if event.axis == 1:
                self.y_revert = self.y_add
                self.y_add = event.value

    def update(self):
        # Evaluate the movement of the snek if you're using a keyboard
        if self.controller_id == -1:
            x, y = 0, 0
            if self.a_pressed:
                x = -1
            if self.d_pressed:
                x = 1
            if self.w_pressed:
                y = -1
            if self.s_pressed:
                y = 1
            if x != 0 or y != 0:
                self.x_add, self.y_add = x, y
        # Find distance of line on left stick (0, 0) -> (x_add, y_add)
        line_distance = self.pythagoras(self.x_add, self.y_add)
        # Stay the course if stick isn't pushed more than halfway
        if line_distance < .5:
            self.x_add = self.x_revert
            self.y_add = self.y_revert

        # Find the endpoint of the left stick (length of self.movement_speed)
        x = float((self.movement_speed * self.x_add) /
                  (math.sqrt((0-self.x_add) * (0-self.x_add) + (0-self.y_add) * (0-self.y_add))))
        y = float((self.movement_speed * self.y_add) /
                  (math.sqrt((0-self.x_add) * (0-self.x_add) + (0-self.y_add) * (0-self.y_add))))

        # GOVERNATOR!!!
        if len(self.movement_governor) > self.pause_timer*2:
            tx = float(self.rect.center[0] - self.movement_governor[0][0])
            ty = float(self.rect.center[1] - self.movement_governor[0][1])
            x, y = self.governator(tx, ty, x, y)
            self.movement_governor.pop(0)
        self.movement_governor.append(self.rect.center)

        # Find the endpoint of the previous tail center
        self.real_x += x
        self.real_y += y
        self.position = (self.real_x, self.real_y)
        for t in self.tail_sprites:
            t.position_queue.append(self.position)
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1
            if self.invulnerable_time == 0:
                self.invulnerable = False
        super(Player, self).update()

    def add_tail(self):
        if len(self.tail) == 0:
            p = self.position
            q = []
        else:
            end_tail = self.tail[-1]
            p = end_tail.position
            q = end_tail.position_queue
        t = SnekTail(self.image_path, self.dimensions, p, self.controller_id, self.pause_timer, q)
        self.tail_sprites.add(t)
        self.tail.append(t)
        self.stats = self.stats_font.render(self.color + ": " + str(len(self.tail_sprites)), True, self.font_color)
        return t

    def draw_tail(self, screen):
        self.tail_sprites.draw(screen)

    def update_tail(self):
        self.tail_sprites.update()

    def pop_tail(self):
        if self.tail_sprites:
            end_tail = self.tail[-1]
            self.tail_sprites.remove(end_tail)
            return self.tail.pop()
        else:
            return None

    def pythagoras(self, x, y):
        return math.sqrt((x * x) + (y * y))

    def find_degrees(self, x, y):
        if x == 0:
            if y >= 0:
                return 90
            else:
                return 270
        elif y == 0:
            if x > 0:
                return 0
            else:
                return 180
        else:
            degrees = math.degrees(math.atan(y / x))
            quadrant_modifier = 0
            if x < 0:
                quadrant_modifier = 180
            elif y < 0:
                quadrant_modifier = 360
            return degrees + quadrant_modifier

    def governator(self, governator_x, governator_y, left_stick_x, left_stick_y):
        # Find the angle between the left stick and the governator
        governator_angle = self.find_degrees(governator_x, governator_y)
        left_stick_angle = self.find_degrees(left_stick_x, left_stick_y)
        degree_of_movement = abs(governator_angle - left_stick_angle)
        if degree_of_movement > 180:
            degree_of_movement = 360 - degree_of_movement
        # Enforce the govenator if degree of movement is too big of a change
        if degree_of_movement > self.govenator_degree:
            # Find the direction of the movement (clockwise [1] or counter clockwise [-1])
            direction_of_movement = self.find_movement_direction(governator_angle, left_stick_angle)
            governed_left_stick_angle = governator_angle + (self.govenator_degree * direction_of_movement)
            # Account for governmental oversight (angles > 360 or angles < 0)
            if governed_left_stick_angle < 0.0:
                governed_left_stick_angle += 360
            elif governed_left_stick_angle > 360:
                governed_left_stick_angle -= 360
            # Find and set the governed (x, y) Yay regulations!
            x = self.movement_speed * math.cos(math.radians(governed_left_stick_angle))
            y = self.movement_speed * math.sin(math.radians(governed_left_stick_angle))
            return x, y
        # Else just allow the left stick change
        else:
            return left_stick_x, left_stick_y

    def find_movement_direction(self, origin_angle, dest_angle):
        # I ain't fucking around with the same degrees
        if origin_angle == 360:
            origin_angle = 0
        if dest_angle == 360:
            dest_angle = 0
        degrees = int(origin_angle)
        for count in range(0, 180):
            if degrees == int(dest_angle):
                return 1.0
            degrees += 1
            if degrees == 360:
                degrees = 0
        return -1.0

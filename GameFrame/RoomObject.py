import os
import math
import pygame
from GameFrame import Level
from typing import List, Tuple, Callable


class RoomObject:
    def __init__(self, room: Level, x: int, y: int):
        self.room = room
        self.depth = 0
        self.x = x
        self.y = y
        self.rect = 0
        self.prev_x = x
        self.prev_y = y
        self.width = 0
        self.height = 0
        self.image = 0
        self.image_orig = 0
        self.curr_rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0
        self.handle_key_events = False
        self.handle_mouse_events = False
        self.angle = 0

        self.collision_object_types = set()
        self.collision_objects = []

    @staticmethod
    def load_image(file_name: str) -> str:
        return os.path.join('Images', file_name)

    def set_image(self, image: str, width: int, height: int):
        self.image_orig = pygame.image.load(image).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
        self.width = width
        self.height = height
        self.image = self.image_orig.copy()
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def register_collision_object(self, collision_object: str):
        self.collision_object_types.add(collision_object)

    def update(self):
        self.y_speed = self.y_speed + self.gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def delete_object(self, obj: 'RoomObject'):
        self.room.delete_object(obj)

    def remove_object(self, obj: 'RoomObject'):
        for index, list_obj in enumerate(self.collision_objects):
            if list_obj is obj:
                self.collision_objects.pop(index)

    def step(self):
        pass

    def check_collisions(self):
        for item in self.collision_objects:
            if self.rect.colliderect(item.rect):
                item_type = type(item).__name__
                self.handle_collision(item, item_type)

    def collides_at(self, obj, x, y, collision_type):
        check_rect = obj.rect.move(x, y)
        collision_found = False
        for item in self.collision_objects:
            if check_rect.colliderect(item.rect):
                if type(item).__name__ == collision_type:
                    collision_found = True
                    break
        return collision_found

    def handle_collision(self, other, other_type):
        pass

    def key_pressed(self, key):
        pass

    def joy_pad_signal(self, p1_buttons: List[int], p2_buttons: List[int]):
        pass

    def clicked(self, button_number):
        pass

    def mouse_event(self, mouse_x, mouse_y, button_left, button_middle, button_right):
        pass

    def bounce(self, other):

        # self is to the side of other
        if other.rect.top < self.rect.centery < other.rect.bottom:
            self.x_speed *= -1
            self.x = self.prev_x

        # self is above or below other
        if other.rect.left < self.rect.centerx < other.rect.right:
            self.y_speed *= -1
            self.y = self.prev_y

    def blocked(self):

        self.x = self.prev_x
        self.y = self.prev_y
        self.x_speed = 0
        self.y_speed = 0

    def set_timer(self, ticks: int, function_call: Callable):
        self.room.set_timer(ticks, function_call)

    def set_direction(self, angle: int, speed: int):
        if angle < 0:
            pass
        elif angle == 0:
            self.x_speed = speed
            self.y_speed = 0
        elif angle < 90:
            self.x_speed, self.y_speed = self._get_direction(angle, speed)
        elif angle == 90:
            self.x_speed = 0
            self.y_speed = speed
        elif angle < 180:
            self.x_speed, self.y_speed = self._get_direction(angle - 90, speed)
            self.x_speed, self.y_speed = -self.y_speed, self.x_speed
        elif angle == 180:
            self.x_speed = -speed
            self.y_speed = 0
        elif angle < 270:
            self.x_speed, self.y_speed = self._get_direction(angle - 180, speed)
            self.x_speed, self.y_speed = -self.x_speed, -self.y_speed
        elif angle == 270:
            self.x_speed = 0
            self.y_speed = -speed
        elif angle < 360:
            self.x_speed, self.y_speed = self._get_direction(angle - 270, speed)
            self.x_speed, self.y_speed = self.y_speed, -self.x_speed

    @staticmethod
    def _get_direction(angle: int, speed: int):
        # Use Trigonometry to calculate x_speed and y_speed values
        new_x_speed = math.cos(math.radians(angle)) * speed
        new_y_speed = math.sin(math.radians(angle)) * speed

        return round(new_x_speed), round(new_y_speed)

    def get_direction_coordinates(self, angle: int, speed: int) -> Tuple[int, int]:
        x, y = 0, 0
        angle += 90
        if angle >= 360:
            angle = angle - 360

        if angle == 0:
            x = speed
            y = 0
        elif angle < 90:
            x, y = self._get_direction(angle + 90, speed)
            x, y = y, x
        elif angle == 90:
            x = 0
            y = -speed
        elif angle < 180:
            x, y = self._get_direction(angle, speed)
            y *= -1
        elif angle == 180:
            x = -speed
            y = 0
        elif angle < 270:
            x, y = self._get_direction(angle - 90, speed)
            y, x = -x, -y
        elif angle == 270:
            x = 0
            y = speed
        elif angle < 360:
            x, y = self._get_direction(angle - 180, speed)
            y, x = y, -x

        return x, y

    def rotate(self, angle: int):

        if self.curr_rotation > 360:
            self.curr_rotation = self.curr_rotation - 360
        elif self.curr_rotation < 0:
            self.curr_rotation = 350 - self.curr_rotation

        self.curr_rotation = self.angle = angle + self.curr_rotation

        self.image = pygame.transform.rotate(self.image_orig, self.angle)

        x, y = self.rect.center

        self.rect = self.image.get_rect()

        self.x = x - int((self.rect.width / 2))
        self.y = y - int((self.rect.height / 2))

        self.rect.x = self.x
        self.rect.y = self.y

    def rotate_to_coordinate(self, mouse_x: int, mouse_y: int):
        distance_x = self.x + (self.width / 2) - mouse_x
        distance_y = self.y + (self.height / 2) - mouse_y

        angle = math.degrees(math.atan2(distance_x, distance_y))

        self.curr_rotation = 0
        self.rotate(int(angle))

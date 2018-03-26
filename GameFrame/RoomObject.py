import math
import os
import pygame


class RoomObject:

    def __init__(self, room, x, y):
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
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0
        self.handle_key_events = False
        self.handle_mouse_events = False

        self.collision_object_types = set()
        self.collision_objects = []

    def load_image(self, file_name):
        return os.path.join('Images', file_name)

    def set_image(self, image, width, height):
        self.image = pygame.image.load(image).convert_alpha()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def register_collision_object(self, collision_object):
        self.collision_object_types.add(collision_object)

    def update(self):
        self.y_speed = self.y_speed + self.gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def delete_object(self, obj):
        self.room.delete_object(obj)

    def remove_object(self, obj):
        for index, list_obj in enumerate(self.collision_objects):
            if list_obj is obj:
                self.collision_objects.pop(index)

    def step(self):
        pass

    def check_collisions(self):
        for item in self.collision_objects:
            if self.rect.colliderect(item.rect):
                self.handle_collision(item)

    def collides_at(self, obj, x, y, collision_type):
        check_rect = obj.rect.move(x, y)
        collision_found = False
        for item in self.collision_objects:
            if check_rect.colliderect(item.rect):
                if type(item).__name__ == collision_type:
                    collision_found = True
                    break
        return collision_found

    def handle_collision(self, other):
        pass

    def key_pressed(self, key):
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

    def set_timer(self, ticks, function_call):
        self.room.set_timer(ticks, function_call)

    def set_direction(self, angle, speed):
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

    def _get_direction(self, angle, speed):
        # Use Trigonometry to calculate x_speed and y_speed values
        new_x_speed = math.cos(math.radians(angle)) * speed
        new_y_speed = math.sin(math.radians(angle)) * speed

        return round(new_x_speed), round(new_y_speed)

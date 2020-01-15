import os
import pygame
from typing import List
from pygame import Surface
from typing import Callable
from pygame.mixer import Sound
from pygame.joystick import Joystick
from GameFrame.Globals import Globals
from GameFrame.RoomObject import RoomObject


class Level:

    def __init__(self, screen: Surface, joysticks: Joystick):
        self.screen = screen
        self.objects = []
        self.keyboard_objects = []
        self.mouse_objects = []
        self._clock = pygame.time.Clock()
        self.running = False
        self.quitting = False
        self.background_set = False
        self.background_image = 0
        self.background_y = 0
        self.background_scroll_speed = 0
        self.background_scrolling = False
        self.user_events = []
        self.joysticks = joysticks
        self.p1_btns = []
        self.p2_btns = []
        self.has_buttons_1 = False
        self.has_buttons_2 = False
        self.has_hat_1 = False
        self.has_hat_2 = False
        if len(self.joysticks) > 0:
            buttons = self.joysticks[0].get_numbuttons()
            if buttons > 0:
                self.has_buttons_1 = True
            for i in range(buttons):
                self.p1_btns.append(self.joysticks[0].get_button(i))
            axes = self.joysticks[0].get_numaxes()
            if axes > 0:
                self.has_hat_1 = True
            for i in range(axes):
                self.p1_btns.append(self.joysticks[0].get_axis(i))
            if len(self.joysticks) > 1:
                buttons = self.joysticks[1].get_numbuttons()
                if buttons > 0:
                    self.has_buttons_2 = True
                for i in range(buttons):
                    self.p2_btns.append(self.joysticks[1].get_button(i))
                axes = self.joysticks[1].get_numaxes()
                if axes > 0:
                    self.has_hat_2 = True
                for i in range(axes):
                    self.p1_btns.append(self.joysticks[1].get_axis(i))

    def run(self) -> bool:
        self.running = True
        for obj in self.objects:
            self.init_collision_list(obj)

        while self.running:
            self._clock.tick(Globals.FRAMES_PER_SECOND)

            for obj in self.objects:
                obj.prev_x = obj.x
                obj.prev_y = obj.y

            # - Process user events - #
            self.process_user_events()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quitting = True
                    Globals.exiting = True
                    pass
                # - Check for mouse click and pass to objects registered for mouse events - #
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for obj in self.mouse_objects:
                        if obj.rect.collidepoint(mouse_pos):
                            obj.clicked(event.button)

            # -  Check for joystick events and pass  - #
            # - to objects registered for key events - #
            signals = False
            if self.has_buttons_1:
                for i in range(self.joysticks[0].get_numbuttons()):
                    self.p1_btns[i] = self.joysticks[0].get_button(i)
                    if self.p1_btns[i] == 1:
                        signals = True
            if self.has_hat_1:
                for i in range(self.joysticks[0].get_numaxes()):
                    self.p1_btns[-(i+1)] = self.joysticks[0].get_axis(i)
                    if self.p1_btns[-(i+1)] > 0 or self.p1_btns[-(i+1)] < 0:
                        signals = True
            if self.has_buttons_2:
                for i in range(self.joysticks[1].get_numbuttons()):
                    self.p2_btns[i] = self.joysticks[1].get_button(i)
                    if self.p2_btns[i] == 1:
                        signals = True
            if self.has_hat_2:
                for i in range(self.joysticks[1].get_numaxes()):
                    self.p1_btns[-i] = self.joysticks[1].get_axis(i)
                    if self.p2_btns[-i] > 0 or self.p2_btns[-i] < 0:
                        signals = True

            if signals:
                for obj in self.keyboard_objects:
                    obj.joy_pad_signal(self.p1_btns, self.p2_btns)

            # - Check for a keyboard event and pass - #
            # - to objects registered for key events - #
            keys = pygame.key.get_pressed()
            if len(keys):
                for obj in self.keyboard_objects:
                    obj.key_pressed(keys)

            # - Check for a mouse event and pass - #
            # - to objects registered for mouse events - #
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            (button_left, button_middle, button_right) = pygame.mouse.get_pressed()
            for obj in self.mouse_objects:
                    obj.mouse_event(mouse_x, mouse_y, button_left, button_middle, button_right)

            # - Handle all other events - #
            self.catch_events(events)

            # - Clear the screen - #
            self.screen.fill((0, 0, 0))
            # - Add Background if set - #
            if self.background_set:
                # - Scrolling if set - #
                if self.background_scrolling:
                    self.background_y += self.background_scroll_speed
                    if self.background_y >= Globals.SCREEN_HEIGHT:
                        self.background_y = 0
                    self.screen.blit(self.background_image, (0, self.background_y))
                    self.screen.blit(self.background_image, (0, self.background_y - Globals.SCREEN_HEIGHT))
                else:
                    self.screen.blit(self.background_image, (0, 0))
            # Call Update on all objects
            for item in self.objects:
                item.update()
                item.step()

            # Check collisions
            for item in self.objects:
                item.check_collisions()

            for item in self.objects:
                self.screen.blit(item.image, (item.x, item.y))

            pygame.display.update()

        return self.quitting

    def set_background_image(self, image_file: str):
        self.background_set = True
        self.background_image = pygame.image.load(os.path.join('Images', image_file)).convert_alpha()

    def set_background_scroll(self, speed: int):
        self.background_scrolling = True
        self.background_scroll_speed = speed

    def add_room_object(self, room_object: RoomObject):
        # - Add to room objects list - #
        if len(self.objects) == 0:
            self.objects.append(room_object)
        else:
            for index, item in enumerate(self.objects):
                if item.depth >= room_object.depth:
                    self.objects.insert(index, room_object)
                    break
                elif index == len(self.objects) - 1:
                    self.objects.append(room_object)
                    break

        # - Add objects that handle key events to array - #
        if room_object.handle_key_events:
            self.keyboard_objects.append(room_object)

        # - Add objects that handle mouse events to array - #
        if room_object.handle_mouse_events:
            self.mouse_objects.append(room_object)

        if self.running:
            for obj in self.objects:
                self.init_collision_list(obj)

    def load_sound(self, sound_file: str) -> Sound:
        fq_filename = os.path.join('Sounds', sound_file)
        return pygame.mixer.Sound(fq_filename)

    def load_image(self, file_name: str) -> str:
        return os.path.join('Images', file_name)

    def init_collision_list(self, room_object: RoomObject):
        # - Initialise collision list for object - #
        for obj_name in room_object.collision_object_types:
            for obj_instance in self.objects:
                if type(obj_instance).__name__ == obj_name and obj_instance is not room_object:
                    room_object.collision_objects.append(obj_instance)

    def catch_events(self, events):
        pass

    def delete_object(self, obj: RoomObject):
        for index, list_obj in self.enumerate_backwards(self.objects):
            if list_obj is obj:
                self.objects.pop(index)
            else:
                list_obj.remove_object(obj)
        for index, list_obj in self.enumerate_backwards(self.keyboard_objects):
            if list_obj is obj:
                self.keyboard_objects.pop(index)
        for index, list_obj in self.enumerate_backwards(self.mouse_objects):
            if list_obj is obj:
                self.mouse_objects.pop(index)
        # Remove any timed function calls for the deleted object
        for index, event_method in self.enumerate_backwards(self.user_events):
            obj_inst = event_method[1].__self__
            if obj_inst is obj:
                self.user_events.pop(index)

    def set_timer(self, ticks: int, function_call: Callable):
        self.user_events.append([ticks, function_call])

    def process_user_events(self):
        for index, user_event in self.enumerate_backwards(self.user_events):
            user_event[0] -= 1
            if user_event[0] <= 0:
                event = user_event[1]
                self.user_events.pop(index)
                event()

    # Iterate backwards over a list, using an index and item iterator
    def enumerate_backwards(self, object_list: List):
        index = len(object_list)
        for item in reversed(object_list):
            index -= 1
            yield index, item

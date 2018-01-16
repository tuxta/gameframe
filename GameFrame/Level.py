import os
import pygame
from GameFrame.Globals import Globals


class Level:

    def __init__(self, screen):
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

    def run(self):
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

            # - Check for a keyboard event and pass - #
            # - to objects registered for key events - #
            keys = pygame.key.get_pressed()
            if len(keys) > 0:
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
                    self.screen.blit(self.background_image, (0, self.background_y - 600))
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

    def set_background_image(self, image_file):
        self.background_set = True
        self.background_image = pygame.image.load(os.path.join('Images', image_file))

    def set_background_scroll(self, speed):
        self.background_scrolling = True
        self.background_scroll_speed = speed

    def add_room_object(self, room_object):
        # - Add to room objects list - #
        if len(self.objects) == 0:
            self.objects.append(room_object)
        else:
            for index, item in enumerate(self.objects):
                if item.depth >= room_object.depth:
                    self.objects.insert(index, room_object)
                    break
                if index == len(self.objects) - 1:
                    self.objects.append(room_object)

        # - Add objects that handle key events to array - #
        if room_object.handle_key_events:
            self.keyboard_objects.append(room_object)

        # - Add objects that handle mouse events to array - #
        if room_object.handle_mouse_events:
            self.mouse_objects.append(room_object)

        if self.running:
            for obj in self.objects:
                self.init_collision_list(obj)

    def load_sound(self, sound_file):
        fq_filename = os.path.join('Sounds', sound_file)
        return pygame.mixer.Sound(fq_filename)

    def load_image(self, file_name):
        return os.path.join('Images', file_name)

    def init_collision_list(self, room_object):
        # - Initialise collision list for object - #
        for obj_name in room_object.collision_object_types:
            for obj_instance in self.objects:
                if type(obj_instance).__name__ == obj_name and obj_instance is not room_object:
                    room_object.collision_objects.append(obj_instance)

    def catch_events(self, events):
        pass

    def delete_object(self, obj):
        for index, list_obj in enumerate(self.objects):
            if list_obj is obj:
                self.objects.pop(index)
            else:
                list_obj.remove_object(obj)
        for index, list_obj in enumerate(self.keyboard_objects):
            if list_obj is obj:
                self.keyboard_objects.pop(index)
        for index, list_obj in enumerate(self.mouse_objects):
            if list_obj is obj:
                self.mouse_objects.pop(index)

    def set_timer(self, ticks, function_call):
        self.user_events.append([ticks, function_call])

    def process_user_events(self):
        for index, user_event in enumerate(self.user_events):
            user_event[0] -= 1
            if user_event[0] <= 0:
                user_event[1]()
                self.user_events.pop(index)

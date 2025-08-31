import pygame
import time

class Canvas:
    def __init__(self, drawing_surface, input_manager, header_height=100):
        self.surface = drawing_surface
        self.input_manager = input_manager
        self.refresh_interval = 0.1
        self.last_refresh_time = 0
        self.header_height = header_height

    # Clear the canvas
    def clear(self):
        self.surface.fill((255, 255, 255))

    # Redraw the canvas
    def refresh(self):
        current_time = time.time()
        if current_time - self.last_refresh_time < self.refresh_interval:
            return
        self.last_refresh_time = current_time

        self.clear()
        devices = self.input_manager.get_active_inputs()

        # For previous lines
        for device_id in devices:
            device = self.input_manager.get_device(device_id)
            if device:
                for stroke in device.get_undo_stack() or []:
                    line, color = stroke
                    if len(line) > 1:
                        adjusted_line = [(x, y - self.header_height) for (x, y) in line]
                        pygame.draw.lines(self.surface, color, False, adjusted_line, self.input_manager.get_size(device_id))

        # For current lines
        for device_id in devices:
            device = self.input_manager.get_device(device_id)
            if device:
                current_line = device.get_current_line()
                if current_line and len(current_line) > 1:
                    adjusted_line = [(x, y - self.header_height) for (x, y) in current_line]
                    pygame.draw.lines(self.surface, device.get_color(), False, adjusted_line, self.input_manager.get_size(device_id))

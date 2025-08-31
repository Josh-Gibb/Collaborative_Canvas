import pygame
import time
from logging_manager import logger
from tool_button import ToolButton
from color_button import ColorButton

class HeaderManager:
    def __init__(self, header_surface, colors):
        self.surface = header_surface
        self.buttons = [
            ToolButton('Undo', '<-', (100, 50), (255, 255, 255)),
            ToolButton('Redo', '->', (250, 50), (255, 255, 255)),
            ToolButton('Clear', 'X', (400, 50), (255, 255, 255)),
            ToolButton('Eraser', 'E', (550, 50), (255, 255, 255)),
            ToolButton('Marker', 'M', (700, 50), (0, 0, 0)),
            ToolButton('Change Color', 'C', (850, 50), (128, 128, 128))
        ]
        self.show_palette = False
        self.palette_buttons = [
            ColorButton(color, (950 + i * 50, 50)) for i, color in enumerate(colors)
        ]
        self.last_click_time = 0
        self.debounce_time = 0.1

    # Draw the header background and buttons on the dedicated header_surface.
    def draw(self):
        pygame.draw.rect(
            self.surface,
            (200, 200, 200),
            (0, 0, self.surface.get_width(), self.surface.get_height())
        )
        for button in self.buttons:
            button.draw(self.surface)
        if self.show_palette:
            for button in self.palette_buttons:
                button.draw(self.surface)

    def draw_buttons(self, device_positions):
        for button in self.buttons:
            combined_hover = any(button.is_clicked(pos) for pos in device_positions)
            button.draw(self.surface, hover=combined_hover)
        if self.show_palette:
            for button in self.palette_buttons:
                combined_hover = any(button.is_clicked(pos) for pos in device_positions)
                button.draw(self.surface, hover=combined_hover)

    # Process click events for header buttons.
    def handle_click(self, pos, device_path, input_manager):
        current_time = time.time()
        if current_time - self.last_click_time < self.debounce_time:
            return
        self.last_click_time = current_time

        for device in input_manager.get_active_inputs():
            current_line = input_manager.get_current_line(device)
            if current_line:
                input_manager.add_line(device)

        for button in self.buttons:
            if button.is_clicked(pos):
                logger.info(f"Button '{button.text}' clicked by {device_path}")
                if button.text == 'Undo':
                    input_manager.undo(device_path)
                elif button.text == 'Redo':
                    input_manager.redo(device_path)
                elif button.text == 'Clear':
                    input_manager.clear(device_path)
                elif button.text == 'Change Color':
                    self.show_palette = not self.show_palette
                elif button.text == 'Eraser':
                    input_manager.set_tool(device_path, 'Eraser')
                    input_manager.set_size(device_path, 5)
                elif button.text == 'Marker':
                    input_manager.set_tool(device_path, 'Marker')
                    input_manager.set_size(device_path, 5)
                return

        if self.show_palette:
            for color_button in self.palette_buttons:
                if color_button.is_clicked(pos):
                    logger.info(f"{device_path} changed color to {color_button.color}")
                    input_manager.set_color(device_path, color_button.color)
                    input_manager.set_tool(device_path, 'Marker')
                    self.show_palette = False
                    return

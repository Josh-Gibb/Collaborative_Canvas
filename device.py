from logging_manager import logger

class Device:   
    ADMIN = 'ImExPS/2 Generic Explorer Mouse'

    def __init__(self, device_id, name, user_id, position):
        self.device_id = device_id
        self.user_id = user_id
        self.name = name
        self.position = position
        self.color = (0, 0, 0)
        self.tool = "Marker"
        self.size = 5
        self.undo_stack = []
        self.redo_stack = []
        self.current_line = []
    
    def is_admin(self):
        return self.name == self.ADMIN

    # Set a device (x, y) position
    def set_position(self, new_pos):
        self.position = new_pos

    # Return a device position
    def get_position(self):
        return self.position

    # Track and update the current line
    def add_to_current_line(self, point):
        self.current_line.append(point)

    # Clear current line
    def reset_current_line(self):
        self.current_line = []

    # Return current line
    def get_current_line(self):
        return self.current_line

    # Add line to the stack
    def add_line(self):
        if self.current_line:
            self.undo_stack.append((self.current_line.copy(), self.color))
            self.redo_stack.clear()
            self.reset_current_line()

    # Pop line from undo stack and push line onto redo stack
    def undo(self):
        if self.undo_stack:
            line = self.undo_stack.pop()
            self.redo_stack.append(line)
            logger.info(f"{self.user_id} performed undo")
            return True
        logger.info(f"{self.user_id} undo stack empty")
        return False

    # Pop line from redo stack and push line onto redo stack
    def redo(self):
        if self.redo_stack:
            line = self.redo_stack.pop()
            self.undo_stack.append(line)
            logger.info(f"{self.user_id} performed redo")
            return True
        logger.info(f"{self.user_id} redo stack empty")
        return False

    # Return undo stack
    def get_undo_stack(self):
        return self.undo_stack if self.undo_stack else None

    # Return redo stack
    def get_redo_stack(self):
        return self.redo_stack if self.redo_stack else None

    # Remove and split the line
    def remove_point(self, pos):
        temp_stack = []
        for line, color in self.undo_stack or []:
            segments = []
            current_segment = []
            for point in line:
                if (pos[0] - point[0]) ** 2 + (pos[1] - point[1]) ** 2 >= 10 ** 2:
                    current_segment.append(point)
                else:
                    if len(current_segment) >= 2:
                        segments.append(current_segment)
                    current_segment = []
            if len(current_segment) >= 2:
                segments.append(current_segment)
            for segment in segments:
                temp_stack.append((segment, color))
        self.undo_stack = temp_stack

    # Clear the device stacks
    def clear(self):
        self.undo_stack = []
        self.redo_stack = []
        logger.info(f"{self.user_id} cleared canvas")

    # Set the device color
    def set_color(self, color):
        self.color = color
        logger.info(f"{self.user_id} changed color to {color}")

    # Return the device color
    def get_color(self):
        return self.color

    # Set the device tool
    def set_tool(self, tool):
        self.tool = tool
        logger.info(f"{self.user_id} changed tool to {tool}")

    # Return the device tool
    def get_tool(self):
        return self.tool

    # Set the device size
    def set_size(self, size):
        self.size = size

    # Return the device size
    def get_size(self):
        return self.size

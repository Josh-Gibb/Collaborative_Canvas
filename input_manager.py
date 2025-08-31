import threading
from logging_manager import logger
from device import Device


class InputManager:
    def __init__(self, screen_width, screen_height):
        self.inputs = {}
        self.lock = threading.Lock()
        self.screen_width = screen_width
        self.screen_height = screen_height

    # Pair a device, and add it to the input
    def pair_device(self, device_id, name, user_id):
        with self.lock:
            logger.info(f"Attempting to pair Device {device_id} with user {user_id} and name {name}")
            if device_id not in self.inputs:
                self.inputs[device_id] = Device(device_id, name, user_id, (self.screen_width // 2, self.screen_height // 2))
                logger.info(f"Successfully paired Device {name} with user {user_id}")
                return True
            else:
                logger.warning(f"Device {name} already in use")
                return False

    def is_admin(self, device_id):
        if device_id in self.inputs:
            return self.inputs[device_id].is_admin()

    # Unpair a device, and remove it from the input
    def unpair_device(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                del self.inputs[device_id]
                logger.info(f"{device_id} unpaired")
                return True
            else:
                logger.warning(f"{device_id} was not paired")
                return False

    # Set a device position
    def set_position(self, device_id, position):
        position = (
            max(0, min(self.screen_width, position[0])),
            max(10, min(self.screen_height - 10, position[1]))
        )
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].set_position(position)

    # Return a device from the input list 
    def get_device(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id]
            return None

    # Return the input position
    def get_position(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id].get_position()
            return (self.screen_width // 2, self.screen_height // 2)

    # Add a line to the input memory
    def add_line(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].add_line()

    # Erase points from a line
    def erase(self, device_id, pos):
        with self.lock:
            if device_id in self.inputs:
                if(self.is_admin(device_id)):
                    for dev in self.inputs:
                        self.inputs[dev].remove_point(pos)
                self.inputs[device_id].remove_point(pos)

    # Undo the last line from an input
    def undo(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                if self.inputs[device_id].undo():
                    return self.inputs[device_id].get_undo_stack()
            return None

    # Redo a line that was removed from an input
    def redo(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                if self.inputs[device_id].redo():
                    return self.inputs[device_id].get_undo_stack()
            return None

    # A method to clear an input
    def clear(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                if(self.is_admin(device_id)):
                    for dev in self.inputs:
                        self.inputs[dev].clear()
                self.inputs[device_id].clear()

    # Set the input's color
    def set_color(self, device_id, color):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].set_color(color)

    # Get the a device color
    def get_color(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id].get_color()
            return None

    # Set the device's color
    def set_tool(self, device_id, tool):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].set_tool(tool)

    # Get the device's color
    def get_tool(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id].get_tool()
            return None

    # Set the device's drawing size
    def set_size(self, device_id, size):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].set_size(size)

    # Get the device's drawing size
    def get_size(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id].get_size()
            return None

    # Return an inputs current line
    def get_current_line(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                return self.inputs[device_id].get_current_line()
            return None

    # Add a point to the current line
    def add_to_current_line(self, device_id, point):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].add_to_current_line(point)

    # Resets the current line
    def clear_current_line(self, device_id):
        with self.lock:
            if device_id in self.inputs:
                self.inputs[device_id].reset_current_line()

    # Return all inputs
    def get_active_inputs(self):
        with self.lock:
            return list(self.inputs.keys())

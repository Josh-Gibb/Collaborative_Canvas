import threading
import pygame
from evdev import InputDevice, ecodes, list_devices
from logging_manager import logger
from input_manager import InputManager
from canvas import Canvas
from header_manager import HeaderManager

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Canvas")
pygame.mouse.set_visible(False)

HEADER_HEIGHT = 100
COLORS = ((255, 0, 0), (0, 255, 0), (0, 0, 255),(255, 255, 0), (255, 0, 255), (0, 255, 255))

# Create surfaces for the header and the canvas
canvas_surface = pygame.Surface((WIDTH, HEIGHT - HEADER_HEIGHT))
canvas_surface.fill((255, 255, 255))
header_surface = pygame.Surface((WIDTH, HEADER_HEIGHT))
header_surface.fill((200, 200, 200))

# Instantiate manager classes
input_manager = InputManager(WIDTH, HEIGHT)
canvas = Canvas(canvas_surface, input_manager, header_height=HEADER_HEIGHT)
header_manager = HeaderManager(header_surface,COLORS)

draw_lock = threading.Lock()
stop_threads = threading.Event()

# A method to find all devices
def find_device_paths(device_names):
    device_paths = {}
    for path in list_devices():
        device = InputDevice(path)
        if device.name in device_names and device.name not in device_paths:
            device_paths[device.name] = path
    return list(device_paths.values())

# A method to handle each device
def handle_device(device_path, name, stop_event):
    thread_name = threading.current_thread().name
    if not input_manager.pair_device(device_path, name, thread_name):
        logger.error(f"Failed to pair device {device_path}")
        return

    try:
        inputs = InputDevice(device_path)
        x, y = input_manager.get_position(device_path)
        button_pressed = False

        for event in inputs.read_loop():
            if stop_event.is_set():
                break

            if event.type == ecodes.EV_KEY and event.code == ecodes.BTN_LEFT:
                if not button_pressed:  
                    if y < HEADER_HEIGHT:
                        pygame.event.post(pygame.event.Event(
                            pygame.USEREVENT, 
                            {"pos": (x, y), "device_path": device_path}
                        ))
                button_pressed = (event.value == 1)
                if not button_pressed:
                    current_line = input_manager.get_current_line(device_path)
                    if current_line:
                        with draw_lock:
                            input_manager.add_line(device_path)
                            input_manager.clear_current_line(device_path)
                continue

            if event.type == ecodes.EV_REL:
                if event.code == ecodes.REL_X:
                    if button_pressed:
                        x += max(-7, min(7, event.value))
                    else:
                        x += event.value
                elif event.code == ecodes.REL_Y:
                    if button_pressed:
                        y += max(-7, min(7, event.value))
                    else:
                        y += event.value

                x = max(0, min(WIDTH, x))
                y = max(0, min(HEIGHT, y))

                with draw_lock:
                    input_manager.set_position(device_path, (x, y))

                if button_pressed and y >= HEADER_HEIGHT:
                    current_tool = input_manager.get_tool(device_path)
                    if current_tool == 'Eraser':
                        with draw_lock:
                            input_manager.erase(device_path, (x, y))
                    else:
                        input_manager.add_to_current_line(device_path, (x, y))

    finally:
        input_manager.unpair_device(device_path)

def main():
    device_names = ['ImExPS/2 Generic Explorer Mouse', 'Lenovo Bluetooth Mouse', 'Microsoft Arc Mouse']
    device_paths = find_device_paths(device_names)
    threads = []

    # Start one thread per input device
    for path, name in zip(device_paths, device_names):
        thread = threading.Thread(target=handle_device, args=(path, name, stop_threads))
        thread.start()
        threads.append(thread)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                stop_threads.set()
            elif event.type == pygame.USEREVENT:
                logger.info(f"Header click event received at {event.pos} from {event.device_path}")
                header_manager.handle_click(event.pos, event.device_path, input_manager)

        # Lock and refresh the canvas once per frame
        with draw_lock:
            canvas.refresh()

            screen.blit(canvas_surface, (0, HEADER_HEIGHT))

            # Draw the header
            header_surface.fill((200, 200, 200))
            header_manager.draw()

            # Updates the button if an input is hovering over the button
            device_positions = [input_manager.get_position(device) for device in device_paths]
            header_manager.draw_buttons(device_positions)

            screen.blit(header_surface, (0, 0))

            # Drawing cursor for each device
            for device_path in device_paths:
                x, y = input_manager.get_position(device_path)
                pygame.draw.rect(screen, (0, 0, 0), (x - 10, y - 10, 20, 20), 2)
                pygame.draw.rect(screen, (255, 255, 255), (x - 9, y - 9, 18, 18))

        pygame.display.flip()
        clock.tick(60)

    for thread in threads:
        thread.join()

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame

# Initialize pygame and joystick modules
pygame.init()
pygame.joystick.init()

# Ensure at least one joystick is connected
if pygame.joystick.get_count() == 0:
    print("No controller detected.")
    exit()

# Use the first connected joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to: {joystick.get_name()}")

# Total buttons, axes, and hats
num_buttons = joystick.get_numbuttons()
num_axes = joystick.get_numaxes()
num_hats = joystick.get_numhats()
num_balls = joystick.get_numballs()
print("Controller details:")
print(f"Buttons: {num_buttons}, Axes: {num_axes}, Hats: {num_hats}, Balls: {num_balls}, Name: {joystick.get_name()}, ID: {joystick.get_id()}")

# Run the main input loop
print("Listening for button presses... (Ctrl+C to quit)")
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.1:
                    print(f"Axis {event.axis} moved: {event.value:.2f}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Hat {event.hat} moved: {event.value}")
except KeyboardInterrupt:
    print("Exiting.")
    joystick.quit()
    pygame.quit()



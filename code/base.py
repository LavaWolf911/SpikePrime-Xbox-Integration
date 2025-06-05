__author__ = "Connor Schwartz"

from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.tools import wait
from pybricks.parameters import Direction, Port
from pybricks.hubs import PrimeHub

# Deadzone threshold for joystick input
THRESBRAKE = 0.01

def deadzone(value: float) -> float:
    """Returns 0 if abs(value) is less than THRESBRAKE, else returns value."""
    return value if abs(value) >= THRESBRAKE else 0.0

# Clamp range for motor speeds
CLAMP_MIN = -500.0
CLAMP_MAX = 500.0

# Speed multipliers for drive, claw, and optional motors
MAX_SPEED = 10          # Drive motors (1-10, scaled to 100-1000 deg/s)
MAX_CLAW_SPEED = 10     # Claw motor (1-10, scaled to 100-1000 deg/s)
MAX_OPTIONAL_SPEED = 10 # Optional motor (1-10, scaled to 100-1000 deg/s)

def clamp(value: float) -> float:
    """Clamp value between CLAMP_MIN and CLAMP_MAX."""
    return max(CLAMP_MIN, min(CLAMP_MAX, value))

class Robot:
    """
    Main robot class for controlling drive, claw, and optional motors
    using an Xbox controller.
    """
    def __init__(self):
        # Initialize hub and controller
        self.hub = PrimeHub()
        self.op = XboxController()

        # Drive motors on Port A (left) and Port B (right)
        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)

        # Claw motor on Port C
        self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)

        # Optional motor on Port D (if present)
        try:
            self.optional_motor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False

        # Rumble feedback to confirm initialization
        self.op.rumble(200, 200, 2, 200)

    def drive(self, leftSpeed, rightSpeed):
        """Drive the robot with specified left and right motor speeds."""
        self.leftDrive.run(leftSpeed)
        self.rightDrive.run(rightSpeed)

    def run(self):
        """Main control loop for reading controller input and driving motors."""
        while True:
            # Get joystick inputs (scaled to -100 to 100)
            # leftX = clamp(deadzone(self.op.joystick_left()[0]) * MAX_SPEED)
            leftY = clamp(deadzone(self.op.joystick_left()[1]) * MAX_SPEED)
            rightX = clamp(deadzone(self.op.joystick_right()[0]) * MAX_SPEED)
            # rightY = clamp(deadzone(self.op.joystick_right()[1]) * MAX_SPEED)

            # === Arcade Drive ===
            # Left stick Y controls forward/backward
            # Right stick X controls turning
            leftSpeed = leftY + rightX
            rightSpeed = leftY - rightX

            # --- Optional: Inverted Directions ---
            # Invert both drive directions
            # leftSpeed = -(leftY + rightX)
            # rightSpeed = -(leftY - rightX)

            # Invert only forward/backward
            # leftSpeed = (-leftY) + rightX
            # rightSpeed = (-leftY) - rightX

            # Invert only turning direction
            # leftSpeed = leftY - rightX
            # rightSpeed = leftY + rightX

            # --- Optional: Tank Drive ---
            # Each joystick Y controls its own motor
            # leftSpeed = leftY
            # rightSpeed = rightY

            # Inverted tank controls
            # leftSpeed = -leftY
            # rightSpeed = -rightY

            # Claw motor control using triggers
            if self.claw_motor.stalled():
                self.op.rumble(100, 20, delay=1)
            if self.op.triggers()[0] != 0:
                self.claw_motor.run(self.op.triggers()[0] * MAX_CLAW_SPEED)
            elif self.op.triggers()[1] != 0:
                self.claw_motor.run(-self.op.triggers()[1] * MAX_CLAW_SPEED)
            else:
                self.claw_motor.run(0)
            # self.claw_motor.run(-self.op.triggers()[0])
            # self.claw_motor.run(self.op.triggers()[1])

            # Optional motor control using buttons
            if self.has4th_motor:
                if 'a' in self.op.buttons.pressed():
                    self.optional_motor.run(MAX_OPTIONAL_SPEED * 100)
                elif 'b' in self.op.buttons.pressed():
                    self.optional_motor.run(-MAX_OPTIONAL_SPEED * 100)
                else:
                    self.optional_motor.run(0)

            # Stop motors if no input, else drive
            if leftSpeed == 0 and rightSpeed == 0:
                self.leftDrive.run(0)
                self.rightDrive.run(0)
            else:
                self.drive(leftSpeed, rightSpeed)

            wait(20)  # Small delay to avoid busy loop

# Instantiate and run the robot if this file is executed directly
if __name__ == "__main__":
    bot = Robot()
    bot.run()

__author__ = "Connor Schwartz"

from pybricks.iodevices import XboxController
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.tools import wait
from pybricks.parameters import Direction, Port, Stop
from pybricks.hubs import PrimeHub

THRESBRAKE = 0.01  # Deadzone thresBRAKE for joystick input

def deadzone(value: float) -> float:
    """Returns 0 if abs(value) is less than thresBRAKE, else returns value."""
    return value if abs(value) >= THRESBRAKE else 0.0

CLAMP_MIN = -500.0
CLAMP_MAX = 500.0
""""
MAX_SPEED (int): Speed multiplier for drive motors. 
    Multiply joystick values by this to set the maximum speed in deg/s.
    Range: 1-10 (resulting in max speed of 100-1000 deg/s).
    # Set MAX_SPEED to control how fast the robot drives. 
    # For example, MAX_SPEED = 10 means joystick input is scaled up to 1000 deg/s.
"""
MAX_SPEED = 10  
# Speed multipliers for claw and optional motors (1-10, scaled to 100-1000 deg/s)
MAX_CLAW_SPEED = 10
MAX_OPTIONAL_SPEED = 10

def clamp(value: float) -> float:
    """Clamp value between CLAMP_MIN and CLAMP_MAX."""
    return max(CLAMP_MIN, min(CLAMP_MAX, value))

class Robot:
    def __init__(self):
        self.hub = PrimeHub()
        self.op = XboxController()

        # Must have Drive motors on Port A and B
        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)

        # At least one claw motor on Port C
        self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)

        # Optional motor on port D
        try:
            self.optional_motor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False

        # Feedback to confirm init
        self.op.rumble(200, 200, 2, 200)

    def drive(self, leftSpeed, rightSpeed):
        """Drive the robot with specified speed and turn rate."""
        self.leftDrive.run(leftSpeed)
        self.rightDrive.run(rightSpeed)

    def run(self):
        while True:
            
            # Get joystick inputs (scaled to -100 to 100)
            # If not used comment out the joystick lines for efficiency
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
            if self.claw_motor.stalled():
                self.op.rumble(100, 20, delay=1)
            if self.op.triggers()[0] != 0:
                self.claw_motor.run(self.op.triggers()[0]*MAX_CLAW_SPEED)
            elif self.op.triggers()[1] != 0:
                self.claw_motor.run(-self.op.triggers()[1]*MAX_CLAW_SPEED)
            else:
                self.claw_motor.run(0)
            # self.claw_motor.run(-self.op.triggers()[0])
            # self.claw_motor.run(self.op.triggers()[1])
            if self.has4th_motor:
                if 'a' in self.op.buttons.pressed():
                    self.optional_motor.run(MAX_OPTIONAL_SPEED*100)
                elif 'b' in self.op.buttons.pressed():
                    self.optional_motor.run(-MAX_OPTIONAL_SPEED*100)
                else:
                    self.optional_motor.run(0)
            if leftSpeed == 0 and rightSpeed == 0:
                self.leftDrive.run(0)
                self.rightDrive.run(0)
            else:
                self.drive(leftSpeed, rightSpeed)
            wait(20)  # Small delay to avoid busy loop


# Example of instantiating and running
if __name__ == "__main__":
    bot = Robot()
    bot.run()

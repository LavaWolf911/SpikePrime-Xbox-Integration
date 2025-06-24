__author__ = "Connor Schwartz"
from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Direction, Port, Button
from pybricks.tools import wait
# Constants
THRESHOLD = 1
CLAMP_MIN = -100.0
CLAMP_MAX = 100.0
MAX_CLAW_SPEED = 100
MAX_OPTIONAL_SPEED = 100
def deadzone(value):
    return value if abs(value) >= THRESHOLD else 0.0
def clamp(value):
    return max(CLAMP_MIN, min(CLAMP_MAX, value))
class Robot:
    def __init__(self):
        self.hub = PrimeHub()
        while True:
            try:
                self.op = XboxController()
                break
            except Exception as e:
                print(f"Error initializing XboxController: {e}")
                wait(500)
        try: 
            self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        except Exception as e:
            print(f"Error initializing left drive motor: {e}")
        try: 
            self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)
        except Exception as e:
            print(f"Error initializing right drive motor: {e}")
        try:
            self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)
        except Exception as e:
            print(f"Error initializing claw motor: {e}")
        self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)
        try:
            self.optional_motor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False
        self.op.rumble(100, 200, 2, 100)
    def run(self):
        while True:
            self.runReg()
            wait(1)
    def runReg(self):
        # === Joystick Handling ===
        leftY = clamp(deadzone(self.op.joystick_left()[1]) * 1.0)
        rightX = clamp(deadzone(self.op.joystick_right()[0]) * 1.0)
        leftSpeed = (leftY + rightX)
        rightSpeed = (leftY - rightX)
        if leftSpeed == 0:
            self.leftDrive.brake()
            self.rightDrive.dc(rightSpeed)
        elif rightSpeed == 0:
            self.rightDrive.brake()
            self.leftDrive.dc(leftSpeed)
        elif leftSpeed == 0 and rightSpeed == 0:
            self.leftDrive.brake()
            self.rightDrive.brake()
        else:
            self.rightDrive.dc(rightSpeed)
            self.leftDrive.dc(leftSpeed)
        # === Trigger & Button Handling ===
        lt, rt = self.op.triggers()
        if lt != 0:
            self.claw_motor.dc(MAX_CLAW_SPEED)
        elif rt != 0:
            self.claw_motor.dc(MAX_CLAW_SPEED)
        else:
            self.claw_motor.brake()
        if self.has4th_motor:
            if Button.LB in self.op.buttons.pressed():
                self.optional_motor.dc(100)
            elif Button.RB in self.op.buttons.pressed():
                self.optional_motor.dc(-100)
            else:
                self.optional_motor.brake()
if __name__ == "__main__":
    bot = Robot()
    bot.run()
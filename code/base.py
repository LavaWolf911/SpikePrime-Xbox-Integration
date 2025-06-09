__author__ = "Connor Schwartz"

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Direction, Port, Button
from pybricks.tools import wait

# Constants
THRESBRAKE = 0.01
CLAMP_MIN = -1000.0
CLAMP_MAX = 1000.0

MAX_SPEED = 10
MAX_CLAW_SPEED = 5
MAX_OPTIONAL_SPEED = 5

def deadzone(value):
    return value if abs(value) >= THRESBRAKE else 0.0

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

        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)
        self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)

        try:
            self.optional_motor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False
        self.op.rumble(100, 200, 2, 100)

    def drive(self, leftSpeed, rightSpeed):
        self.leftDrive.run(leftSpeed)
        self.rightDrive.run(rightSpeed)


    def run(self):
        while True:
            self.runReg()
            wait(1)

    def runReg(self):
        # === Joystick Handling ===
        leftY = clamp(deadzone(self.op.joystick_left()[1]) * MAX_SPEED)
        rightX = clamp(deadzone(self.op.joystick_right()[0]) * MAX_SPEED)

        leftSpeed = leftY + rightX
        rightSpeed = leftY - rightX

        if leftSpeed == 0 and rightSpeed == 0:
            # self.leftDrive.run(0)
            # self.rightDrive.run(0)
            self.leftDrive.brake()
            self.rightDrive.brake()
        else:
            self.drive(leftSpeed, rightSpeed)

        # === Trigger & Button Handling ===
        lt, rt = self.op.triggers()
        if lt != 0:
            self.claw_motor.run(100 * MAX_CLAW_SPEED)
        elif rt != 0:
            self.claw_motor.run(-100 * MAX_CLAW_SPEED)
        else:
            # self.claw_motor.run(0)
            self.claw_motor.brake()

        if self.has4th_motor:
            if Button.LB in self.op.buttons.pressed():
                self.optional_motor.run(100 * MAX_OPTIONAL_SPEED)
            elif Button.RB in self.op.buttons.pressed():
                self.optional_motor.run(-100 * MAX_OPTIONAL_SPEED)
            else:
                self.optional_motor.run(0)

if __name__ == "__main__":
    bot = Robot()
    bot.run()

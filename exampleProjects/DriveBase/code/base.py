__author__ = "Connor Schwartz"
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.tools import wait
from pybricks.parameters import Direction, Port
from pybricks.hubs import PrimeHub
THRESHOLD = 1
def deadzone(value: float) -> float:
    return value if abs(value) >= THRESHOLD else 0.0
CLAMP_MIN = -100.0
CLAMP_MAX = 100.0
MAX_OPTIONAL_SPEED = 100
def clamp(value: float) -> float:
    return max(CLAMP_MIN, min(CLAMP_MAX, value))
class Robot:
    def __init__(self):
        self.hub = PrimeHub()
        while True:
            try: 
                self.op = XboxController()
                break
            except Exception:
                print("Waiting for Xbox controller...")
                wait(200) 
        try:
            self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        except Exception:
            print("Left motor not connected on Port A. Please check your setup.")
            raise
        try:
            self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)
        except Exception:
            print("Right motor not connected on Port B. Please check your setup.")
            raise
        try:
            self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)
        except Exception:
            print("Claw motor not connected on Port C. Please check your setup.")
            raise
        try:
            self.optional_motor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False  
        self.op.rumble(200, 200, 2, 200)
    def drive(self, leftSpeed, rightSpeed):
        if leftSpeed == 0 and rightSpeed == 0:
            self.leftDrive.brake()
            self.rightDrive.brake()
        elif leftSpeed == 0 and rightSpeed != 0:
            self.leftDrive.brake()
            self.rightDrive.dc(rightSpeed)
        elif leftSpeed != 0 and rightSpeed == 0:
            self.leftDrive.dc(leftSpeed)
            self.rightDrive.brake()
        else:
            self.leftDrive.dc(leftSpeed)
            self.rightDrive.dc(rightSpeed)
    def run(self):
        while True:
            leftY = clamp(deadzone(self.op.joystick_left()[1]))
            rightX = clamp(deadzone(self.op.joystick_right()[0]))
            leftSpeed = leftY + rightX
            rightSpeed = leftY - rightX
            if self.op.triggers()[0] != 0:
                self.claw_motor.dc(self.op.triggers()[0])
            elif self.op.triggers()[1] != 0:
                self.claw_motor.dc(-self.op.triggers()[1])
            else:
                self.claw_motor.brake()
            if self.has4th_motor:
                if 'rb' in self.op.buttons.pressed():
                    self.optional_motor.dc(MAX_OPTIONAL_SPEED)
                elif 'lb' in self.op.buttons.pressed():
                    self.optional_motor.dc(-MAX_OPTIONAL_SPEED)
                else:
                    self.optional_motor.brake()
            self.drive(leftSpeed, rightSpeed)
            wait(20)
if __name__ == "__main__":
    bot = Robot()
    bot.run()
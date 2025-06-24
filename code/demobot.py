__author__ = "Connor Schwartz"

from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Direction, Port, Button
from pybricks.tools import wait

# Constants
THRESHOLD = 0.01
CLAMP_MIN = -100.0
CLAMP_MAX = 100.0

MAX_SPEED = 100
MAX_CLAW_SPEED = 100
MAX_OPTIONAL_SPEED = 100

def deadzone(value):
    return value if abs(value) > THRESHOLD else 0

def clamp(value):
    return max(CLAMP_MIN, min(CLAMP_MAX, value))

class Robot:
    def __init__(self):
        self.lowerWristLimit = -2000
        self.upperWristLimit = 2000
        self.hub = PrimeHub()
        while True:
            try:
                self.op = XboxController()
                break
            except Exception as e:
                print(f"Error initializing XboxController: {e}")
                if e.args[0] == "Unknown":
                    print("Turn off bluetooth on pc")
                wait(500)

        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B, Direction.CLOCKWISE)
        self.claw_motor = Motor(Port.C, Direction.CLOCKWISE)

        try:
            self.wristMotor = Motor(Port.D, Direction.CLOCKWISE)
            self.has4th_motor = True
        except Exception:
            self.has4th_motor = False

        self.op.rumble(200, 200, 2, 200)

    def runFlipped(self):
        # === Joystick Handling ===
        leftY = clamp(deadzone(self.op.joystick_left()[1]) * 1.0)
        rightX = clamp(deadzone(self.op.joystick_right()[0]) * 1.0)

        leftSpeed = -(leftY - rightX)
        rightSpeed = -(leftY + rightX)

        if leftSpeed == 0 and rightSpeed != 0:
            self.leftDrive.brake()
        elif rightSpeed == 0 and leftSpeed != 0:
            self.rightDrive.brake()
        elif leftSpeed == 0 and rightSpeed == 0:
            self.leftDrive.brake()
            self.rightDrive.brake()
        else:
            self.leftDrive.dc(leftSpeed)
            self.rightDrive.dc(rightSpeed)

        # === Trigger & Button Handling ===
        lt, rt = self.op.triggers()
        if rt != 0:
            self.claw_motor.run(100 * MAX_CLAW_SPEED)
        elif lt != 0:
            self.claw_motor.run(-100 * MAX_CLAW_SPEED)
        else:
            self.claw_motor.brake()
            self.wristAngle = self.wristMotor.angle()
        if Button.A in self.op.buttons.pressed():
            print(f"Wrist angle: {self.wristAngle}")
            print(f"High limit: {self.upperWristLimit}")
            print(f"Low limit: {self.lowerWristLimit}")

        if Button.DOWN in self.op.buttons.pressed():
            self.upperWristLimit = self.wristMotor.angle()
        if Button.UP in self.op.buttons.pressed():
            self.lowerWristLimit = self.wristMotor.angle()
        if Button.Y in self.op.buttons.pressed():
            self.upperWristLimit = 2000
            self.lowerWristLimit = -2000

        if self.has4th_motor:
            if Button.LB in self.op.buttons.pressed():
                if self.wristAngle > self.lowerWristLimit:
                    self.wristMotor.run(-100 * MAX_OPTIONAL_SPEED)
                else:
                    self.op.rumble(100, 100, 1, 200)
                    self.wristMotor.brake()
            elif Button.RB in self.op.buttons.pressed():
                if self.wristAngle < self.upperWristLimit:
                    self.wristMotor.run(100 * MAX_OPTIONAL_SPEED)
                else:
                    self.op.rumble(100, 100, 1, 200)
                    self.wristMotor.brake()
            else:
                self.wristMotor.brake()

    def run(self):
        while True:
            self.roll = self.hub.imu.tilt()[1]
            flipped = self.roll < -90 or self.roll > 90
            if flipped:
                self.runFlipped()
            else:
                self.runReg()

    def runReg(self):
        # === Joystick Handling ===
        leftY = clamp(deadzone(self.op.joystick_left()[1]) * 1.0)
        rightX = clamp(deadzone(self.op.joystick_right()[0]) * 1.0)

        leftSpeed = leftY + rightX
        rightSpeed = leftY - rightX

        if leftSpeed == 0 and rightSpeed != 0:
            self.leftDrive.brake()
        elif rightSpeed == 0 and leftSpeed != 0:
            self.rightDrive.brake()
        elif leftSpeed == 0 and rightSpeed == 0:
            self.leftDrive.brake()
            self.rightDrive.brake()
        else:
            self.leftDrive.dc(leftSpeed)
            self.rightDrive.dc(rightSpeed)

        # === Trigger & Button Handling ===
        lt, rt = self.op.triggers()
        if lt != 0:
            self.claw_motor.dc(-MAX_CLAW_SPEED)
        elif rt != 0:
            self.claw_motor.dc(MAX_CLAW_SPEED)
        else:
            self.claw_motor.brake()
        self.wristAngle = self.wristMotor.angle()
        if Button.A in self.op.buttons.pressed():
            print(f"Wrist angle: {self.wristAngle}")
            print(f"High limit: {self.upperWristLimit}")
            print(f"Low limit: {self.lowerWristLimit}")

        if Button.UP in self.op.buttons.pressed():
            self.upperWristLimit = self.wristMotor.angle()
        if Button.DOWN in self.op.buttons.pressed():
            self.lowerWristLimit = self.wristMotor.angle()
        if Button.Y in self.op.buttons.pressed():
            self.upperWristLimit = 2000
            self.lowerWristLimit = -2000
        if self.has4th_motor:
            if Button.RB in self.op.buttons.pressed():
                if self.wristAngle > self.lowerWristLimit:
                    self.wristMotor.dc(-MAX_OPTIONAL_SPEED)
                else:
                    self.op.rumble(100, 100, 1, 200)
                    self.wristMotor.brake()
            elif Button.LB in self.op.buttons.pressed():
                if self.wristAngle < self.upperWristLimit:
                    self.wristMotor.dc(MAX_OPTIONAL_SPEED)
                else:
                    self.op.rumble(100, 100, 1, 200)
                    self.wristMotor.brake()
            else:
                self.wristMotor.brake()

if __name__ == "__main__":
    bot = Robot()
    bot.run()

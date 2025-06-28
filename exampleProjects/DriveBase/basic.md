# Basic Drive Base Example

This example demonstrates how to control a LEGO Spike Prime robot using an Xbox controller with Python and the Pybricks library.

## Overview

The code connects an Xbox controller to the Spike Prime hub and maps joystick and button inputs to control two drive motors, a claw motor, and an optional fourth motor.

## Helper methods and Variables!

```python
THRESHOLD = 1
def deadzone(value: float) -> float:
    return value if abs(value) >= THRESHOLD else 0.0
CLAMP_MIN = -100.0
CLAMP_MAX = 100.0
MAX_OPTIONAL_SPEED = 100
def clamp(value: float) -> float:
    return max(CLAMP_MIN, min(CLAMP_MAX, value))
```
The following helper methods and variables are used throughout the code to simplify motor control and input handling:

- **Variables**
  - **THRESHOLD**: Minimum joystick movement required to register as input. Values below this are ignored to prevent accidental movement.
  - **CLAMP_MIN / CLAMP_MAX**: Define the minimum and maximum allowed motor speed values.
  - **MAX_OPTIONAL_SPEED**: Sets the maximum speed for the optional fourth motor.
- **Methods**
  - **deadzone(value)**: Returns the input value if it is outside the deadzone threshold; otherwise, returns 0. This helps filter out small, unintended joystick movements.</span>
  - **clamp(value)**: Restricts the input value to stay within the defined minimum and maximum speed limits.</span>

These helpers ensure that motor commands are safe, consistent, and responsive to user input.


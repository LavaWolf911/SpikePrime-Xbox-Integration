## Xbox Controller Pairing & Test Guide

Use this guide to pair a Bluetooth Xbox controller with your Spike Prime hub and verify it’s working using Pybricks.

---

### Step 1: Put Controller in Pairing Mode

1. Press and hold the **Xbox button** to turn the controller on.
2. Then press and hold the **pairing button** (small button between the bumpers) until the Xbox light flashes rapidly.

This puts the controller in pairing mode.

---

### Step 2: Pair via Python in Code.Pybricks

Pairing must be done through a Python script **run using** [Code.Pybricks](https://code.pybricks.com).

* A **solid Xbox light** means the controller is successfully paired.
* A flashing light means pairing failed.

---

### 🔄 Important Note: Re-Pairing Required

Each time you **run the Python program to connect the controller**, you will need to pair it again. The Xbox controller does **not** stay paired permanently with the Spike Prime hub — it must be paired fresh every time the program starts.

Make sure to run the pairing script through Code.Pybricks whenever you start a new session.

---

### Step 3: Confirm Pairing

* You can also use rumble to confirm:

```python
from pybricks.iodevices import XboxController
xbox = XboxController()
# If the controller rumbles, it is successfully connected; otherwise, it is not connected.
xbox.rumble(200, 200, 2, 200)
```

* This will cause two short rumbles.

---

### Running the Test

To run the test program:

1. Open [Code.Pybricks](https://code.pybricks.com) in Google Chrome.
2. Connect to your Spike Prime hub.
3. Paste the script or upload a `.py` file.
4. Click **Run**.

If the controller rumbles and the light turns solid, you're good to go!

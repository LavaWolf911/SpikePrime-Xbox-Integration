# Spike Prime Setup Guide (for Pybricks)

This guide walks you through preparing your LEGO Spike Prime hub to run Pybricks firmware and connect with a Bluetooth Xbox controller.

---

### Step 1: Enter DFU Mode
To install Pybricks firmware, your Spike Prime hub must be in DFU mode:

1. **Turn off** the Spike Prime hub.
2. **Unplug** the USB cable if already connected.
3. **Hold the center Bluetooth button**, then plug the hub into your computer via USB.
4. Continue holding the button until:
   - The **center button flashes blue**
   - The **Bluetooth light flashes pink**

You are now in DFU mode and ready to flash the firmware.

---

### Step 2: Flash Pybricks Firmware
1. Open [Code.Pybricks](https://code.pybricks.com) in Google Chrome.
2. Follow the on-screen instructions to install the firmware (select your hub and upload).

> Note: On Windows, you may need to update the device driver manually using Device Manager:
> - Open Device Manager  
> - Find the **unidentified device** under **Other devices**  
> - Right-click and choose **Properties**  
> - Go to **Driver** tab → **Update Driver**  
> - Select **Browse my computer for drivers**  
> - Choose **Let me pick from a list of available drivers**  
> - Scroll to and select **Universal Serial Bus devices**  
> - Choose **WinUSB (WinUSB)**

---

### Step 3: Reconnect Hub for Coding
1. Turn off the hub (if still in DFU mode).
2. Unplug and plug it back in normally.
3. The hub will now appear as a Pybricks device in Code.Pybricks and is ready to run MicroPython code.

You're now ready to test pairing with your Xbox controller!

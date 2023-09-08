# serial2bluez

A small program that emulates a bluetooth keyboard and sends
data that it reads from a serial device.

## TODO

 - Read from serial device

## Setup

```
pip install dbus-python
```

bluetoothd must be started with `-P input` to disable the input plugin which would otherwise bind to port 17 which is needed for HID emulation

## Resources

 - https://github.com/Mqrius/BluePloverPi
 - https://pypi.org/project/PyBluez/
 - https://github.com/kcolford/hidclient
 - https://github.com/ArthurYidi/Bluetooth-Keyboard-Emulator
 - https://github.com/Alkaid-Benetnash/EmuBTHID
 - https://github.com/taoso/btk
 - https://github.com/pikvm/kvmd/tree/master/kvmd/plugins/hid/bt
# serial2bluez

A small program that emulates a bluetooth keyboard and sends
data that it reads from a serial device.

## TODO

 - Read from serial device

## Setup

```
pip install dbus-python pyserial
```

bluetoothd must be started with `-P input` to disable the input plugin which would otherwise bind to port 17 which is needed for HID emulation

## Deployment

```shell

# Set a reasonable hostname
sudo hostnamectl hostname serial2bluez-<insert installation name or id>

# Install dependencies
sudo apt install variocube-unit git bluez python3 python3-dbus python3-serial

# Clone repository into the home directory of the `variocube` user
git clone git@github.com:variocube/serial2bluez /home/variocube/serial2bluez

# Create the service file
sudo tee /etc/systemd/system/serial2bluez.service <<EOF
[Unit]
Description=Serial to Bluetooth HID bridge
After=bluetooth.target

[Service]
ExecStart=/home/variocube/serial2bluez/main.py

[Install]
WantedBy=multi-user.target
EOF

# Disable bluetoothd `input` module
sudo sed -i '/ExecStart=.*bluetoothd$/s/$/ -P input/' /lib/systemd/system/bluetooth.service

# Reload systemd config and (re-)start services
sudo systemctl daemon-reload
sudo systemctl restart bluetooth

```

## Resources

 - https://github.com/Mqrius/BluePloverPi
 - https://pypi.org/project/PyBluez/
 - https://github.com/kcolford/hidclient
 - https://github.com/ArthurYidi/Bluetooth-Keyboard-Emulator
 - https://github.com/Alkaid-Benetnash/EmuBTHID
 - https://github.com/taoso/btk
 - https://github.com/pikvm/kvmd/tree/master/kvmd/plugins/hid/bt
import dataclasses


@dataclasses.dataclass(frozen=True)
class Hid:
    protocol: int
    subclass: int
    report_length: int
    report_descriptor: bytes


def make_keyboard_hid(report_id: int) -> Hid:
    return Hid(
        protocol=1,  # Keyboard protocol
        subclass=1,  # Boot interface subclass

        report_length=8,

        report_descriptor=bytes([
            # Logitech descriptor. It's very similar to https://www.kernel.org/doc/Documentation/usb/gadget_hid.txt
            # Dumped using usbhid-dump; parsed using https://eleccelerator.com/usbdescreqparser

            # Keyboard
            0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
            0x09, 0x06,  # USAGE (Keyboard)
            0xA1, 0x01,  # COLLECTION (Application)

            # Report ID
            *([0x85, report_id]),

            # Modifiers
            0x05, 0x07,  # USAGE_PAGE (Keyboard)
            0x19, 0xE0,  # USAGE_MINIMUM (Keyboard LeftControl)
            0x29, 0xE7,  # USAGE_MAXIMUM (Keyboard Right GUI)
            0x15, 0x00,  # LOGICAL_MINIMUM (0)
            0x25, 0x01,  # LOGICAL_MAXIMUM (1)
            0x75, 0x01,  # REPORT_SIZE (1)
            0x95, 0x08,  # REPORT_COUNT (8)
            0x81, 0x02,  # INPUT (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)

            # Reserved byte
            0x95, 0x01,  # REPORT_COUNT (1)
            0x75, 0x08,  # REPORT_SIZE (8)
            0x81, 0x01,  # INPUT (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)

            # LEDs output
            0x95, 0x05,  # REPORT_COUNT (5)
            0x75, 0x01,  # REPORT_SIZE (1)
            0x05, 0x08,  # USAGE_PAGE (LEDs)
            0x19, 0x01,  # USAGE_MINIMUM (Num Lock)
            0x29, 0x05,  # USAGE_MAXIMUM (Kana)
            0x91, 0x02,  # OUTPUT (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)

            # Reserved 3 bits in output
            0x95, 0x01,  # REPORT_COUNT (1)
            0x75, 0x03,  # REPORT_SIZE (3)
            0x91, 0x01,  # OUTPUT (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)

            # 6 keys
            0x95, 0x06,  # REPORT_COUNT (6)
            0x75, 0x08,  # REPORT_SIZE (8)
            0x15, 0x00,  # LOGICAL_MINIMUM (0)
            0x26, 0xFF, 0x00,  # LOGICAL_MAXIMUM (0xFF)
            0x05, 0x07,  # USAGE_PAGE (Keyboard)
            0x19, 0x00,  # USAGE_MINIMUM (Reserved)
            0x2A, 0xFF, 0x00,  # USAGE_MAXIMUM (0xFF)
            0x81, 0x00,  # INPUT (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)

            0xC0,  # END_COLLECTION
        ]),
    )

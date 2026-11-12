# A-Pad firmware (KMK on CircuitPython) for the Seeed XIAO RP2040
#
# Install:
#   1. Flash CircuitPython to the XIAO RP2040.
#   2. Copy the `kmk` folder from https://github.com/KMKfw/kmk_firmware to CIRCUITPY.
#   3. From the CircuitPython library bundle, copy these into CIRCUITPY/lib:
#      neopixel.mpy, adafruit_displayio_ssd1306.mpy, adafruit_display_text/
#   4. Copy this file to CIRCUITPY as main.py.
#
# Pin map (from PCB/HackPad.kicad_pcb):
#   D0 = Col 0    D1 = Col 1    D2 = Col 2
#   D3 = Row 0    D6 = Row 1    D7 = Row 2
#   D4 = SDA      D5 = SCL      (OLED, I2C address 0x3C)
#   D8 = ENC_A    D9 = ENC_B    (EC11, common pin to GND)
#   D10 = LED data (8x SK6812 MINI-E in a chain)
#
# Physical layout (the "A") and matrix position of each key:
#
#              [SW2 R0C1]
#      [SW4 R0C0]       [SW6 R0C2]
#      [SW7 R1C0][SW8 R1C1][SW9 R1C2]
#      [SW10 R2C0]      [SW12 R2C1]   (encoder push = R2C2)

import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
try:
    from kmk.extensions.rgb import RGB, AnimationModes  # current KMK
except ImportError:
    from kmk.extensions.RGB import RGB, AnimationModes  # older KMK releases
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()

# ---------- Key matrix ----------
# Switch -> diode anode, diode cathode -> row, so current flows column to row.
keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D6, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ---------- Extensions ----------
keyboard.extensions.append(MediaKeys())

rgb = RGB(
    pixel_pin=board.D10,
    num_pixels=8,
    hue_default=170,
    sat_default=255,
    val_default=80,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
)
keyboard.extensions.append(rgb)

i2c_bus = busio.I2C(board.SCL, board.SDA)
oled = SSD1306(i2c=i2c_bus, device_address=0x3C)
display = Display(
    display=oled,
    width=128,
    height=32,
    entries=[
        TextEntry(text="A-Pad", x=64, y=0, x_anchor="M"),
        TextEntry(text="Vol: knob  Mute: push", x=64, y=20, x_anchor="M"),
    ],
)
keyboard.extensions.append(display)

# ---------- Rotary encoder ----------
encoder = EncoderHandler()
encoder.pins = ((board.D8, board.D9, None),)  # push button is in the matrix
encoder.map = [((KC.VOLD, KC.VOLU, KC.NO),)]  # (counter-clockwise, clockwise, push)
keyboard.modules.append(encoder)

# ---------- Keymap ----------
# Order is row by row: R0C0, R0C1, R0C2, R1C0, R1C1, R1C2, R2C0, R2C1, R2C2
COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
UNDO = KC.LCTL(KC.Z)
SAVE = KC.LCTL(KC.S)
REDO = KC.LCTL(KC.Y)

keyboard.keymap = [
    [
        COPY,      KC.MPLY,  PASTE,     # SW4 (left), SW2 (apex), SW6 (right)
        UNDO,      SAVE,     REDO,      # SW7, SW8, SW9 (crossbar)
        KC.MPRV,   KC.MNXT,  KC.MUTE,   # SW10, SW12, encoder push
    ],
]

if __name__ == "__main__":
    keyboard.go()

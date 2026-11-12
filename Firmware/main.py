# A-pad firmware (KMK / CircuitPython) for Seeed XIAO RP2040
# Matrix: 3 cols x 3 rows, diodes COL2ROW (cathode toward row)
import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()

# XIAO pin map taken from PCB/HackPad.kicad_pcb
keyboard.col_pins = (board.D0, board.D1, board.D2)   # Col 0, Col 1, Col 2
keyboard.row_pins = (board.D3, board.D6, board.D7)   # Row 0, Row 1, Row 2
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.extensions.append(MediaKeys())

# Rotary encoder (A=D8, B=D9; push switch is in the matrix)
encoder = EncoderHandler()
encoder.pins = ((board.D8, board.D9, None, False),)
encoder.map = [((KC.VOLD, KC.VOLU, KC.NO),)]
keyboard.modules.append(encoder)

# 8x SK6812 MINI-E on D10
rgb = RGB(pixel_pin=board.D10, num_pixels=8, hue_default=170, val_default=60,
          animation_mode=None)
keyboard.extensions.append(rgb)

# 0.91" SSD1306 OLED, I2C on D4 (SDA) / D5 (SCL)
i2c = busio.I2C(board.SCL, board.SDA)
display = Display(
    display=SSD1306(i2c=i2c, device_address=0x3C),
    width=128, height=32, brightness=0.8,
    entries=[TextEntry(text="A-pad", x=64, y=4, x_anchor="M"),
             TextEntry(text="KMK ready", x=64, y=18, x_anchor="M")],
)
keyboard.extensions.append(display)

# 9 matrix positions: 8 keys + encoder push button
keyboard.keymap = [[
    KC.ESC,  KC.MUTE,  KC.MPLY,
    KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.Z),
    KC.LCTL(KC.S), KC.RGB_TOG, KC.ENTER,
]]

if __name__ == "__main__":
    keyboard.go()

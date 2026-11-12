# A-pad Firmware (KMK)

1. Flash CircuitPython for the Seeed XIAO RP2040 (hold BOOT, plug in, drop the UF2).
2. Copy the `kmk` folder from https://github.com/KMKfw/kmk_firmware to the CIRCUITPY drive.
3. Copy `main.py` to the drive root.

| Function | XIAO pin |
|---|---|
| Col 0 / 1 / 2 | D0 / D1 / D2 |
| Row 0 / 1 / 2 | D3 / D6 / D7 |
| OLED SDA / SCL | D4 / D5 |
| Encoder A / B | D8 / D9 |
| SK6812 data | D10 |

Diodes: COL2ROW. Encoder push switch sits in the matrix (Col 2).

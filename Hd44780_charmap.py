from RPLCD import CharLCD
import time

# Adjust these parameters based on your actual wiring and LCD spec
lcd = CharLCD(cols=16, rows=4, pin_rs=15, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode='BCM', charmap='A00')

def dump_charmap():
    print("Dumping LCD charmap...\n")
    lcd.clear()
    for i in range(0, 256):
        row = i // 16
        col = i % 16
        lcd.cursor_pos = (row % 2, col)
        lcd.write_string(chr(i))
        time.sleep(0.01)
        if col == 15 and row % 2 == 1:
            time.sleep(1)
            lcd.clear()

dump_charmap()

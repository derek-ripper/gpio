from RPLCD.i2c import CharLCD
import time

# I2C configuration for PCF8574 at address 0x27
lcd = CharLCD(i2c_expander='PCF8574',
              address=0x27,
              port=1,
              cols=20,
              rows=4,
              charmap='A02',
              auto_linebreaks=False)

def dump_charmap():
    print("Dumping LCD charmap via I2C...\n")
    lcd.clear()
    for i in range(0, 256):
        row = i // 16
        col = i % 16
        lcd.cursor_pos = (row % 2, col)
        lcd.write_string(chr(i))
        time.sleep(.01)
        if col == 15 and row % 2 == 1:
            #time.sleep(10)
            input("C= "+str(col)+"R= "+str(row) + " Press anykey.....")
            lcd.clear()

dump_charmap()




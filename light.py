from machine import ADC, Pin
from time import sleep

lux_pwr = Pin(27, Pin.OUT)
lux_pwr.value(1)

lux = ADC(26)

while True:
    reading = lux.read_u16()
    print(reading)
    sleep(1)
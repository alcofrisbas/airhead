import RPi.GPIO as GPIO
import time
import smbus

GPIO.setmode(GPIO.BCM)
keys = [16,20,21]
states = [0 for i in keys]
right = False
left = False
rising = False
falling = False
fps = 0.1
flash_freq = 10
GPIO.setup(keys, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
count = 0

DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)




try:
    while True:
        count = count%flash_freq
        if count == 0:
            rising = True
            falling = False
            #print("rising")
        elif count == flash_freq /2:
            falling = True
            rising = False
            #print("falling")
        else:
            rising = falling = False
            #print("tick")
        
        for i, key in enumerate(keys):
            cur_state = GPIO.input(key)
            if key == 16:
                if cur_state != states[i]:
                    if cur_state:
                        if left or right:
                            left = right = False
                        else:
                            left = True
                states[i] = cur_state
                
            if key == 21:
                if cur_state != states[i]:
                    if cur_state:
                        if left or right:
                            left = right = False
                        else:
                            right = True
                states[i] = cur_state

        #if GPIO.input(16):
        #    print("16")
        #    if left:
        #        left = False
        #    elif right:
        #        right = False
        #    else:
        #        left = True
        #    print(left)
        #if GPIO.input(20):
        #    pass

        if rising:
            if left:
                bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
            elif right:
                bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)
        if falling:
            bus.write_byte_data(DEVICE_ADDR, 1, 0x00)
            bus.write_byte_data(DEVICE_ADDR, 2, 0x00)

        count += 1
        time.sleep(fps)
        
except KeyboardInterrupt:
    pass

GPIO.cleanup()
print()

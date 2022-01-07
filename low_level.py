import RPi.GPIO as GPIO

#--------------------------------EMBEEDED---------------------------------------

def init():
    """"Initialize GPIO pins and all devices"""
    global buzzer

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins_out.keys():
        GPIO.setup(pins_out[pin], GPIO.OUT)
    for button in buttons.keys():
        GPIO.setup(buttons[button], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # an input pin, set initial value to be pulled low (off)

    GPIO.add_event_detect(buttons["up"], GPIO.RISING, callback = on_click_button_up) # Setup event on rising edge
    GPIO.add_event_detect(buttons["down"], GPIO.RISING, callback = on_click_button_down)
    GPIO.add_event_detect(buttons["ok"], GPIO.RISING, callback = on_click_button_ok)

    buzzer = GPIO.PWM(pins_out["BUZZER"], 440)
    buzzer.start(50)


def play_tone(frequency):
    """Play tone on buzzer"""
    global buzzer
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)


def be_quiet():
    """Turn the buzzer off"""
    global buzzer
    buzzer.duty_u16(0)


def light_diode(addr: list):
    GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.HIGH)
    GPIO.output(pins_out["MAIN_MUX_X"], GPIO.HIGH)
    GPIO.output(pins_out["MAIN_MUX_ADDR_A"], addr[0])
    GPIO.output(pins_out["MAIN_MUX_ADDR_B"], addr[1])
    GPIO.output(pins_out["FIRST_MUX_ADDR_A"], addr[2])
    GPIO.output(pins_out["FIRST_MUX_ADDR_B"], addr[3])


def light_off():
    """Turn off all diodes"""

    GPIO.output(pins_out["MAIN_MUX_Y"], GPIO.LOW)
    GPIO.output(pins_out["MAIN_MUX_X"], GPIO.LOW)


def play_sound(note: str, beat = 0.01):
    """Play tone on the buzzer and light the diode for certain time"""
    light_diode(diodes[note])
    play_tone(sounds[note]) #TODO: play 2 sounds
    time.sleep(beat*0.13)
    be_quiet()
    light_off()


def show_text_lcd(text: str):
    print("ON LCD:", text)
    #TODO: show on LCD
    pass


def get_key():
    #TODO: check on gpio
    pass

# ----------------------------------- HELPFUL ----------------------------------

def on_click_button_up():
    global option_chosen
    option_chosen -= 1
    refresh_menu()


def on_click_button_down():
    global option_chosen
    option_chosen += 1
    refresh_menu()


def on_click_button_ok():
    if current_menu == 0:
        choose_option_main_menu()
    elif current_menu in (1,2):
        choose_option_songs_menu()


def check_keys():
    for key in piano_keys.keys():
        if get_key(key):
            return key
    return None
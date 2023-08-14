from machine import Pin, ADC, SPI, Timer
import utime, micropython
import time
from random import randint
from array import array
import _thread

# LCD Functions
def Configure():
    for i in range(4):
       L[i] = Pin(PORT[i], Pin.OUT)
    
def lcd_strobe():
    EN.value(1)
    utime.sleep_ms(1)
    EN.value(0)
    utime.sleep_ms(1)
    
def lcd_write(c, mode):
    if mode == 0:
       d = c
    else:
       d = ord(c)
    d = d >> 4
    for i in range(4):
        b = d & 1
        L[i].value(b)
        d = d >> 1
    RS.value(mode)
    lcd_strobe()
    
    if mode == 0:
       d = c
    else:
       d = ord(c)
    for i in range(4):
        b = d & 1
        L[i].value(b)
        d = d >> 1
    RS.value(mode)
    lcd_strobe()
    utime.sleep_ms(1)
    RS.value(1)

def lcd_clear():
    lcd_write(0x01, 0)
    utime.sleep_ms(5)

def lcd_home():
    lcd_write(0x02, 0)
    utime.sleep_ms(5)

def lcd_cursor_blink():
    lcd_write(0x0D, 0)
    utime.sleep_ms(1)

def lcd_cursor_on():
    lcd_write(0x0E, 0)
    utime.sleep_ms(1)

def lcd_cursor_off():
    lcd_write(0x0C, 0)
    utime.sleep_ms(1)

def lcd_puts(s):
    l = len(s)
    for i in range(l):
       lcd_putch(s[i])

def lcd_putch(c):
    lcd_write(c, 1)

def lcd_goto(col, row):
    c = col + 1
    if row == 0:
        address = 0
    if row == 1:
        address = 0x40
    if row == 2:
        address = 0x14
    if row == 3:
        address = 0x54
    address = address + c - 1
    lcd_write(0x80 | address, 0)

def lcd_init():
    Configure()
    utime.sleep_ms(120)
    for i in range(4):
        L[i].value(0)
    utime.sleep_ms(50)
    L[0].value(1)
    L[1].value(1)
    lcd_strobe()
    utime.sleep_ms(10)
    lcd_strobe()
    utime.sleep_ms(10)
    lcd_strobe()
    utime.sleep_ms(10)
    L[0].value(0)
    lcd_strobe()
    utime.sleep_ms(5)
    lcd_write(0x28, 0)
    utime.sleep_ms(1)
    lcd_write(0x08, 0)
    utime.sleep_ms(1)
    lcd_write(0x01, 0)
    utime.sleep_ms(10)
    lcd_write(0x06, 0)
    utime.sleep_ms(5)
    lcd_write(0x0C, 0)
    utime.sleep_ms(10)

# LCD Variables
EN = Pin(6, Pin.OUT)
RS = Pin(7, Pin.OUT)
D4 = Pin(10, Pin.OUT)
D5 = Pin(11, Pin.OUT)
D6 = Pin(12, Pin.OUT)
D7 = Pin(13, Pin.OUT)
PORT = [10,11,12,13]
L = [0,0,0,0]

# BUTTON INPUTS
yellow_push = Pin(17, Pin.IN, Pin.PULL_DOWN)
blue_push = Pin(20, Pin.IN, Pin.PULL_DOWN)
red_push = Pin(22, Pin.IN, Pin.PULL_DOWN)
green_push = Pin(5, Pin.IN, Pin.PULL_DOWN)

# INTERRUPT DEFAULT
last_time_y = 0
last_time_b = 0
last_time_r = 0
last_time_g = 0

# LED OUTPUTS
yellow_led = Pin(16, Pin.OUT)
blue_led = Pin(18, Pin.OUT)
red_led = Pin(21, Pin.OUT)
green_led = Pin(26, Pin.OUT)

# GAME DIFFICULTY SELECT
game_select = ADC(27)

# Speaker Outputs
BUZZER = Pin(15, Pin.OUT)
BUZZER_FREQ = 250
micropython.alloc_emergency_exception_buf(100)

# SPI Outputs
cs = Pin(9, Pin.OUT)
spi = machine.SPI(0,
                  baudrate=115200,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(0))

# Lookup Table
sine = [0x200,0x27f,0x2f6,0x35e,0x3af,0x3e6,0x3fe,0x3f6,0x3ce,0x38a,
0x32c,0x2bc,0x240,0x1bf,0x143,0xd3,0x75,0x31,0x9,0x1,
0x19,0x50,0xa1,0x109,0x180,0x200]

sawtooth = [0x28,0x50,0x78,0xa0,0xc9,0xf1,0x119,0x141,
0x169,0x191,0x1b9,0x1e1,0x20a,0x232,0x25a,0x282,
0x2aa,0x2d2,0x2fa,0x322,0x34a,0x373,0x39b,0x3c3,
0x3eb,0x3ff,]

triangle = [409,818,1023,818,409,0]

def ybutton(Source):
    global last_time_y, input_sequence, y_pushed
    
    new_time_y = utime.ticks_ms()
    if (new_time_y - last_time_y > 200):
        input_sequence.append(1)
        y_pushed = 1
        last_time_y = new_time_y
        
yellow_push.irq(handler=ybutton, trigger=Pin.IRQ_FALLING)

def bbutton(Source):
    global last_time_b, input_sequence, b_pushed
    
    new_time_b = utime.ticks_ms()
    
    if (new_time_b - last_time_b > 200):
        input_sequence.append(2)
        b_pushed = 1
        last_time_b = new_time_b
  
blue_push.irq(handler=bbutton, trigger=Pin.IRQ_FALLING)  
  
def rbutton(Source):
    global last_time_r, input_sequence, r_pushed
    
    new_time_r = utime.ticks_ms()
    
    if (new_time_r - last_time_r > 200):
        input_sequence.append(3)
        r_pushed = 1
        last_time_r = new_time_r
    
red_push.irq(handler=rbutton, trigger=Pin.IRQ_FALLING)

def gbutton(Source):
    global last_time_g, input_sequence, g_pushed
    
    new_time_g = utime.ticks_ms()
    
    if (new_time_g - last_time_g > 200):
        input_sequence.append(4)
        g_pushed = 1
        last_time_g = new_time_g
    
green_push.irq(handler=gbutton, trigger=Pin.IRQ_FALLING)

def game_mode_calculation():
    global game_select
    game_select_output = game_select.read_u16() * 5 / 65536
    if (game_select_output < 1.67):
        return "easy"
    elif (game_select_output < 3.34):
        return "medium"
    else:
        return "hard"
 
def reset_leds():
    yellow_led(0)
    blue_led(0)
    red_led(0)
    green_led(0)
    
 
def game_starting_screen():
    lcd_clear()
    utime.sleep_ms(100)
    lcd_puts("Welcome to Simon!")
    utime.sleep(5)
    
    lcd_clear()
    lcd_puts("Choose game mode                           difficulty")
    utime.sleep(5)
    
    count = 0
    lcd_clear()
    while(count < 5):
          game_mode = game_mode_calculation()
          output = f'Selected Game                           Mode: {game_mode}'
          lcd_puts(output)
          utime.sleep_ms(750)
          lcd_clear()
          count = count + 1
     
    lcd_puts("Starting Game!")
    utime.sleep_ms(100)
     
    while(count < 20):
        yellow_led(1)
        blue_led(1)
        red_led(1)
        green_led(1)
        utime.sleep_ms(125)
        yellow_led(0)
        blue_led(0)
        red_led(0)
        green_led(0)
        utime.sleep_ms(125)
        count = count + 1
        
 
def calculating_sequence():
     game_mode = game_mode_calculation()
     
     if (game_mode == "easy"): 
         sequence_l=[(randint(1,4)) for i in range(5)]
         sequence = array('i',[0])
         for i in sequence_l:
             sequence.append(i)
         return sequence
        
     if (game_mode == "medium"): 
         sequence_l=[(randint(1,4)) for i in range(10)]
         sequence = array('i',[0])
         for i in sequence_l:
             sequence.append(i)
         return sequence
        
     if (game_mode == "hard"): 
         sequence_l=[(randint(1,4)) for i in range(15)]
         sequence = array('i',[0])
         for i in sequence_l:
             sequence.append(i)
         return sequence
        
def print_sequence(sequence,index):
    
    if (index == 0):
        led = sequence[1]
        
        if (led == 1):
                yellow_led(1)
                yellow_sound()
                utime.sleep_ms(2000)
                yellow_led(0)
                
        elif (led == 2):
                blue_led(1)
                blue_sound()
                utime.sleep_ms(2000)
                blue_led(0)
                
        elif (led == 3):
                red_led(1)
                red_sound()
                utime.sleep_ms(2000)
                red_led(0)
                
        elif (led == 4):
                green_led(1)
                green_sound()
                utime.sleep_ms(2000)
                green_led(0)
                
        button = 0
                
    
    else:
            new_sequence = sequence[1:index+2]
            for i in range(index+1):
                led = new_sequence[i]
                
                if (led == 1):
                    yellow_led(1)
                    yellow_sound()
                    utime.sleep_ms(2000)
                    yellow_led(0)
                        
                elif (led == 2):
                    blue_led(1)
                    blue_sound()
                    utime.sleep_ms(2000)
                    blue_led(0)
                        
                elif (led == 3):
                    red_led(1)
                    red_sound()
                    utime.sleep_ms(2000)
                    red_led(0)
                        
                elif (led == 4):
                    green_led(1)
                    green_sound()
                    utime.sleep_ms(2000)
                    green_led(0)
                    
                reset_leds()
                utime.sleep_ms(250)
                    
    reset_leds()
    utime.sleep_ms(250)
    
def check_sequence(sequence,index):
     global input_sequence
     
     if (input_sequence == sequence[0:index+2]):
         return 1
     else:
         return 0
         
def flash_led(button):
    if (button == 1):
        yellow_led(1)
        utime.sleep(0.25)
        yellow_led(0)
        
    elif (button == 2):
        yellow_blue(1)
        utime.sleep(0.25)
        blue_led(0)
        
    elif (button == 3):
        red_led(1)
        utime.sleep(0.25)
        red_led(0)
        
    elif (button == 4):
        green_led(1)
        utime.sleep(0.25)
        green_led(0)
 
def yellow_sound():
    global triangle
    frequency = 75
    period = 1/frequency
    for j in range(10):
        for i in triangle:
            #shifting over 2 for dont cares
            temp = (i << 2) | 0x9000
            # HB=upper byte or control code
            HB = 0xFF00 & temp
            HB= HB >> 8
            # LB=low byte 
            LB = temp & 0xFF
            buf=bytearray([HB,LB])
            cs(0)
            spi.write(buf)
            cs(1)
            sleep=(period/6)
            utime.sleep_ms(int(sleep*1000))
        
def blue_sound():
    global triangle
    frequency = 100
    period = 1/frequency
    for j in range(10):
        for i in triangle:
            #shifting over 2 for dont cares
            temp = (i << 2) | 0x9000
            # HB=upper byte or control code
            HB = 0xFF00 & temp
            HB= HB >> 8
            # LB=low byte 
            LB = temp & 0xFF
            buf=bytearray([HB,LB])
            cs(0)
            spi.write(buf)
            cs(1)
            sleep=(period/6)
            utime.sleep_ms(int(sleep*1000))
        
def red_sound():
    global triangle
    frequency = 125
    period = 1/frequency
    for j in range(10):
        for i in triangle:
            #shifting over 2 for dont cares
            temp = (i << 2) | 0x9000
            # HB=upper byte or control code
            HB = 0xFF00 & temp
            HB= HB >> 8
            # LB=low byte 
            LB = temp & 0xFF
            buf=bytearray([HB,LB])
            cs(0)
            spi.write(buf)
            cs(1)
            sleep=(period/6)
            utime.sleep_ms(int(sleep*1000))
        
def green_sound():
    global triangle
    frequency = 350
    period = 1/frequency
    for j in range(10):
        for i in triangle:
            #shifting over 2 for dont cares
            temp = (i << 2) | 0x9000
            # HB=upper byte or control code
            HB = 0xFF00 & temp
            HB= HB >> 8
            # LB=low byte 
            LB = temp & 0xFF
            buf=bytearray([HB,LB])
            cs(0)
            spi.write(buf)
            cs(1)
            sleep=(period/6)
            utime.sleep_ms(int(sleep*1000))
 

lcd_init()
global y_pushed 
global b_pushed
global r_pushed
global g_pushed
y_pushed = 0
b_pushed = 0
r_pushed = 0
g_pushed = 0
while True :
            
    lose = 0
    game_starting_screen()
    sequence=calculating_sequence()
    print(sequence)
    
    game_mode=game_mode_calculation()
    if (game_mode == "easy"):
        length = 5
    elif (game_mode == "medium"):
        length = 10
    elif (game_mode == "hard"):
        length = 15
    count=0
    
    while (count < length):
        lcd_clear()
        utime.sleep_ms(100)
        output = f'Level: {count+1}'
        lcd_puts(output)
        utime.sleep(1)
        
        print_sequence(sequence,count)
        input_sequence = array('i',[0])
        
        wait_time = 2*(count+1) + 1*count
        #utime.sleep(wait_time)
        
        deadline = time.ticks_add(time.ticks_ms(), int(wait_time*1000))
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            if (y_pushed == 1):
                yellow_led(1)
                utime.sleep_ms(300)
                yellow_led(0)
                yellow_sound()
                y_pushed = 0
            elif (b_pushed == 1):
                blue_led(1)
                utime.sleep_ms(300)
                blue_led(0)
                blue_sound()
                b_pushed = 0
            elif (r_pushed == 1):
                red_led(1)
                utime.sleep_ms(300)
                red_led(0)
                red_sound()
                r_pushed = 0
            elif (g_pushed == 1):
                green_led(1)
                utime.sleep_ms(300)
                green_led(0)
                green_sound()
                g_pushed = 0
                
        print(input_sequence)
        print(sequence[0:count+2])
        
        y_pushed = 0
        b_pushed = 0
        r_pushed = 0
        g_pushed = 0
        
        
        is_sequence_true=check_sequence(sequence,count)
        if (is_sequence_true == 0) :
            lcd_clear()
            utime.sleep_ms(100)
            lcd_puts("Game Over!")
            utime.sleep(2)
            lcd_clear()
            lose = 1
            break
        count = count + 1
        
    if (lose == 0):
        lcd_clear()
        utime.sleep_ms(100)
        lcd_puts("You Win!")
        utime.sleep_ms(100)
            
        count = 0
        while(count < 10):
            
            yellow_led(1)
            utime.sleep_ms(150)
            yellow_led(0)
                
            blue_led(1)
            utime.sleep_ms(150)
            blue_led(0)
                
            red_led(1)
            utime.sleep_ms(150)
            red_led(0)
                
            green_led(1)
            utime.sleep_ms(150)
            green_led(0)
                
            count = count + 1
        
        
        for i in range(3):
            green_sound()
        for i in range(2):
            green_sound()
        for i in range(8):
            green_sound()
        for i in range(5):
            green_sound()


    
    
# Version 4
# Board: ItsyBitsy M0
# 1. Added proximity switch to indicate upper limit of
#    travel. Lower limit of travel is still indicated
#    by counting magnets via the hall effect sensor
# 2. Reversed count convention to count up as curtain lowers

import board
import digitalio
import pulseio
import time

# define I/O objects:
button_dn = digitalio.DigitalInOut(board.D9)
button_dn.direction = digitalio.Direction.INPUT
button_dn.pull = digitalio.Pull.UP

button_up = digitalio.DigitalInOut(board.D10)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

prox_sens = digitalio.DigitalInOut(board.D2)
prox_sens.direction = digitalio.Direction.INPUT
prox_sens.pull = digitalio.Pull.UP

hall_sens = digitalio.DigitalInOut(board.D12)
hall_sens.direction = digitalio.Direction.INPUT
hall_sens.pull = digitalio.Pull.UP

motor = pulseio.PWMOut(board.D13, frequency=50)

# define initial variables:
count = 0
count_max = 58
speed_up = 30
speed_dn = -27
on_cycle_time = .005
off_cycle_time = .1
speed_init = 7
motor_accel = 1.05

# define initial states:
new_mag = True
press_flag = False
count_dn_ok = False
count_up_ok = False
motor_up = False
motor_dn = False

# conversion of motor input to servo duty cycle:
def motor_duty_cycle(speed_percent, frequency=50):
    pulse_ms = speed_percent / 200 + 1.5
    duty_cycle = int((pulse_ms * frequency / 1000) * 65535)
    return duty_cycle

while True:
    # set initial conditions
    motor.duty_cycle = motor_duty_cycle(0)
    motor_speed = speed_init

    while True:
        # update counter check (counts up as curtain lowers)
        count_dn_ok = count < count_max  # check if exceeded lower limit

        # check proximity sensor
        curtain_dn = not prox_sens.value  # check if curtain is at top

        # check for button press
        up_press = not button_up.value
        dn_press = not button_dn.value

        # if button pressed, count good, and no flags:
        if up_press and curtain_dn and (not press_flag):
            press_flag = True  # set flag
            motor_up = True  # set state
            while motor_up:
                # slow start the motor
                if motor_speed < speed_up:
                    motor.duty_cycle = motor_duty_cycle(motor_speed)
                    motor_speed = motor_speed * motor_accel
                    if motor_speed > speed_up:
                        motor_speed = speed_up
                else:
                    motor.duty_cycle = motor_duty_cycle(motor_speed)
                print("entered motor_up", count)
                if (not hall_sens.value):  # check for magnet (active low)
                    if new_mag:  # one count per new magnet
                        count -= 1
                        new_mag = False  # clear new mag flag
                else:
                    new_mag = True  # if no magnet, reset flag

                if button_up.value:  # if button is not pressed (active low)
                    press_flag = False  # clear flag

                if (not press_flag):  # flag must be cleared
                    # if either button pressed, or proimity sensor triggered
                    # must perform direct query of i/o value inside while loop
                    if (not button_up.value) or (not button_dn.value) or prox_sens.value:
                        motor.duty_cycle = motor_duty_cycle(0)  # turn off motor
                        motor_speed = speed_init  # reset motor speed
                        motor_up = False  # reset state
                        press_flag = True  # set button flag
                        #  if proximity sensor was triggered, reset count
                        if prox_sens.value:
                            count = 0  # reset count
                            print("motor stopped, count reset")
                        print ("motor stopped, count=",count)
                time.sleep(on_cycle_time)

        if button_up.value and button_dn.value:  # if button is not pressed (active low)
            press_flag = False  # clear the flag

        # if button pressed, count good, and no flags:
        if dn_press and count_dn_ok and (not press_flag):
            press_flag = True
            motor_dn = True
            motor_speed = -speed_init
            while motor_dn:
                # slow start the motor
                if motor_speed > speed_dn:
                    motor.duty_cycle = motor_duty_cycle(motor_speed)
                    motor_speed = motor_speed * motor_accel
                    if motor_speed < speed_dn:
                        motor_speed = speed_dn
                else:
                    motor.duty_cycle = motor_duty_cycle(motor_speed)
                print("entered motor_dn", count)
                if (not hall_sens.value):  # check for magnet (active low)
                    if new_mag:  # one count per new magnet
                        count += 1  # count up as curtain lowers
                        new_mag = False
                else:
                    new_mag = True

                if button_dn.value:  # if button is pressed (active low)
                    press_flag = False  #  clear the flag

                if (not press_flag):  # flag must be cleared
                    if (not button_up.value) or (not button_dn.value) or (count >= count_max):
                        motor.duty_cycle = motor_duty_cycle(0)
                        motor_speed = speed_init
                        motor_dn = False
                        press_flag = True
                        print("motor stopped, count=",count)
                time.sleep(on_cycle_time)

        if button_up.value and button_dn.value:  # if both buttons aren't pressed (active low)
            press_flag = False  # clear the flag

        time.sleep(off_cycle_time)
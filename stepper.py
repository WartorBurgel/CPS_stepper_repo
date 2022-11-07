import pigpio
from time import sleep
from collections import deque
from os import system

steppins = [17, 18, 27, 22]

fullstepsequence = (
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1)
)


class StepperMotor:
    def __init__(self, pi, pins, sequence):
        if not isinstance(pi, pigpio.pi):
            raise TypeError("Der Daemon pipgio.pi ist nicht instanziert!")
        for pin in pins:
            pi.set_mode(pin, pigpio.OUTPUT)
        self.deque = deque(sequence)
        self.pi = pi
        self.__delay_after_step = None

    def set_stepper_delay(self, step_freq):
        if (step_freq > 0) and (step_freq < 1500):
            self.__delay_after_step = 1/step_freq
            return step_freq

    def do_counterclockwise_step(self):
        self.deque.rotate(-1)
        self.do_step_and_delay(self.deque[0])

    def do_clockwise_step(self):
        self.deque.rotate(1)
        self.do_step_and_delay(self.deque[0])

    def do_step_and_delay(self, step):
        nr = 0
        for pin in steppins:
            self.pi.write(pin, step[nr])
            nr += 1
        sleep(self.__delay_after_step)

    def disable_stepper_motor(self, pins):
        for pin in pins:
            self.pi.write(pin, 0)


system("sudo systemctl disable pigpiod")
sleep(0.5)
system("sudo systemctl start pigpiod")

pi = pigpio.pi()
motor = StepperMotor(pi, steppins, fullstepsequence)
motor.set_stepper_delay(900)
for steps in range(2048):
    motor.do_clockwise_step()
for steps in range(2048):
    motor.do_counterclockwise_step()
motor.disable_stepper_motor(steppins)

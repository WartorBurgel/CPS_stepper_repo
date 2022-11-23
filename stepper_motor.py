import pigpio
from time import sleep
from collections import deque


class MyStepperMotor:
    def __init__(self, pi):
        if not isinstance(pi, pigpio.pi):
            raise TypeError("Der Daemon pipgio.pi ist nicht instanziert!")

        self.steppins = [17, 18, 27, 22]
        self.fullstepsequence = (
            (1, 0, 1, 0),
            (0, 1, 1, 0),
            (0, 1, 0, 1),
            (1, 0, 0, 1)
        )

        for pin in self.steppins:
            pi.set_mode(pin, pigpio.OUTPUT)
        self.deque = deque(self.fullstepsequence)
        self.pi = pi
        self.delay_after_step = None

    def set_stepper_delay(self, step_freq):
        if (step_freq > 0) and (step_freq < 1500):
            self.delay_after_step = 1 / step_freq
            return step_freq

    def do_counterclockwise_step(self):
        self.deque.rotate(-1)
        self.do_step_and_delay(self.deque[0])

    def do_clockwise_step(self):
        self.deque.rotate(1)
        self.do_step_and_delay(self.deque[0])

    def do_step_and_delay(self):
        nr = 0
        for pin in self.steppins:
            self.pi.write(pin, self.steppins[nr])
            nr += 1
        sleep(self.delay_after_step)

    def disable_stepper_motor(self):
        for pin in self.steppins:
            self.pi.write(pin, 0)

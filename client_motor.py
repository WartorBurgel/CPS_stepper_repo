import sys
from socket import *
import threading

from time import sleep
from os import system
import pigpio
from stepper_motor import MyStepperMotor


class Client:
    server_port = 5555
    buffer_size = 1024
    host = "192.168.178.47"
    i = 1

    def __init__(self):
        self.received_data = None
        self.data_send = None
        self.input_message = None
        self.exit = False
        self.i = 1
        self.step_freq = 0.00001

        self.client_connection = socket(AF_INET, SOCK_STREAM)
        self.client_connection.connect((self.host, self.server_port))
        print('Verbunden mit Server %s' % self.host)
        self.receive_thread = threading.Thread(target=self.client_receiver)
        self.transmit_thread = threading.Thread(target=self.client_transmitter)
        self.receive_thread.start()
        self.transmit_thread.start()

    def client_receiver(self):
        while not self.exit:
            self.received_data = self.client_connection.recv(self.buffer_size)
            if self.received_data is not None:
                input_message = self.received_data
                if input_message.decode() == 'exit':
                    print('Server hat die Verbindung geschlossen.')
                    self.stop_connection()
                    sys.exit()
                elif input_message.decode() == 'ok':
                    print('Motor dreht')
                    input_message = 'Motor dreht mit Schrittfrequenz' + str(self.step_freq)

                    self.data_send = input_message
                    self.data_send = str(self.data_send)
                    self.client_connection.send(self.data_send.encode())

                elif input_message.decode().strip().isdigit():
                    print('Neue Frequenz' + str(input_message))
                    self.step_freq = input_message
                    self.data_send = input_message
                    self.step_freq = input_message
                    self.data_send = str(self.data_send)
                    self.client_connection.send(self.data_send.encode())

    def client_transmitter(self):
        while not self.exit:
            if self.i == 1:
                input_message = self.step_freq
                self.data_send = input_message
                self.data_send = str(self.data_send)
                self.client_connection.send(self.data_send.encode())
                self.i -= 1

    def stop_connection(self):
        self.exit = True
        self.transmit_thread.isAlive()
        self.client_connection.close()
        print('Client hat die Verbindung beendet')



system('sudo systemctl disable pigpiod')
sleep(0.5)
system('sudo systemctl start pigpiod')
pi = pigpio.pi()

motor = MyStepperMotor(pi)

client1 = Client()

while not client1.exit:
    motor.set_stepper_delay(client1.step_freq)
    motor.do_clockwise_step()


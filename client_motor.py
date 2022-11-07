from socket import *
import threading
from stepper import *


class Client:
    server_port = 5555
    buffer_size = 1024
    host = "192.168.2.50"

    def __init__(self):
        self.received_data = None
        self.data_send = None
        self.input_message = None
        self.exit = False

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
                    print('Server hat die Verbindung geschlossen')
                    self.stop_connection()
                else:
                    print('Client empfängt: %s' % self.received_data)

    def client_transmitter(self):
        while not self.exit:
            print('Type message: ')
            input_message = str(motor.set_stepper_delay)
            self.data_send = input_message
            self.data_send = 'Client ' + str(self.data_send)
            self.client_connection.send(self.data_send.encode())

    def stop_connection(self):
        self.exit = True
        self.transmit_thread.isAlive()
        self.client_connection.close()
        print('Client hat die Verbindung beendet')


client1 = Client()
pi = pigpio.pi()
motor = StepperMotor(pi, steppins, fullstepsequence)
motor.set_stepper_delay(900)

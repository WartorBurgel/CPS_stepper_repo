import sys
from socket import *
import threading


class Server:
    server_port = 5555
    buffer_size = 1024

    def __init__(self):
        self.received_data = None
        self.data_send = None
        self.input_message = None
        self.exit = False
        self.step_freq = 0.000001
        self.i = 1

        self.server_connection = socket(AF_INET, SOCK_STREAM)
        self.server_connection.bind(('', self.server_port))
        self.server_connection.listen(3)
        print('Server gestartet')
        print('Hostname ', gethostname())
        print('IP Nummer: ', gethostbyname(gethostname()))
        print('Listening on Port ' + str(self.server_port))

        self.connected, (self.remotehost, self.remoteport) = self.server_connection.accept()
        print('Verbunden mit %s:%s' % (self.remotehost, self.remoteport))

        self.receive_thread = threading.Thread(target=self.server_receiver)
        self.transmit_thread = threading.Thread(target=self.server_transmitter)
        self.receive_thread.start()
        self.transmit_thread.start()

    def server_receiver(self):
        while not self.exit:
            self.received_data = self.connected.recv(self.buffer_size)
            if self.received_data is not None:
                print('Server empfängt: Schrittfrequenz %s' % self.received_data)

    def server_transmitter(self):
        while not self.exit:
            if self.i == 1:
                print('Type ok to start Motor or type a number between 1 - 1500:')
                self.i -= 1
            if input is not None:
                input_message = input()
                if input_message == 'exit':
                    self.data_send = input_message
                    self.connected.send(self.data_send.encode())
                    self.stop_connection()
                elif input_message == 'ok':
                    self.data_send = input_message
                    self.data_send = str(self.data_send)
                    self.connected.send(self.data_send.encode())
                elif input_message.strip().isdigit():
                    self.data_send = input_message
                    self.data_send = str(self.data_send)
                    self.connected.send(self.data_send.encode())

    def stop_connection(self):
        self.exit = True
        self.server_connection.close()
        self.receive_thread.join()
        print('Server-Verbindung wurde beendet')
        sys.exit()


server = Server()

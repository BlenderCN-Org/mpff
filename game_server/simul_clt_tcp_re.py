#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## simul_client_tcp_recon.py


import sys
from time import time, sleep
import threading
import json

from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

tempo = 0.008

simul = {   'ball_position': [0.5, 3.3],
            'bat_position': [-9.4, 0.0],
            'my_score': 9,
            'my_name': 's' + str(int(time())),
            "reset":         0}

##to_json = json.dumps(simul) + "\n"  # str
##SIMUL_C = to_json.encode("utf-8")  # bytes

class MyTcpClient(Protocol):
    global simul

    def __init__(self):
        print("Un protocol client créé")
        self.user = self.create_user()

    def create_user(self):
        '''Ne sert à rien, il faut utiliser addr TODO'''

        user = str(int(10000* time()))[-8:]
        print("Un user créé: ", user)
        return user

    def connectionMade(self):
        print("Une connexion établie avec le serveur.")
        self.loop_thread()

    def loop(self):
        global simul

        while 1:
            sleep(tempo)
            simul["user"] = self.user
            simul_json = json.dumps(simul)
            toto = simul_json.encode("utf-8")
            self.transport.write(toto)
            #print("Envoi vers serveur tcp")
            pass

    def loop_thread(self):
        thread_C = threading.Thread(target=self.loop)
        thread_C.start()

    def dataReceived(self, data):
        #print("msg {}".format(data))
        #self.transport.write(SIMUL_C)
        pass


class MyTcpClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print('Essai de connexion ...')

    def buildProtocol(self, addr):
        print('Connecté à {}'.format(addr))
        print('Resetting reconnection delay')
        self.resetDelay()
        self.maxDelay = 5  # seconds
        return MyTcpClient()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        print('Resetting reconnection delay')
        self.resetDelay()
        self.maxDelay = 5
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


if __name__ == '__main__':
    host, port = "192.168.1.11", 8888
    reactor.connectTCP(host, port, MyTcpClientFactory())
    reactor.run()

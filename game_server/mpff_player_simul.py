#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## mpff_player_simul.py

'''
Envoi en TCP sur 8888 des datas simulant un joueur.

'''

import os, sys
from time import time, sleep
import threading
import json
import random

from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from player_simul import Player


# Variable globale à définir
HOST = "127.0.0.1"
PORT = 8888

NUMERO_JOUEUR = random.randint(0, 8)
print("Numéro du joueur", NUMERO_JOUEUR)

#  Variable globale à ne pas modifier
# 9 joueurs maxi, os._exit si plus
#                    r     centre   sec  score_rnd   x1  y1  x2  y2
PLAYER_LIST = [ ( (3, 7), (-5, -5), 0.4,   160,      5, -2,  9, 2 ),
                ( (2, 5), (-3, -2), 1.0,   100,      4,  2,  7, 4 ),
                ( (2, 7), (-1, -1), 0.7,   150,      2,  6,  6, 10 ),
                ( (2, 6), (0,  0),  0.4,   200,     -2,  9,  2, 4 ),
                ( (2, 4), (1,  1),  0.5,   300,     -4,  5,  0, 1 ),
                ( (2, 3), (2,  2),  0.6,   130,     -5,  1, -1,-4 ),
                ( (2, 9), (3,  3),  0.7,   110,     -1, -3,  3, 1 ),
                ( (1, 9), (4,  4),  0.8,   80,       1,  0,  5, -4 ),
                ( (1, 5), (4,  5),  0.9,   250,      3,  2,  8, -8 )]



class MyTcpClient(Protocol):

    global NUMERO_JOUEUR, PLAYER_LIST

    def __init__(self):
        global NUMERO_JOUEUR, PLAYER_LIST

        print("Un protocol client créé. Nombre de joueurs simulés", NUMERO_JOUEUR)

        self.t_print = time()

        p = NUMERO_JOUEUR
        self.player_simul = Player( PLAYER_LIST[p][0],
                                    PLAYER_LIST[p][1],
                                    PLAYER_LIST[p][2],
                                    PLAYER_LIST[p][3],
                                    PLAYER_LIST[p][4],
                                    PLAYER_LIST[p][5],
                                    PLAYER_LIST[p][6],
                                    PLAYER_LIST[p][7])

    def connectionMade(self):

        print("Une connexion établie avec le serveur.")
        self.loop_thread()

    def loop(self):
        '''Envoi à 60 Hz vers le serveur en TCP
        de data de simulation d'un joueur.
        '''

        while 1:
            sleep(0.01666)
            simul = self.player_simul.simul
            simul_json = json.dumps(simul)
            toto = simul_json.encode("utf-8")
            self.transport.write(toto)
            if time() - self.t_print > 1:
                self.t_print = time()
                print(simul)


    def loop_thread(self):
        '''Thread d'envoi.'''

        thread_C = threading.Thread(target=self.loop)
        thread_C.start()


class MyTcpClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print('Essai de connexion ...')

    def buildProtocol(self, addr):
        print('Connecté à {}'.format(addr))
        print('Resetting reconnection delay')
        self.resetDelay()
        self.maxDelay = 1  # seconds
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

    reactor.connectTCP(HOST, PORT, MyTcpClientFactory())
    reactor.run()

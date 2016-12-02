#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## simul_server.py

import os, sys
from time import time, sleep
import threading
import json
import ast

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor, defer

from labtools.labconfig import MyConfig
from labtools.labformatter import Formatter
from labtools.labfifolist import PileFIFO
from game_dictator import GameManagement

# Variable globale
scr = os.path.dirname(os.path.abspath(__file__))
conf = MyConfig(scr + "/mpff.ini")
my_conf = conf.conf
pretty = Formatter()
print("Configuration du serveur: {}".format(pretty(my_conf)))

MULTICAST_IP = my_conf["multicast"]["ip"]
MULTICAST_PORT = my_conf["multicast"]["port"]

to_raw = {'dictat': {   'classement': {},
                        'score': [9, 8],
                        'who_are_you': {'gf14560487': 1, 'gg14560430': 0},
                        'other_bat_position': {0: [-9.4, 0.0], 1: [9.4, 0.0]},
                        'level': 2,
                        'ball_position_server': [0.5, 3.3],
                        'state': 'play'}}

to_json = json.dumps(to_raw) # str
TO_ALL = to_json.encode("utf-8")  # bytes


class MulticastPong(DatagramProtocol):
    '''Envoi en continu à tous les joueurs.'''

    def __init__(self):
        # Gestion du jeu, my_conf = dict
        self.game = GameManagement(my_conf)

        # Pour gestion des déconnectés propre
        self.tempo_1s = time()

        # Boucle infinie pour envoi continu à tous les joueurs
        self.loop_thread()

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        # Set the TTL>1 so multicast will cross router hops:
        # https://www.rap.prd.fr/pdf/technologie_multicast.pdf
        # préconise TTL = 1
        self.transport.setTTL(1)
        # Join a specific multicast group:
        self.transport.joinGroup("228.0.0.5")

    def loop(self):
        while 1:
            addr = "228.0.0.5", 18888
            sleep(0.02)
            try:
                self.transport.write(TO_ALL, addr)
            except:
                pass

    def loop_thread(self):
        thread_C = threading.Thread(target=self.loop)
        thread_C.start()


class MyTcpServer(Protocol):
    '''Message reçu de chaque joueur en TCP:
            {'ball_position': [0.5, 3.3],
            'bat_position': [-9.4, 0.0],
            'my_score': 9,
            'my_name': 'ggffg1456048730',
            'my_ip': '192.168.0.103'}
    '''

    def __init__(self, factory):
        self.factory = factory
        self.t_zero = time()
        self.create_user()

    def create_user(self):
        '''Le plus vieux, donc le plus petit va demander la mise à jour du jeu.
        '''

        self.user = str(int(10000* time()))[-8:]
        print("Un user créé: ", self.user)

    def connectionMade(self):
        self.addr = self.transport.client
        print("Une connexion établie par le client {}".format(self.addr))

    def connectionLost(self, reason):
        print("Connection lost, reason:", reason)
        print("Connexion fermée avec le client {}".format(self.addr))
        self.user = None

    def dataReceived(self, data):
        ''' TODO: rajouter decode sorting'''

        # Retourne un dict ou None
        data = datagram_decode(data)

        if data:
            self.insert_data(data)
            #print(data)
            ##d = defer.Deferred()
            ##d.addCallback(self.insert_data)
            ##reactor.callLater(0, d.callback, data)

    def insert_data(self, data) :
        self.factory.game.insert_data(self.user, data)


class MyTcpServerFactory(Factory):

    def __init__(self):
        self.game = GameManagement(my_conf)

        # Serveur
        self.numProtocols = 1
        print("Serveur twisted réception sur {}\n".format(8888))

    def buildProtocol(self, addr):
        print("Nouveau protocol crée dans l'usine: factory")
        print("nombre de protocol dans factory", self.numProtocols)

        return MyTcpServer(self)


def datagram_decode(data):
    '''Decode le message.
    Retourne un dict ou None
    '''

    try:
        dec = data.decode("utf-8")
    except:
        #print("Décodage UTF-8 impossible")
        dec = data

    try:
        msg = ast.literal_eval(dec)
    except:
        #print("ast.literal_eval impossible")
        msg = dec

    if isinstance(msg, dict):
        return msg
    else:
        #print("Message reçu: None")
        return None


if __name__ == "__main__":
    ## Receive
    endpoint = TCP4ServerEndpoint(reactor, 8888)
    endpoint.listen(MyTcpServerFactory())

    ## Send
    #reactor.listenMulticast(MULTICAST_PORT, MulticastPong(), listenMultiple=True)

    ## Pour les 2
    reactor.run()


'''
        # provisoire
        data = data.decode("utf-8")
        data = ast.literal_eval(data)
        self.player_pile.append(data)

        # dans la big_pile
        #self.game.collect_data(data)

        # Vérif provisoire
        if time() - self.t_zero > 5:
            self.t_zero = time()
            print("from", self.addr,
                          self.player_pile.queue[self.player_pile.size - 1])

dir(self)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__getattribute__', '__gt__', '__hash__',
'__implemented__', '__init__', '__le__', '__lt__', '__module__', '__ne__',
 '__new__', '__providedBy__', '__provides__', '__reduce__', '__reduce_ex__',
  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  '__weakref__', 'connected', 'connectionLost', 'connectionMade',
  'dataReceived', 'factory', 'logPrefix', 'makeConnection', 'num_player',
  'play_fifo', 't_zero', 'transport']

dir(self.factory)
  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
  '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__',
  '__implemented__', '__init__', '__le__', '__lt__', '__module__',
  '__ne__', '__new__', '__providedBy__', '__provides__', '__reduce__',
  '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
  '__subclasshook__', '__weakref__', 'buildProtocol', 'doStart', 'doStop',
  'forProtocol', 'game', 'logPrefix', 'noisy', 'numPorts',
  'numProtocols', 'protocol', 'startFactory', 'stopFactory']

dir(self.factory.logPrefix)
['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__',
'__format__', '__func__', '__ge__', '__get__', '__getattribute__', '__gt__',
'__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__',
'__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__',
'__subclasshook__']

print(dir(self.transport))
['SEND_LIMIT', 'TLS', '__class__', '__delattr__', '__dict__', '__dir__',
'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
'__hash__', '__implemented__', '__init__', '__le__', '__lt__', '__module__',
'__ne__', '__new__', '__providedBy__', '__provides__', '__reduce__',
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
'__subclasshook__', '__weakref__', '_aborting', '_addressType', '_base',
'_closeSocket', '_closeWriteConnection', '_dataReceived',
'_fromConnectedSocket', '_getLogPrefix', '_isSendBufferFull',
'_maybePauseProducer', '_postLoseConnection', '_shouldShutdown',
'_tempDataBuffer', '_tempDataLen', '_tlsClientDefault', '_writeDisconnected',
'_writeDisconnecting', 'abortConnection', 'bufferSize', 'client', 'connected',
'connectionLost', 'dataBuffer', 'disconnected', 'disconnecting', 'doRead',
'doWrite', 'fileno', 'getHandle', 'getHost', 'getPeer', 'getTcpKeepAlive',
'getTcpNoDelay', 'hostname', 'logPrefix', 'logstr', 'loseConnection',
'loseWriteConnection', 'offset', 'pauseProducing', 'producer', 'producerPaused',
 'protocol', 'reactor', 'readConnectionLost', 'registerProducer', 'repstr',
 'resumeProducing', 'server', 'sessionno', 'setTcpKeepAlive', 'setTcpNoDelay',
 'socket', 'startReading', 'startTLS', 'startWriting', 'stopConsuming',
 'stopProducing', 'stopReading', 'stopWriting', 'streamingProducer',
 'unregisterProducer', 'write', 'writeConnectionLost', 'writeSequence',
 'writeSomeData']



  '''

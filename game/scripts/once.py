#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## once.py

#############################################################################
# Copyright (C) Labomedia November 2012
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

'''
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier las variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.

'''

import ast
import json
import threading
from time import sleep

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from scripts.labtools.labconfig import MyConfig
from scripts.labtools.labformatter import Formatter
from scripts.labtools.tempo import Tempo


# Blender
from bge import logic as gl


class MulticastClient(DatagramProtocol):
    '''Ce client reçoit les datas du serveur, ip et dictat'''

    def startProtocol(self):
        '''Ticket sur le groupe multicast.'''

        # Join the multicast address, so we can receive replies:
        self.transport.joinGroup(gl.multi_ip)

        print("Le Client Multicast a pris un ticket sur {}".format(gl.multi_addr))

    def datagramReceived(self, datagram, address):
        '''Réception, demande de traitement.'''

        data = datagram_decode(datagram)

        if data:
            self.datagram_sorting(data)

    def datagram_sorting(self, data_dict):
        '''Met à jour les variables avec les valeurs reçues. data = dict'''

        data = data_dict["paradis"]

        if "ip" in data:
            gl.ip_server = data["ip"]

        if "dictat" in data:
            data = data["dictat"]
            if data:
                if gl.state == "play" or gl.state == "Rank":
                    self.tri_msg(data)

    def tri_msg(self, data):
        if "level" in data:
            gl.level = data["level"]
            if gl.level < 1:
                gl.level = 1
            if gl.level > 10:
                gl.level = 10

        if "state" in data:
            gl.state = data["state"]

        if "ball_position_server" in data:
            # list de 2
            gl.ball_position_server = data["ball_position_server"]

        if "score" in data:
            gl.score = data["score"]

        if "other_bat_position" in data:
            gl.bat_position = data["other_bat_position"]

        if "who_are_you" in data:
            '''Ma place dans ??????????'''
            # {"toto":0, "tata":1}
            who = data["who_are_you"]
            for k, v in who.items():
                if gl.my_name == k:
                    gl.I_am = v

        if "classement" in data:
            '''Classement des joueurs:
            {'toto': 3, 'labomedia': 2, 'gddgsg': 1}
            '''
            gl.classement = data["classement"]


class MyTcpClient(Protocol):

    def connectionMade(self):
        print("Connexion établie avec le serveur\n")
        self.send_thread()

    def connectionLost(self, reason):
        print("Connection lost")

    def send(self, data):
        '''Envoi d'un message si play en cours:
        data doit êre un dictionnaire.
        '''

        if gl.state == "play":
            msg_json = json.dumps(data) # str
            msg = msg_json.encode("utf-8")  # bytes
            try:
                self.transport.write(msg)
            except:
                pass

    def send_loop(self):
        while 1:
            #print(gl.msg_to_send)
            sleep(0.015)
            # gl.msg_to_sen json + encodé dans message.py
            if gl.msg_to_send:
                self.send(gl.msg_to_send)
                gl.msg_to_send = None


    def send_thread(self):
        self.t = threading.Thread(target=self.send_loop)
        self.t.start()


class MyTcpClientFactory(ReconnectingClientFactory):

    def startedConnecting(self, connector):
        print("\nstartedConnecting sur ip", gl.ip_server, "\n")

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
        self.maxDelay = 1
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


def datagram_decode(datagram):
    '''Decode la réception qui est des bytes, pour obtenir un dict.
    Valable pour python3.
    Cette fonction doit être revue pour être en béton.
    '''

    try:
        dec = datagram.decode("utf-8")
    except:
        print("Décodage UTF-8 inutile !")
        dec = datagram

    try:
        msg_dict = ast.literal_eval(dec)
    except:
        print("ast.literal_eval raté")
        msg_dict = None

    if isinstance(msg_dict, dict):
        return msg_dict
    else:
        print("Mauvais message reçu")
        return None

def run_twisted():
    reactor.listenMulticast(gl.multi_port, MulticastClient(), listenMultiple=True)
    #reactor.connectTCP(gl.ip_server, gl.tcp_port, MyTcpClientFactory())
    reactor.run(installSignalHandlers=False)

def run_twisted_thread():
    thread_twist = threading.Thread(target=run_twisted)
    thread_twist.start()

def TCP_client():
    '''Crée le client TCP.'''

    reactor.connectTCP(gl.ip_server, gl.tcp_port, MyTcpClientFactory())

def TCP_client_thread():
    '''Le client est dans un thread.'''

    thread_t = threading.Thread(target=TCP_client)
    thread_t.start()

def get_conf():
    '''Récupère la configuration depuis le fichier *.ini.'''

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    gl.once = 0

    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/mpff.ini")
    gl.conf = gl.ma_conf.conf

    print("Configuration du jeu MPFF:\n")
    pretty = Formatter()
    print(pretty(gl.conf))

def init_variable():
    '''Valeurs par défaut de tous les attributs du bge.logic'''

    # state possible:play rank labo
    gl.state = "labo"

    # msg à envoyer
    gl.msg_to_send = None

    # Défini par le serveur
    gl.level = 1
    gl.block = 0

    # Rank
    gl.text = ""
    gl.classement =  {}  # {'toto': 3, 'labomedia': 2, 'gddgsg': 1}

    # vient du server
    gl.ball_position_server = [0,0] # liste
    gl.score = [0,0,0,0,0,0,0,0,0,0] # liste
    gl.bat_position = { 0: [0,0],   # dict !!
                        1: [0,0],
                        2: [0,0],
                        3: [0,0],
                        4: [0,0],
                        5: [0,0],
                        6: [0,0],
                        7: [0,0],
                        8: [0,0],
                        9: [0,0]}

    # Scene Name
    gl.my_name = ""
    gl.my_name_ok = 0
    gl.name_obj = 0

    gl.I_am = 0
    gl.ip_server = "127.0.0.1"

    gl.multi_ip = gl.conf["multicast"]["ip"]
    gl.multi_port = gl.conf["multicast"]["port"]
    gl.multi_addr = gl.multi_ip, gl.multi_port
    gl.tcp_port = gl.conf["tcp"]["port"]

    # level 1 only
    gl.level1_rated = 0 # si classement du level 1 fait dans game.py
    gl.classement_level1 = {}
    gl.tempo_rank_level1 = 0

def init_blender_obj():
    '''Définit les variables qui permettront d'accéder aux objects de blender.
    '''

    #Cube de Labomedia
    gl.cube_obj = 0
    # L'objet qui permet d'afficher le texte du classement
    gl.rank_obj = 0
    # L'objet dn bas de Labomedia
    gl.help_obj = 0

    # permet accès aux objet blender score et leur score
    gl.goal = {  0 : 0,
                1 : 1,
                2 : 2,
                3 : 3,
                4 : 4,
                5 : 5,
                6 : 6,
                7 : 7,
                8 : 8,
                9 : 9   }

    # All bat
    gl.bat = {  0 : 0,
                1 : 1,
                2 : 2,
                3 : 3,
                4 : 4,
                5 : 5,
                6 : 6,
                7 : 7,
                8 : 8,
                9 : 9}

    gl.ball = 0  # mon objet blender ball

def init_tempo():
    ''' * tempo_liste = [("intro", 60), ("print", 12), ("sound", 6)]
        * tempoDict = Tempo(tempo_liste)
        * tempoDict.update()
    '''

    tempo_liste = [("always", 1), ("frame_60", 60)]
    gl.tempoDict = Tempo(tempo_liste)

def main():
    '''Lancé une seule fois à la 1ère frame au début du jeu par main_once.'''

    get_conf()
    init_variable()
    init_blender_obj()
    init_tempo()

    # Lance multicast et reactor
    run_twisted_thread()

    # Envoi TCP
    # Pour lancer ce thread, il faut avoir reçu l'ip server en multicast
    # Vérif que ip server est ok

    # sinon ne fait pas le while !!!!!!!! TODO
    sleep(1)
    print(gl.ip_server)
    ##while gl.ip_server != "127.0.0.1":
        ##sleep(1)
        ##print("attente")

    print("\nIP serveur =", gl.ip_server, "lancement thread TCP")
    # C'est bon pour le TCP
    TCP_client_thread()

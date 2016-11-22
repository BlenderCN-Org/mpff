#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## game_dictator.py


'''
De msg =
{'ball_position': [0.5, 3.3],
'bat_position': [-9.4, 0.0],
'my_score': 9,
'my_name': 'ggffg1456048730',
'my_ip': '192.168.0.103'}

Vers
players = [
('gg1456048982', {  'ball_position': [2.1, 4.8],
                    'my_score': 9,
                    'time': 1456048988.52,
                    'classement': 0,
                    'bat_position': [-9.4, 0.0],
                    'my_name': 'gg1456048982'}),

('gg1456048985', {  'ball_position': [7.4, 9.1],
                    'my_score': 8,
                    'time': 1456048987.50,
                    'classement': 0,
                    'bat_position': [9.4, 0.0],
                    'my_name': 'gg1456048985'})
]

msg envoyé:
{'dictat': {
'classement': {},
'score': [9, 8],
'who_are_you': {'gffgfg1456048734': 1, 'ggffg1456048730': 0},
'other_bat_position': {0: [-9.4, 0.0], 1: [9.4, 0.0]},
'level': 2,
'ball_position_server': [0.5, 3.3],
'state': 'play'}}
'''


from collections import OrderedDict
from time import time, sleep
from random import uniform
import threading
import json

from labtools.labfifolist import PileFIFO
from labtools.labformatter import Formatter


class GameManagement():
    '''Gestion du jeu avec les datas envoyés par tous les joueurs'''

    def __init__(self, conf):
        # Config du jeu
        self.conf = conf

        # Dict des datas de tous les joueurs
        self.players = OrderedDict()
        # Gestion du jeu
        self.winner = None
        self.ranked = []
        self.state = "play"
        self.rank = None
        self.t_rank = 0
        self.classement = {}
        self.level = 0

        # Spécifique protocol twisted 3
        t = time()
        self.t_print = t  # print régulier
        self.t_count = t  # Affichage fréquence régulier
        self.count = 0
        self.pile_dict = {}

    def insert_data_in_pile(self, user, data):
        '''Ajoute les datas reçues d'un user dans sa pile,
        Demande de la mise à jour de la gestion du jeu à 60 Hz.
        '''

        try:
            self.pile_dict[user].append(data)
        except:
            self.pile_dict[user] = PileFIFO(60)
            print("Init de la pile du user:", user)

        # Affichage de la fréquence d'appel de cette méthode
        self.frequency()

    def pile_to_players(self):
        '''Appelé par create_msg_for_all_players
        Provisoire TODO
        Passe la dernière valeur des piles dans players dict.
        msg = {'my_score': 10, 'ball_position': [4.39, 9.99],
        'my_name': 'n1654453', 'bat_position': [1.16, -0.16]}
        '''

        # copie du dict pour le libérer
        all_data = self.pile_dict.copy()
        for cle, valeur in all_data.items():
            # cle = user de TCP, valeur = pile, queue = list
            try:
                # valeur est un object PileFIFO
                msg = valeur.queue[59]
            except:
                msg = None
            self.insert_data_in_players_dict(msg, cle)

    def frequency(self):
        self.count += 1
        t = time()
        if t - self.t_count > 5:
            print("Fréquence d'accès par les clients", int(self.count/5))
            self.count = 0
            self.t_count = t

    def insert_data_in_players_dict(self, msg, user):
        '''A chaque reception de msg par le server, insère in dict'''

        # Seulement si le nom est valide, donc saisi
        try:
            if msg and msg["my_name"] != "":
                if msg["my_name"] in self.players:
                    self.players[msg["my_name"]]["ball_position"] = msg["ball_position"]
                    self.players[msg["my_name"]]["bat_position"] = msg["bat_position"]
                    self.players[msg["my_name"]]["my_score"] = msg["my_score"]
                    self.players[msg["my_name"]]["time"] = time()
                    self.players[msg["my_name"]]["user"] = user
                else:
                    self.players[msg["my_name"]] = {}
                    self.players[msg["my_name"]]["ball_position"] = msg["ball_position"]
                    self.players[msg["my_name"]]["bat_position"] = msg["bat_position"]
                    self.players[msg["my_name"]]["my_score"] = msg["my_score"]
                    self.players[msg["my_name"]]["my_name"] = msg["my_name"]
                    self.players[msg["my_name"]]["time"] = time()
                    self.players[msg["my_name"]]["classement"] = 0
                    self.players[msg["my_name"]]["user"] = user
        except:
            pass

    def update_game_management(self):
        '''Appelé par create_msg_for_all_players, tourne donc à 60 fps.'''

        self.pile_to_players()
        self.update_level()
        self.update_classement()
        self.update_rank()
        #self.print_some()
        pass

    def update_level(self):
        l = len(self.players)
        if l == 0:
            l = 1
        self.level = l

    def update_rank(self):
        '''Je bloque la réception et maj,
        j'envoie les infos pour la scène rank.'''

        if self.rank == "Rank":
            self.state = "Rank"
            if time() - self.t_rank > 3:
                self.reset_data()

    def update_classement(self):
        '''Fonction trop longue donc pas clair: TODO !!'''

        self.ranked = []

        # Je récupère ceux qui sont déjà classés
        for k, v in self.players.items():
            if v["classement"] != 0:
                self.ranked.append(v["classement"])
        self.ranked.sort()

        # Je récupère ceux qui viennent de perdre
        # mais le nb de classés doit être inf au nb de joueurs, pas de 1:
        if len(self.ranked) < self.level:
            for k, v in self.players.items():
                # Ceux qui viennent de perdre et ne ne sont pas encore classés
                if v["classement"] == 0 and v["my_score"] == 0:
                    if len(self.ranked) == 0:
                        cl = len(self.players)
                    else:
                        cl = self.ranked[0] - 1
                    if cl != 1: # le gagnant est gérer ci-dessous
                        v["classement"] = cl
                        self.ranked.append(cl)
                        self.ranked.sort()

        # Si il y a un 2ème, c'est fini, le restant est le 1er
        # le score du dernier ne va pas à 0, et si il y va, il a gagné
        if 2 in self.ranked:
            # Qui a un classement = 0 ?
            for k, v in self.players.items():
                if v["classement"] == 0:
                    v["classement"] = 1
                    self.winner = v["my_name"]
                    self.rank = "Rank"
                    self.t_rank = time()
                    print("The winner is {}".format(self.winner))

        # Maj du dict du classement final, car un joueur est 1
        # mais 1 seul 1, parfois plus car le jeu continue à tourner
        verif = 0
        for i in self.ranked:
            if i == 1:
                verif += 1
        if 1 in self.ranked and verif == 1:
            clst = {}
            for k, v in self.players.items():
                clst[v["my_name"]] = v["classement"]
            self.classement = clst
        else:
            self.classement = {}

    def get_ball(self):
        '''Retourne la position de la balle du premier joueur dans players dict.
        '''

        ball = [0, 0]  # liste
        for k, v in self.players.items():
            ball = v["ball_position"]
            # j'ai lu le premier dans le dict, sa balle sert pour les autres
            break
        return ball

    def get_score(self):
        '''Retourne les scores de tous les joueurs, dans une liste.
        Le dict est ordonné, j'ajoute les scores dans l'ordre.
        '''

        score = []  # liste
        for k, v in self.players.items():
            score.append(v["my_score"])
        return score

    def get_bat(self):
        '''Retourne la position des bats de tous les joueurs.
        Le dict est ordonné, j'ajoute les bats dans l'ordre.
        '''

        bat = {}  # dict
        b = 0
        for k, v in self.players.items():
            bat[b] = v["bat_position"]
            b += 1
        return bat

    def get_who(self):
        '''Retourne le numéro de tous les joueurs dans un dict
        {"toto":0, "tata":1}
        '''

        who = {}
        a = 0
        for k, v in self.players.items():
            who[v["my_name"]] = a
            a += 1
        return who

    def create_msg_for_all_players(self):
        '''Appelé à 60 fps. Commence par demander une mise à jour du jeu.
        Message à créer:
        { 'ball_position_server': [7.19, 7.19],
                        'classement': {},
                        'state': 'play',
                        'other_bat_position': {0: [-9.4, 0.0], 1: [-9.4, 0.40]},
                        'level': 2,
                        'who_are_you': {'tt1455984924': 0, 'tt1455984921': 1},
                        'score': [9, 7]}
        '''

        # Maj
        self.update_game_management()

        # Récup data à envoyer
        ball = self.get_ball()
        score = self.get_score()
        bat = self.get_bat()
        who = self.get_who()

        # Je regroupe tout
        if self.level > 1:
            msg =   {"level": self.level,
                                "state" : self.state,
                                "ball_position_server": ball,
                                "score": score,
                                "other_bat_position": bat,
                                "classement": self.classement,
                                "who_are_you": who,
                                 }
        else:
            msg = None

        return msg

    def delete_disconnected_players(self, user):
        '''Appelé depuis MyTcpServer si conection lost.'''

        del self.pile_dict[user]
        print("{} supprimé dans pile_dict".format(user))

        for key, val in self.players.items():
            if val["user"] == user:
                del self.players[key]
                break
        print("{} supprimé dans players".format(key))

    def reset_data(self):
        print("Reset in Game Dictator")
        self.players = OrderedDict()
        self.ranked = []
        self.winner = None
        self.rank = None
        self.t_rank = 0
        self.state = "play"

    def print_some(self):
        if time() - self.t_print > 10:
            toto = []
            for k, v in self.players.items():
                toto.append((v["my_name"][:-10], v["my_score"], v["classement"]))
            print("Joueurs:\n {}".format(toto))
            print( '''              level: {}, state: {}
            classé: {}
            classement: {}'''.format(self.level, self.state,
                                    self.ranked, self.classement))

            for k, v in self.players.items():
                print("joueur en cours", v)
            self.t_print = time()


if __name__ == "__main__":
    # utiliser mpff_player_simul
    import os
    from labtools.labconfig import MyConfig

    scr = os.path.dirname(os.path.abspath(__file__))
    conf = MyConfig(scr + "/mpff.ini")
    my_conf = conf.conf
    game = GameManagement(conf)

    msg1 = { "my_name":       "rien124",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      6 }

    msg2 = { "my_name":       "tout123",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      7 }

    msg3 = { "my_name":       "moi125",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      9 }

    msg4 = { "my_name":       "toi333",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      8 }

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
                    'address': ('192.168.0.103', 55345),
                    'my_score': 9,
                    'time': 1456048988.52,
                    'classement': 0,
                    'bat_position': [-9.4, 0.0],
                    'my_name': 'gg1456048982'}),

('gg1456048985', {  'ball_position': [7.4, 9.1],
                    'address': ('192.168.0.103', 58877),
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
import threading

from labtools.labfifolist import PileFIFO
from labtools.labformatter import Formatter

'''    ##def test_dict_apply_thread(self):
        ##thread_test = threading.Thread(target=self.test_dict_apply)
        ##thread_test.start()
'''


class GameManagement():
    '''Gestion du jeu avec les datas envoyés par tous les joueurs'''

    def __init__(self, conf):
        # Config du jeu
        self.conf = conf

        # Dict des datas de tous les joueurs
        self.players = OrderedDict()

        self.winner = None
        self.ranked = []
        self.state = "play"
        self.rank = None
        self.t_rank = 0
        self.classement = {}
        self.level = 0
        t = time()
        self.t_print = t
        self.t_count = t
        self.t_blend = t
        self.count = 0
        self.test_dict = {}
        self.pulse_verif = 0
        self.blend_freq = 0.02

    def insert_data(self, user, data):
        '''Ajoute les datas reçues d'un user dans sa pile,
        Demande de la mise à jour de la gestion du jeu à 60 Hz.
        '''

        try:
            self.test_dict[user].append(data)
        except:
            self.test_dict[user] = PileFIFO(60)
            print("Init de la pile du user", user)

        # Affichage de la fréquence d'appel de cette méthode
        self.frequency()
        #self.test_dict_apply()

    def test_dict_apply(self):
        '''Utilisation de test_dict pour gérer le jeu à 60 Hz.
        TODO: cette méthode n'est à priori pas bloquante !!'''

        t = time()
        if t - self.t_blend > self.blend_freq:
            self.pulse_verif += 1
            self.t_blend = t
            all_data = self.test_dict.copy()
            # Print
            if len(all_data) > 0:
                l = []
                for k, v in all_data.items():
                    l.append(k)
                #print(l)
            # j'exploite
            pass

    def frequency(self):
        ''' ##print("test_dict",self.test_dict )
            ##tmin = 0
            ##tmax = 0
            ##v_list = []
            ##for k, v in self.test_dict.items():
                ##v_list.append(v)
            ##tamx = max(v_list)
            ##tmin = min(v_list)
            ##delta = tamx - tmin
            ##print("delta", delta)
            '''

        self.count += 1
        t = time()
        if t - self.t_count > 5:
            print("Fréquence: ", int(self.count/5))
            self.count = 0
            self.t_count = t

            f = int(1/self.blend_freq)
            v = int(self.pulse_verif/5)
            toto = "Fréquence d'appel de la méthode à {} Hz: {}"
            print(toto.format(f ,v))
            self.pulse_verif = 0

    def collect_data(self, data):
        '''TODO: supprimer ip des envois client
            {   'ball_position': [0.5, 3.3],
                'bat_position': [-9.4, 0.0],
                'my_score': 9,
                'my_name': 'ggffg1456048730'}

        ##ball = data['ball_position']
        ##bat = data['bat']
        ##score = data['score']
        ##name = data['my_name']
        ##self.big_pile.append({"bat": bat,
                              ##"ball": ball,
                              ##"score": score,
                              ##"name": name})'''

        pass

    def insert_data_in_dict(self, msg, address):
        '''A chaque reception de msg par le sever, insère in dict, update'''

        # Seulement si le nom est valide, donc saisi
        if msg["my_name"] != "":
            if msg["my_name"] in self.players:
                self.players[msg["my_name"]]["ball_position"] = msg["ball_position"]
                self.players[msg["my_name"]]["bat_position"] = msg["bat_position"]
                self.players[msg["my_name"]]["my_score"] = msg["my_score"]
                self.players[msg["my_name"]]["time"] = time()
            else:
                self.players[msg["my_name"]] = {}
                self.players[msg["my_name"]]["ball_position"] = msg["ball_position"]
                self.players[msg["my_name"]]["bat_position"] = msg["bat_position"]
                self.players[msg["my_name"]]["my_score"] = msg["my_score"]
                self.players[msg["my_name"]]["my_name"] = msg["my_name"]
                self.players[msg["my_name"]]["address"] = address
                self.players[msg["my_name"]]["time"] = time()
                self.players[msg["my_name"]]["classement"] = 0

        # Update du jeu, uniquement si le 1er joueur est reçu
        if self.players:
            items_list = list(self.players.items())[0]
            if items_list[0] == msg["my_name"]:
                self.update_game_management()

    def update_game_management(self):
        '''  maj déconnectés, classement, level, rank
        '''

        self.delete_disconnected_players()
        self.update_level()
        self.update_classement()
        self.update_rank()
        self.print_some()

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

    def delete_disconnected_players(self):
        for key, val in self.players.items():
            if time() - val["time"] > 1.2:
                print("{} supprimé des joueurs".format(val["my_name"]))
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

    def create_msg_for_all_players(self):
        '''{'dictat': { 'ball_position_server': [7.19, 7.19],
                        'classement': {},
                        'state': 'play',
                        'other_bat_position': {0: [-9.4, 0.0], 1: [-9.4, 0.40]},
                        'level': 2,
                        'who_are_you': {'tt1455984924': 0, 'tt1455984921': 1},
                        'score': [9, 7]}}
        '''
        # le premier dans le dict ordonné donne la position de la balle
        ball = [0, 0]  # liste
        for k, v in self.players.items():
            ball = v["ball_position"]
            break

        # le dict est ordonné, j'ajoute les scores dans l'ordre
        score = []  # liste
        for k, v in self.players.items():
            score.append(v["my_score"])

        # le dict est ordonné, j'ajoute les bats de tous les joueurs
        bat = {}  # dict
        b = 0
        for k, v in self.players.items():
            bat[b] = v["bat_position"]
            b += 1

        # Dict du numéro des joueurs {"toto":0, "tata":1}
        who = {}
        a = 0
        for k, v in self.players.items():
            who[v["my_name"]] = a
            a += 1

        if self.level > 1:
            msg =   {"dictat": {"level": self.level,
                                "state" : self.state,
                                "ball_position_server": ball,
                                "score": score,
                                "other_bat_position": bat,
                                "classement": self.classement,
                                "who_are_you": who,
                                 }}
        else:
            msg = {"dictat": 0}

        return msg

    def reset_data(self):
        print("Reset in Game Dictionnary")
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
            print()
            print( '''              level: {}, state: {}
            classé: {}
            classement: {}'''.format(self.level, self.state,
                                    self.ranked, self.classement))

            self.t_print = time()


if __name__ == "__main__":
    # only to test
    import os
    from labtools.labconfig import MyConfig

    scr = os.path.dirname(os.path.abspath(__file__))
    conf = MyConfig(scr + "/mpff.ini")
    my_conf = conf.conf
    game = GameManagement(conf)

    msg1 = { "my_ip":         "10.0.0.5",
             "my_name":       "rien124",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      6 }

    msg2 = { "my_ip":         "10.0.0.2",
             "my_name":       "tout123",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      7 }

    msg3 = { "my_ip":         "10.0.0.10",
             "my_name":       "moi125",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      9 }

    msg4 = { "my_ip":         "10.0.0.20",
             "my_name":       "toi333",
             "ball_position": [2,3],
             "bat_position": [2, 4],
             "my_score":      8 }

    a = 1
    while 1:
        a += 1
        sleep(0.5)
        game.insert_data_in_dict(msg1, ("10.0.0.5", 12345))
        game.insert_data_in_dict(msg2, ("10.0.0.2", 12346))
        game.insert_data_in_dict(msg3, ("10.0.0.10", 12347))
        if a < 3:
            game.insert_data_in_dict(msg4, ("10.0.0.20", 123563))

        # diminution des scores pour le prochain tour
        msg1["my_score"] -= 1
        if msg1["my_score"] < 0:
            msg1["my_score"] = 9

        msg2["my_score"] -= 1
        if msg1["my_score"] < 0:
            msg1["my_score"] = 6

        msg3["my_score"] -= 1
        if msg1["my_score"] < 0:
            msg1["my_score"] = 7

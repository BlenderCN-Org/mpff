#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## player_simul.py


from time import time, sleep
import math
import random
import threading


class Player:
    '''Simulation d'un joueur de MPFF.
    Crée un dictionnaire équivalent à celui
    envoyé par le jeu réel dans Blender soit

    simul = {   'ball_position': [0.5, 3.3],
                'bat_position': [-9.4, 0.0],
                'my_score': 9,
                'my_name': 'gf1456048730'}
    Tourne à 60 Hz
    '''

    def __init__(self, r, centre, sec, score_rnd, x1, y1, x2, y2):
        '''sec: nombre de sec pour faire 1/4 de tour > entre
        score_rnd: score varie avec random sur 0, score_rnd > entre 150 et 300
                    300 varie moins vite
        '''

        # Période de mise à jour
        self.periode = 0.0166
        # Balle
        self.centre = centre
        self.rayon = random.randint(r[0], r[1])
        self.delta = 90 / (sec * 60)
        self.alfa = 0
        self.ball = [0, 0]
        # Score
        self.score = 10
        self.score_rnd = score_rnd
        self.t_score = time()
        # Raquette
        self.bat = [x1, y1]
        self.bat_speed = 1/(60*sec)
        self.sens = 1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = (x2 - x1) * self.bat_speed
        self.dy = (y2 - y1) * self.bat_speed
        # Nom
        self.create_name()
        # Le message à envoyer
        self.simul = {}
        self.animation_thread()

    def animation_thread(self):
        t = threading.Thread(target=self.animation)
        t.start()

    def animation(self):
        while 1:
            sleep(self.periode)
            self.alfa += self.delta
            self.ball_simul()
            self.score_simul()
            self.bat_simul()
            self.create_simul()

    def create_name(self):
        self.name = "s" + str(int(100*time()))[5:]
        print("Mon nom est {}".format(self.name))

    def create_simul(self):
        '''le message prêt à être envoyer
        msg = {"joueur": {  "my_name":       gl.my_name,
                            "ball_position": get_ball_position(),
                            "my_score":      get_my_score(),
                            "bat_position":  get_bat_position(),
                            "reset":         get_reset()
                 }}
                     '''
        self.simul =    {"joueur": {    "reset":       0,
                                        'ball_position': self.ball,
                                        'bat_position': self.bat,
                                        'my_score': self.score,
                                        'my_name': self.name}
                        }

    def print_some(self):
        print(self.simul)

    def ball_simul(self):
        '''Met à jour les coordonnées de la balle,
        qui tourne en rond, autour du centre.'''

        # radians
        a_r = (self.alfa / 180) * 3.14
        x = math.sin(a_r) * self.rayon
        y = math.cos(a_r) * self.rayon

        x = (x + self.centre[0])
        y = (y + self.centre[1])

        x = round(x, 2)
        y = round(y, 2)

        self.ball = [x, y]

    def score_simul(self):
        '''Le score va diminué au hazard, puis repasse à10 si <0.'''

        up = random.randint(0, self.score_rnd)
        if up == 1:
            self.score -= up
        if self.score < 0:
            self.score = 0
        # Reset du score
        if self.score == 0 and time() - self.t_score > 3:
            self.score = 10

    def bat_simul(self):
        '''La bat va de x1,y1 à x2,y2 en self.bat_speed secondes par frames
        et retour.'''

        x = self.bat[0]
        y = self.bat[1]

        x += self.sens * self.dx
        y += self.sens * self.dy

        if x > self.x2:
            self.sens = -1
        if x < self.x1:
            self.sens = 1

        self.bat[0] = round(x, 2)
        self.bat[1] = round(y, 2)


if __name__ == "__main__":

    # Nombre de joueur à simuler maxi 9
    n_p = 9
    print("Simulation de {} joueurs".format(n_p))

    #                    r     centre  sec score_rnd  x1  y1  x2  y2
    play_list = [   ( (3, 7), (-5, -5), 1,   160,      5, -2,  9, 2 ),
                    ( (2, 5), (-3, -2), 2,   100,      4,  2,  7, 4 ),
                    ( (2, 7), (-1, -1), 3,   150,      2,  6,  6, 10 ),
                    ( (2, 6), (0,  0),  4,   200,     -2,  9,  2, 4 ),
                    ( (2, 4), (1,  1),  5,   300,     -4,  5,  0, 1 ),
                    ( (2, 3), (2,  2),  6,   130,     -5,  1, -1,-4 ),
                    ( (2, 9), (3,  3),  7,   110,     -1, -3,  3, 1 ),
                    ( (1, 9), (4,  4),  8,   80,       1,  0,  5, -4 ),
                    ( (1, 5), (4,  5),  9,   250,      3,  2,  8, -8 )]

    for p in range(n_p):
        Player( play_list[p][0],
                play_list[p][1],
                play_list[p][2],
                play_list[p][3],
                play_list[p][4],
                play_list[p][5],
                play_list[p][6],
                play_list[p][7])
        sleep(1)  # pour créer des noms différents

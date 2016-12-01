#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## player_simul.py


from time import sleep
import threading


class BatSimul:
    '''Simulation des bats level 10 de MPFF.
    Tourne à 60 Hz
    '''

    def __init__(self, sec, x1, y1, x2, y2):
        '''sec != 0'''

        # Période de mise à jour
        self.periode = 0.0166

        # Raquette
        self.bat = [x1, y1]
        bat_speed = 1/(60*sec)
        self.sens_x = 1
        self.sens_y = 1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = (x2 - x1) * bat_speed
        self.dy = (y2 - y1) * bat_speed

        self.animation_thread()

    def animation_thread(self):
        self.t = threading.Thread(target=self.animation)
        self.t.start()

    def animation(self):
        while 1:
            sleep(self.periode)
            self.bat_simul()

    def bat_simul(self):
        '''La bat va de x1,y1 à x2,y2 en self.bat_speed secondes par frames
        et retour.'''

        x = self.bat[0]
        y = self.bat[1]

        x += self.sens_x * self.dx
        y += self.sens_y * self.dy

        # TODO refaire les dessins pour vérifier les formules
        if self.x1 < self.x2 and self.y1 < self.y2:
            if x < self.x1:
                self.sens_x = 1
                self.sens_y = 1
            if x > self.x2:
                self.sens_x = -1
                self.sens_y = -1

        if self.x1 < self.x2 and self.y2 < self.y1:
            if x < self.x1:
                self.sens_x = 1
                self.sens_y = -1
            if x > self.x2:
                self.sens_x = -1
                self.sens_y = 1

        if self.x2 < self.x1 and self.y1 < self.y2:
            if x < self.x2:
                self.sens_x = 1
                self.sens_y = -1
            if x > self.x2:
                self.sens_x = -1
                self.sens_y = 1

        if self.x2 < self.x1 and self.y2 < self.y1:
            if x < self.x2:
                self.sens_x = -1
                self.sens_y = -1
            if x > self.x2:
                self.sens_x = 1
                self.sens_y = 1

        self.bat[0] = round(x, 2)
        self.bat[1] = round(y, 2)


if __name__ == "__main__":

    SPEED = [1,2,3,4,5,6,7,8,9,10]

    DOWN = [[-6.14, -7.1],
            [-9.24, -2.01],
            [-8.70, 3.45],
            [-5.0, 7.79],
            [0.65, 9.31],
            [5.85, 7.27],
            [8.79, 2.53],
            [8.7, 3.36],
            [8.7, -2.35],
            [5.79, -7.21]]

    UP = [  [0.41, -9.23],
            [-5.05, -7.77],
            [-8.40, -3.27],
            [-8.95, 2.35],
            [-5.66, 7.26],
            [-0.88, 9.32],
            [5.03, 7.71],
            [8.40, -3.44],
            [5.0, -7.73],
            [-0.37, -9.21]]

    bat_simul = []
    for num in range(10):
        sim = BatSimul(SPEED[num], DOWN[num][0], DOWN[num][1],
                                     UP[num][0],   UP[num][1])
        bat_simul.append(sim)

    while 1:
        for p in range(10):
            print(bat_simul[2].bat)
            sleep(0.02)

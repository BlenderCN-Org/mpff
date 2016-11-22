#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## game.py

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
game.py

Définit le Game Play

Les try sont nécessaires car les objets appelés ne sont pas toujours présent
dans les scènes à l'instant où ils sont appelés.
L'important est qu'il n'y a pas de pass
'''

import GameLogic as gl
from time import sleep
from random import uniform
from scripts import rank_display
from scripts import message


def main():
    '''La scène Labomedia est toujours en background.'''

    scenes = gl.getSceneList()
    R_B_keys()
    print_some()
    set_resolution(scenes)
    # mon nom a été capturé
    if gl.my_name_ok == 1:
        if gl.state == "play":
            # Plus de name ou rank
            for scn in scenes:
                if "Name" in scn.name:
                    scn.end()
                if "Rank" in scn.name:
                    scn.end()
            # Ajout de la scène de jeu au bon niveau
            set_good_level_scene(scenes)

            # Niveau 1
            if gl.level == 1:
                level_1_main(scenes)

            # Pour tous les autres niveaux
            else:
                for scn in scenes :
                    if "_players" in scn.name :
                        positive_score()
                        set_score()
                        other_bat_position()
                        ball_position()
                        ball_out()
                        bat_block()
    # Rank
    if gl.state == "Rank":
        overlay_scene_rank(scenes)
        rank_display.main()
        display_rank_level1(scenes)

def set_resolution(scenes):
    '''Text resolution.'''
    gl.help_obj.resolution = 16.0 # resolution is normaly 1.0 / 72 dpi

def set_good_level_scene(scenes):
    '''Lance la scene au bon niveau si un joueur arrive ou quitte le jeu.'''

    # La bonne scène est-elle affichée ?
    scene_ok = 0
    for scn in scenes :
        if scn.name == str(gl.level) + "_players" :
            scene_ok = 1

    # Si la scène n'est pas ok
    if scene_ok == 0:

        # Suppression de la mauvaise scène en cours, c'est forcément une scène avec "_players"
        for n in range(1, 11):
            for scn in scenes :
                if scn.name == str(n) + "_players" :
                    scn.end()
                    print("Suppression de la scène", str(n) + "_players")
        # Lancement du bon niveau
        overlay_scene(str(gl.level) + "_players")
        # Je viens de demander l'ajout de la scène, elle ne sera effective qu'à la frame suivante
        print("Ajout de la scène ", str(gl.level))

def overlay_scene(scn, overlay=1):
    '''Note de la doc:
    This function is not effective immediately, the scene is queued and added
    on the next logic cycle where it will be available from getSceneList.
    Overlay = 1: overlay
    Overlay = 0: underlay
    '''

    gl.addScene(scn, overlay)

def level_1_main(scenes):
    '''Machine n'est pas géré par le serveur
    donc main() particulier pour le level 1.
    '''

    positive_score()
    set_score()
    bat_block()
    ball_out()
    classement_level1(scenes)
    # La bat auto est active si pas de scène Rank
    if gl.level1_rated == 0:
        automatic_bat(scenes)

def bat_block():
    '''Bloque ou active ma bat.
    - Active ma bat ou début d'une partie.
    - Bloque ma bat si j'ai perdu, donc que mon score = 0
    '''

    try:
        if gl.goal[gl.I_am]["score"] == 0:
            gl.block = 1
        elif gl.goal[1]["score"] == 0 and gl.level == 1:
            gl.block = 1
        else:
            gl.block = 0

        if gl.block == 0:
            gl.bat[gl.I_am]["activ"] = 1
        if gl.block == 1:
            gl.bat[gl.I_am]["activ"] = 0
    except:
        pass
        #print("Try n°7")

def display_rank_level1(scenes):
    '''Comptage du temps d'affichage seulement level 1.'''

    gl.tempo_rank_level1 += 1
    if gl.tempo_rank_level1 == 2:
        print("Rank Text \n{}".format(gl.text))

    if gl.tempo_rank_level1 > 240:
        # Fin de la scène Rank
        del_rank_scene(scenes)
        reset_variables()

def classement_level1(scenes):
    '''Classement du joueur et de la machine au niveau 1. 2 Cas:'''

    if gl.goal[0] and gl.goal[1]:
        if gl.level1_rated == 0:
            # Cas 1: je gagne, machine perds
            if gl.goal[1]["score"] == 0: # score machine
                gl.classement_level1['machine']  = 2
                gl.classement_level1[gl.my_name] = 1
                # Je ne repasserai plus par ici
                gl.level1_rated = 1
                # demande de la scèneRank
                gl.state = "Rank"
                print("Dans niveau 1, j'ai gagné")

            # Cas 2: je perds, machine gagne
            if gl.goal[0]["score"] == 0: # mon score
                gl.classement_level1['machine']  = 1
                gl.classement_level1[gl.my_name] = 2
                # Je ne repasserai plus par ici
                gl.level1_rated = 1
                # demande de la scèneRank
                gl.state = "Rank"
                print("Dans niveau 1, machine a gagné")
        else:
            # calcul du temps d'affichage
            display_rank_level1(scenes)

def overlay_scene_rank(scenes):
    '''Ajoute la sceène Rank en overlay.'''

    scene_list = []
    for scn in scenes :
        scene_list.append(scn.name)

    if not "Rank" in scene_list:
        # Overlay la scène Rank
        gl.addScene("Rank")

def del_rank_scene(scenes):
    '''Supprime la scène Rank.'''

    for scn in scenes :
        if "Rank" in scn.name:
            scn.end()
            print("Suppression de Rank")

def reset_variables():
    '''Reset de variables pour repartir à zéro.'''

    print("Reset variables in game.py")
    try:
        gl.goal[0]["score"] = 10
        gl.goal[1]["score"] = 10
    except:
        print("Try n°8")

    gl.tempo_globale = 0
    gl.level1_rated = 0
    gl.classement_level1 = {}
    gl.tempo_rank_level1 = 0
    # Le dictionnaire de classement des joueurs
    gl.classement = {}
    gl.block = 0
    gl.state = "play"

def ball_out():
    '''Remet la Ball dans le jeu si la balle sort du jeu.'''

    try:
        if gl.ball.localPosition[0] < -15:
            gl.ball.localPosition = [3, -3, 1]
        elif gl.ball.localPosition[0] > 15:
            gl.ball.localPosition = [3, -3, 1]
        elif gl.ball.localPosition[1] < -15:
            gl.ball.localPosition = [3, -3, 1]
        elif gl.ball.localPosition[1] > 15:
            gl.ball.localPosition = [3, -3, 1]
    except:
        pass
        #print("Try n°3")

def automatic_bat(scenes):
    '''Seulement niveau 1. Mouvement auto de la raquette machine.'''

    for scn in scenes :
        if scn.name == "1_players":
            try:
                y = 0.7 * gl.ball.localPosition[1]
                gl.bat[1].localPosition = [9.5, y, 1]
            except:
                print("Try n°2")

def set_score():
    '''Maj des scores avec les valeurs du server.'''

    if gl.level > 1:
        for player in range(gl.level):
            if player != gl.I_am:
                try:
                    gl.goal[player]["score"] = gl.score[player]
                except:
                    print("Try n°1")

def other_bat_position():
    '''Définir les positions des raquettes des autres joueurs, pas pour moi,
    avec valeur du server.
    '''

    for player in range(gl.level):
        try:
            if player != gl.I_am:
            # les clés de gl.bat_position sont des str
                gl.bat[player].localPosition = [gl.bat_position[str(player)][0],
                                                gl.bat_position[str(player)][1],
                                                1]
        except:
                print("Try n°6")

def positive_score():
    '''Tous les scores doivent être >= 0'''

    if gl.level == 1:
        b = 2 # le niveau 1 a 2 joueurs
    else:
        b = gl.level

    for g in range(b):
        try:
            if gl.goal[g]["score"] <= 0:
                gl.goal[g]["score"] = 0
        except:
            pass
            #print("Try n°4")

def ball_position():
    '''Placer la balle si je ne suis pas master.
    Le premier dans la liste des jouers est toujours le master,
    sauf la machine.
    '''

    if gl.I_am != 0 :
        # Disable rigid body de la balle
        gl.ball["master"] = False
        # Set position
        gl.ball.localPosition = [gl.ball_position_server[0], gl.ball_position_server[1], 1]

def R_B_keys():
    '''Pour les touches R et B.'''

    if gl.cube_obj["ball"]:
        gl.cube_obj["ball"] = False
        gl.ball.localPosition = [3, -3, 1]

    if gl.cube_obj["reset"]:
        gl.cube_obj["reset"] = False
        reset_variables()
        # Envoi au sever de {"reset":1}
        msg = {"reset":1}
        # TODO
        network.send_to_server(msg)

def print_some():
    '''Print toutes les s des valeurs permettant de debugguer.'''

    if gl.tempoDict["frame_60"].tempo == 60:
            print(  "Mon nom: {}, mon n°: {}, state: {}".format(\
                    gl.my_name[:-10], gl.I_am, gl.state))
            #print("FrameRate =", int(gl.getAverageFrameRate()))

# MultiPass For Freedom

Pong en réseau local jusqu'à 10 joueurs. Réalisé avec [blender](https://www.blender.org/) et [python 3.4](https://www.python.org/)

![10 joueurs](https://github.com/sergeLabo/mpff/blob/master/doc/mpff_10.png)
![3 joueurs](https://github.com/sergeLabo/mpff/blob/master/doc/mpff_02.png)

Cette version utilise [twisted](https://twistedmatrix.com/trac/) en python 3

### Genèse du jeu

Ce jeu est un exercice sur les réseaux. Un jeu hyper simple créé dans Blender, et jusqu'à 10 joueurs sur un réseau local.

Dans cette solution , le jeu dans Blender n'est pas simple. Il comporte 14 scènes, les scènes x_players sont construites par copie de la plupart des objets, et un nommage qui permet facilement d'accéder aux objets de Blender dans les scripts python.

Les scripts python doivent être créés / modifiés dans un éditeur externe (par exemple Geany) et n'ont pas besoin d'être rechargés dans Blender. Seuls 2 scripts sont chargés dans Blender en tant que module, et ces scripts ne doivent jamais être modifiés, à savoir main_once.py et main_always.py

### Copyright

Copyright (C) Labomedia May 2012

Pour plus détails, voir le fichier Copyright

### Détails
Sur le wiki: [MultiPass For Freedom]( https://github.com/sergeLabo/mpff/wiki)

### Multicast

Tous les PC doivent être sur le même réseau local, avec un routeur qui supporte le multicast.

### Testé sur

Debian Jessie 8.3 avec Blender 2.72

### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Installation de twisted pour python 3

~~~text
sudo pip3 install twisted
~~~

##### ou

~~~text
sudo apt-get install python3-dev python3-setuptools
~~~

Les sources de twisted comprennent les versions pour python2 et python3.

Télécharger les sources à https://github.com/twisted/twisted ou

~~~text
wget https://github.com/twisted/twisted
~~~

Dans le dossier, ouvrir un terminal:

~~~text
sudo python3 setup.py install
~~~

##### ou

Dans votre dossier projets, ouvrir un terminal:
git clone https://github.com/twisted/twisted.git
cd twisted
sudo python3 setup.py install
~~~

##### ou

Sur Debian Jessie, activer les backport en ajoutant à votre sources.list

~~~text
deb http://ftp.de.debian.org/debian/ jessie-backports main
deb-src http://ftp.de.debian.org/debian/ jessie-backports main
~~~

puis installer le paquet python3-twisted


### Lancement du jeu

Le jeu se lance avec les lanceurs du dossier principal. Ces lanceurs doivent être excécutable.

Lancer un seul server sur le réseau, puis lancer des jeux. Un serveur doit absolument être lancé avant les jeux.

Il est possible de lancer plusieurs jeux sur le même PC, mais un seul jeu peut-être utilisé pour jouer.

### Pour jouer

- Space = Aide
- R = Reset
- B = Replacer la balle
- Haut Bas pour déplacer la raquette

### Test de 10 joueurs sur un seul PC

#####Installer xterm

~~~text
sudo apt-get install xterm
~~~

##### Modifier mpff.ini

Définir

name_capture = 0

Lancer un serveur avec clic_to_run_server, puis lancer avec clic_to_run_10_game
Toutes les raquettes se déplacent en auto. Il n'est pas possible de jouer.

Il est possible de fermer tous les terminaux xterm avec:

~~~text
killall xterm
~~~

Remettre

name_capture = 0

quand vous avez fini de vous amuser !

### Bug connu

* Le serveur doit être lancé obligatoirement avant de lancer des jeux.
* Les déconnexions ne sont pas gérées.

### TODO

* La Pile ne sert à rien, mais ne gêne pas
* Globalement beaucoup de fonctions sont très perfectibles
* Gérer le niveau 1 par le serveur

### Merci à:

* Labomedia

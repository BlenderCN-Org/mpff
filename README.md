# MultiPass For Freedom

Pong en réseau local jusqu'à 10 joueurs. Réalisé avec [blender](https://www.blender.org/) et [python 3.4](https://www.python.org/)

![10 joueurs](https://github.com/sergeLabo/mpff/blob/master/doc/mpff_10.png)
![3 joueurs](https://github.com/sergeLabo/mpff/blob/master/doc/mpff_02.png)

Cette version utilise [twisted](https://twistedmatrix.com/trac/) en python 3

### Genèse du jeu

Ce jeu est un exercice sur les réseaux. Un jeu hyper simple créé dans Blender,

et jusqu'à 10 joueurs sur un réseau local.

Dans cette solution , le jeu dans Blender n'est pas simple. Il comporte 14 scènes,
les scènes x_players sont construites par copie de la plupart des objets, et un
nommage qui permet facilement d'accéder aux objets de Blender dans les scripts python.

Les scripts python doivent être créés / modifiés dans un éditeur externe (par exemple Geany)
et n'ont pas besoin d'être rechagés dans Blender. Seuls 2 scripts sont chargés
dans Blender en tant que module, et ces scripts ne doivent jamais être modifiés,
à savoir main_once.py et main_always.py

### Copyright

Copyright (C) Labomedia May 2012

Pour plus détails voir le fichier Copyright

### Détails
Sur le wiki: [MultiPass For Freedom]()

### Multicast

Tous les PC doivent être sur le même réseau local,
avec un routeur qui supporte le multicast

###Testé sur

Debian Jessie 8.3 avec Blender 2.72

### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Installation de twisted pour python 3
##### Dépendances

~~~text
 sudo apt-get install python3-dev python3-setuptools
~~~

##### Install

Les sources de twisted comprennent les versions pour python2 et python3.

Télécharger les sources à https://github.com/twisted/twisted

Dans le dossier, ouvrir un terminal:

~~~text
sudo python3 setup.py install
~~~

ou

Dans votre dossier projets, ouvrir un terminal:

~~~text
git clone https://github.com/twisted/twisted.git
cd twisted
sudo python3 setup.py install
~~~

### Lancement du jeu

Le jeu se lance avec les lanceurs du dossier principal. Ces lanceurs doivent être excécutable.

Lancer un seul server sur le réseau, puis lancer des jeux. Un serveur doit absolument être lancé avant les jeux.

Il est possible de lancer plusieurs jeux sur le même PC, mais un seul jeu peut-être utilisé pour jouer.

### Pour jouer

- Space = Aide
- R = Reset
- B = Replacer la balle
- Haut Bas pour déplacer la raquette

### Test en simulant des joueurs


### Bug connu

- Le serveur doit être lancé obligatoirement avant de lancer des jeux.
- Les déconnexions ne sont pas gérées.

### Merci à:

 - Labomedia

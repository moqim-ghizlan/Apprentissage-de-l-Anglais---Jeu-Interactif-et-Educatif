# Apprentissage Anglais
![Image text](https://cdn.discordapp.com/attachments/639870893710901264/954304419296579604/logo-removebg-preview.png)
***
## Bienvenue sur le README de notre site web.

### Explication du projet

Ce projet est un site web permettant d'apprendre l'anglais de façon ludique grâce à un jeu de type escape game contenant différents mini-jeux. Ces activités permettent d'apprendre la formation des phrases et des textes en anglais, incluant la ponctuation.

### Le but du projet

Dans le cadre d’un projet tutoré de 2ème année, nous avons développé ce site web avec une version mobile à la demande de notre professeur d’anglais, Mme. LEFORESTIER. Elle souhaitait proposer une plateforme ludique en ligne pour permettre à ses élèves de s’exercer à la formation de phrases et des textes en anglais, incluant la ponctuation. Une base de données est utilisée pour relier les différents programmes développés.

### Les membres
* **OMARI Redwan** @DooM41 (chef de projet)
* **GHIZLAN Moqim** @moqim.ghizlan (vice chef de projet)
* **TARROU Axel** @wormaf
* **GIRAULT Pierre** @pierre04042002
* **ESSALAK Bilal** @bilalessalak
* **LABBE Valentin** @Valentin-Labbe
***

## Les commandes

1. Clonez le projet dans le répertoire de votre choix avec la commande :
```
$ git clone https://gitlab.com/moqim.ghizlan/apprentissage-anglais-g2.git
```

2. Dans le dossier `apprentissage-anglais-g2`, lancez la commande pour créer un environnement virtuel :
```
$ virtualenv env
```
```
$ source env/bin/activate
```

3. Téléchargez les dépendances nécessaires :
```
$ pip install -r requirements.txt
```

4. Lancez Flask :
```
$ python run.py drop # pour supprimer les tables et colonnes existantes.

$ python run.py create # pour créer la base de données.

$ python run.py init # pour remplir les tables avec des données de base (eleve@eleve.eleve, etc.).

$ python run.py run

$ python run.py start # pour tout exécuter automatiquement et lancer le serveur.

$ python run.py # pour lancer le serveur en mode normal.
```

5. Ouvrez votre navigateur et accédez au site via :
```
$ localhost:5000
```
ou
```
$ http://127.0.0.1:5000/
```

6. Pour lancer le jeu, utilisez :
```
$ node apprentissage-anglais-g2\app\static\Build_Game\serveur.js
```

## Deadline

### Pour le site web
Nous aurions voulu ajouter une fonctionnalité permettant la communication entre le professeur et son élève, ainsi qu’entre le professeur et l’administrateur. Cela aurait permis de remonter des problèmes et de suivre les élèves. Cependant, par manque de temps, nous avons dû renoncer à cette fonctionnalité.

### Pour le jeu
Nous aurions voulu ajouter :
- Une fonctionnalité permettant l'ajout de nouveaux tilesets pour personnaliser la carte.
- L’intégration de mini-jeux supplémentaires dans la plateforme d'édition de cartes.

***

Merci pour votre intérêt dans ce projet ! Si vous avez des questions, n'hésitez pas à contacter l'équipe.

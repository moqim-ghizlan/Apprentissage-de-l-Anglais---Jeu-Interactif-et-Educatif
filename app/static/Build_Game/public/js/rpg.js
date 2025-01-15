
//const fs = require('fs');
//const path = "./maps/premiere.json"
//const storeData = (data, path) => {
//    try {
//        fs.writeFileSync(path, JSON.stringify(data))
//    } catch (err) {
//        console.error(err)
//    }
//
//const loadData = (path) => {
//    try {
//        return fs.readFileSync(path, 'utf8')
//    } catch (err) {
//        console.error(err)
//        return false
//    }
//}
//
//let data = loadData(path)
//console.log(data)

//const { response } = require("express");


//const fs = require('fs');
//var data = fs.readFileSync('./../maps/premiere.json', 'utf8')
//console.log(data)
//let mapData = JSON.parse(data)
//console.log(mapData.tileset)
//
//let test = {"test": 1, "test2" : [1, 2, 3, 4, 5, 6]}
//let AEcrir = JSON.stringify(test)
//
//fs.writeFileSync('./../maps/test.json', AEcrir )




//base de données
//const dbName = 'main.db'    // à changer plus tard
//let db = connexionDB()

// fonctions pour la base de données

function getMapData(carte) {
	const nomeC = carte
	let data  ={
		carteRecherche : nomC
	}

	let options = {
		methode : 'POST',
		headers : {"Content-type" : "application/json; charset = UTF-8"},
		body : JSON.stringify(data)
	}
	const promise = fetch('/data', options);
	promise.then(response => {
		if(!response.ok){
			console.error(response)
		} else {
			return response.json();
		}
	}).then(result => {
		console.log(result);
	})
}


//####################################


// instance de la carte
var map = new Carte("premiere");

// rajouter une personne à la carte
let personne = new Personnage("personage.png", 3, 1, DIRECTION.BAS, map);
map.addPersonnage(personne);
let joueur = map.getPersonnage();


window.onload = function() {
	let canvas = document.getElementById('canvas');
	let ctx = canvas.getContext('2d');

	canvas.width = map.getLargeur() * 32;
	canvas.height = map.getHauteur() * 32;

	// #################### test #################

	setInterval(function() {
		map.dessinerMap(ctx);
	}, 40);



	// Gestion du clavier
	window.onkeydown = function(event) {
		let e = event;
		let key = e.which;
		//alert(key);
		switch(key) {
			case 38 : //flèche haut
				joueur.deplacer(DIRECTION.HAUT, map);
				break;
			case 40 : // Flèche bas
				joueur.deplacer(DIRECTION.BAS, map);
				break;
			case 37 : //flèche gauche
				joueur.deplacer(DIRECTION.GAUCHE, map);
				break;
			case 39 : //flèche droit
				joueur.deplacer(DIRECTION.DROITE, map);
				break;
			default : 
				//alert(key);
				return true;
		}
		return false;
	}
}


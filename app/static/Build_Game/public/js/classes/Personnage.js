const DIRECTION = {
    "BAS" : 0,
    "GAUCHE" : 1,
    "DROITE" : 2,
    "HAUT" : 3
}

var DUREE_ANIMATION = 4;
var DUREE_DEPLACEMENT = 15;

function Personnage(url, x, y, direction, carte) {
	this.x = x; // (en cases)
	this.y = y; // (en cases)
	this.direction = direction;
    this.etatAnimation = -1;
    this.carte = carte;
    //this.largeur = 32;
    //this.hauteur = 32;
	
	// Chargement de l'image dans l'attribut image
	this.image = new Image();
	this.image.referenceDuPerso = this;
	this.image.onload = function() {
        //console.log(this.complete);
		if(!this.complete) 
			throw "Erreur de chargement du sprite nommé \"" + url + "\".";
		
		// Taille du personnage
		this.referenceDuPerso.largeur = this.width / 4;
		this.referenceDuPerso.hauteur = this.height / 4;
	}
	this.image.src = "images/sprites/" + url;

}

Personnage.prototype.dessinerPersonnage = function(context) {
    //if(this.x == 0) this.x = 1;
    //if(this.y == 0) this.y = 1;

    // ############## test de fluidité #####################
    
    var frame = 0; // Numéro de l'image à prendre pour l'animation
    var decalageX = 0, decalageY = 0; // Décalage à appliquer à la position du personnage
    if(this.etatAnimation >= DUREE_DEPLACEMENT) {
        // Si le déplacement a atteint ou dépassé le temps nécessaire pour s'effectuer, on le termine
        this.etatAnimation = -1;
    } else if(this.etatAnimation >= 0) {
        // On calcule l'image (frame) de l'animation à afficher
        frame = Math.floor(this.etatAnimation / DUREE_ANIMATION);
        if(frame > 3) {
            frame %= 4;
        }
        
        // Nombre de pixels restant à parcourir entre les deux cases
        var pixelsAParcourir = 32 - (32 * (this.etatAnimation / DUREE_DEPLACEMENT));
        
        // À partir de ce nombre, on définit le décalage en x et y.
        if(this.direction == DIRECTION.HAUT) {
            decalageY = pixelsAParcourir;
        } else if(this.direction == DIRECTION.BAS) {
            decalageY = -pixelsAParcourir;
        } else if(this.direction == DIRECTION.GAUCHE) {
            decalageX = pixelsAParcourir;
        } else if(this.direction == DIRECTION.DROITE) {
            decalageX = -pixelsAParcourir;
        }
        
        this.etatAnimation++;
    }
    

    // ############## fin de test de fluidité #####################
	context.drawImage(
        this.image, 
        this.largeur * frame, this.direction * this.hauteur, // Point d'origine du rectangle source à prendre dans notre image
        this.largeur, this.hauteur, // Taille du rectangle source (c'est la taille du personnage)
        (this.x * 32) - (this.largeur / 2) + 16 + decalageX, (this.y * 32) - this.hauteur + 40 + decalageY, // Point de destination (dépend de la taille du personnage)
	    32, 32
    );
    //console.log(0, this.direction * this.hauteur, // Point d'origine du rectangle source à prendre dans notre image
    //this.largeur, this.hauteur, // Taille du rectangle source (c'est la taille du personnage)
    //(this.x * 32) - (this.largeur / 2) + 16, (this.y * 32) - this.hauteur + 24, // Point de destination (dépend de la taille du personnage)
    //32, 32);
}


Personnage.prototype.getCoordonneesAdjacentes = function(direction){
    let coord = {'x': this.x, 'y': this.y};
    console.log(this.x, this.y);
    console.log(this.carte.getNumeroTuile(this.x, this.y));
    switch(direction){
        case DIRECTION.BAS:
            coord.y++;
            break;
        case DIRECTION.GAUCHE:
            coord.x--;
            break;
        case DIRECTION.DROITE:
            coord.x++;
            break;
        case DIRECTION.HAUT:
            coord.y--;
            break;
    }
    return coord;
}

Personnage.prototype.deplacer = function(direction, map){

    // On ne peut pas se déplacer si un mouvement est déjà en cours !
    if(this.etatAnimation >= 0) {
        return false;
    }

    //on change la direction du personnage
    this.direction = direction;

    //on vérifie que la case demandée est bien située dans la carte
    let prochaineCase = this.getCoordonneesAdjacentes(direction);

    if (this.carte.murs.includes(this.carte.getNumeroTuile(prochaineCase.x,prochaineCase.y))){
        return false;
    }

    if (prochaineCase.x < 0 || prochaineCase.y < 0 || prochaineCase.x >= map.getLargeur() || prochaineCase.y >= map.getHauteur()){
        //on return un booléen indiqant que le déplacemnet ne s'est pas fait 
        return false;
    }
    // on fait le déplacement 
    // On commence l'animation
    this.etatAnimation = 1;
    this.x = prochaineCase.x;
    this.y = prochaineCase.y;

    //déplacement fait 
    return true
}
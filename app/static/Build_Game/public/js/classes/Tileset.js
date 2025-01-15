function Tileset(url) {

	// Chargement de l'image dans l'attribut image
	this.image = new Image();
	this.image.referenceDuTileset = this;
	this.image.onload = function() {
		if(!this.complete) 
			throw new Error("Erreur de chargement du tileset nommé \"" + url + "\".");
        // Largeur du tileset en tiles
        this.referenceDuTileset.largeur = this.width / 32;
	}
	this.image.src = "images/tilesets/" + url;
}

// Méthode de dessin du tile numéro "numero" dans le contexte 2D "context" aux coordonnées x et y
Tileset.prototype.dessinerTile = function(numero, context, xDestination, yDestination) {
	
    //console.log(numero);
    let xSourceEnTiles = numero % this.largeur;
    if(xSourceEnTiles == 0) xSourceEnTiles = this.largeur;
    let ySourceEnTiles = Math.ceil(numero / this.largeur);
    //console.log(xSourceEnTiles, ySourceEnTiles);
    let xSource = (xSourceEnTiles - 1) * 32;
    let ySource = (ySourceEnTiles - 1) * 32;
    //console.log(xSource,ySource, xDestination, yDestination);   
    context.drawImage(this.image, xSource, ySource, 32, 32, xDestination, yDestination, 32, 32);
    //console.log(this.image, xSource, ySource, 32, 32, xDestination, yDestination, 32, 32);
}
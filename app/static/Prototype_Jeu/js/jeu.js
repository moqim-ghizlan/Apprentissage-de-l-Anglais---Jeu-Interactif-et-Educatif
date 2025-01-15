let cnv = document.getElementById("cnv");
let ctx = cnv.getContext("2d");

cnv.width = (window.innerWidth * 100) / 100;
cnv.height = (window.innerHeight * 100) / 100;
ctx.imageSmoothingEnabled = false;

let filename = "map";

async function createMap(file){
	let response = await fetch(file);
	let result = await response.json();

	let mapdata = result[filename];

	let tileset = new Image();
	tileset.src = mapdata.tileset.path;
	tileset.onload = drawBackground;

	let tileSize = mapdata.tileset.tileResolution; // Résolution en pixel de la tile sur l'image (8x8)
	let imageNumTiles = mapdata.tileset.tilePerLine; // Nombre de tile par ligne sur le tileset
	let rowTileCount = mapdata.background.length; // Nombre de tile par ligne sur la map (json)
	let colTileCount = mapdata.background[0].length; // Nombre de tile par colonne sur la map (json)
	let canvasTileWidth = cnv.width / colTileCount;
	let canvasTileHeight = cnv.height / rowTileCount;

	function drawBackground(){
	   	for(let r = 0; r < rowTileCount; r++){
	      	for (let c = 0; c < colTileCount; c++){
	         	let tile = mapdata.background[r][c];
	         	let tileRow = (tile / imageNumTiles) | 0; // Bitwise OR operation
	         	let tileCol = (tile % imageNumTiles) | 0;
	         	ctx.drawImage(tileset, (tileCol * tileSize), (tileRow * tileSize), tileSize - 0.01, tileSize - 0.01, (c * canvasTileWidth), (r * canvasTileHeight), canvasTileWidth, canvasTileHeight);
	          	// drawImage(img, sourceX, sourceY, sourceWidth, sourceHeight, destinationX, destinationY, destinationWidth, destinationHeight)
	      		// Eventuellement ajouter "- 0.1" au tileSize de sourceWidth et sourceHeight
	      	}
	   	}
	}

	function drawElement(){
		for(let item in mapdata.item){
			let position = item.position;
			let index = item.index;
	        ctx.drawImage(tileset, (tileCol * tileSize), (tileRow * tileSize), tileSize - 0.01, tileSize - 0.01, (position[0] * canvasTileWidth), (position[1] * canvasTileHeight), canvasTileWidth, canvasTileHeight);		
		}
	}

	class Sprite{
		constructor(){
			this.position = mapdata.sprite.starting; // Position initiale du sprite
			this.size = mapdata.sprite.resolution; // Résolution en pixel du sprite || USE LATER : let spriteCount = mapdata.sprite.amount; // Nombre d'animation du sprite
			this.facing = 0; // Par défaut le sprite regarde vers le haut
			this.initImg();
		}

		async initImg(){
			this.spriteImg = new Image();
			this.spriteImg.src = mapdata.sprite.path;
			await this.spriteImg.decode();
			this.drawSprite(this.position, this.facing); 
		}

		drawSprite(position, facing){
			ctx.clearRect(0, 0, cnv.width, cnv.height);
			drawBackground();
			this.facing = facing;
			// Position : tuple de valeur représentant les indices de la position sur la grille, facing : l'indice du sprite sur l'image
			ctx.drawImage(this.spriteImg, (this.size * facing), 0, this.size, this.size, (position[0] * canvasTileWidth), (position[1] * canvasTileHeight), canvasTileWidth, canvasTileHeight);
			// Un sprite est défini comme une ligne d'images, d'où 0 d'indice de hauteur
		}

		getTileType(position = this.position){
			return mapdata.background[position[1]][position[0]];
		}

		getTileConsistency(position = this.position){
			try{
				let tile = this.getTileType(position);
				return mapdata.tileProperties[tile].consistency;
			}
			catch(error){
				return error;
			}
		}

	}

	sprite = new Sprite();

	window.addEventListener('keydown', function (e){
		switch(e.key){
			case 'ArrowUp':
				if(sprite.position[1] > 0 && (sprite.getTileConsistency([sprite.position[0], sprite.position[1] - 1]) != ("solid" || null))){
					sprite.position[1] -= 1;	
				}	
				sprite.facing = 0;
				break;
			case 'ArrowRight':
				if(sprite.position[0] < colTileCount - 1 && (sprite.getTileConsistency([sprite.position[0] + 1, sprite.position[1]]) != ("solid" || null))){
					sprite.position[0] += 1;
				}
				sprite.facing = 1;
				break;
			case 'ArrowDown':
				if(sprite.position[1] < rowTileCount - 1 && (sprite.getTileConsistency([sprite.position[0], sprite.position[1] + 1]) != ("solid" || null))){
					sprite.position[1] += 1;
				}
				sprite.facing = 2;
				break;
			case 'ArrowLeft':
				if(sprite.position[0] > 0 && (sprite.getTileConsistency([sprite.position[0] - 1, sprite.position[1]]) != ("solid" || null))){
					sprite.position[0] -= 1;
				}
				sprite.facing = 3;
				break;
		}
		sprite.drawSprite(sprite.position, sprite.facing);
		console.log(sprite.getTileConsistency());
		console.log(sprite.backpack);
	}, false);
}

createMap("http://localhost:3000/maps");
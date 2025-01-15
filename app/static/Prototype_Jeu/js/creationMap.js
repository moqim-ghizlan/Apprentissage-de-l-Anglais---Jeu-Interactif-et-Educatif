let firstPageLoad = true;

async function main(map){

	let dbURL = "http://localhost:3000/maps";
	let filename = map;

	let cnv = document.getElementById("cnv");
	let ctx = cnv.getContext("2d");
	let container = document.getElementById("elementList");
	cnv.addEventListener('mousedown', drawTileOnClick, false);

	cnv.width = cnv.offsetWidth; //(window.innerWidth * 100) / 100;
	cnv.height = cnv.offsetHeight; //(window.innerHeight * 100) / 100;
	ctx.imageSmoothingEnabled = false;

	async function saveJSON(url, json){
		fetch(url, {
			method: 'POST',
			headers: {
			  'Accept': 'application/json',
			  'Content-Type': 'application/json'
			},
			body: JSON.stringify(json)
		});
	}

	let response = await fetch(dbURL);
	let result = await response.json();
	console.log(result);
	let mapdata = result[filename];

	let tileSize = mapdata.tileset.tileResolution; // Résolution en pixel de la tile sur l'image (8x8)
	let imageNumTiles = mapdata.tileset.tilePerLine; // Nombre de tile par ligne sur le tileset
	let rowTileCount = mapdata.background.length; // Nombre de tile par ligne sur la map (json)
	let colTileCount = mapdata.background[0].length; // Nombre de tile par colonne sur la map (json)
	let canvasTileWidth = cnv.width / colTileCount;
	let canvasTileHeight = cnv.height / rowTileCount;
	let tileset = new Image();
	tileset.src = mapdata.tileset.path;
	tileset.onload = function drawAll(){
		ctx.clearRect(0, 0, cnv.width, cnv.height);
		showAvailableElements();
		drawBackground();
		drawGrid();
		createMapSelector();
	};

	let mapSelector = document.getElementById("mapSelector");
	mapSelector.onchange = function f(){
		cnv.removeEventListener('mousedown', drawTileOnClick, false);	
		main(mapSelector.value);
	};

	let mapCreator = document.getElementById("createMapButton");
	mapCreator.onclick = function f(){
		createMap(dbURL);
		console.log(mapSelector[Object.keys(result).length].value);
		main(mapSelector[Object.keys(result).length].value);
	}

	let mapDeletor = document.getElementById("deleteMapButton");
	mapDeletor.onclick = function f(){
		deleteMap(mapSelector.value);
	}

	function getMousePos(canvas, evt) {
		var rect = cnv.getBoundingClientRect();
		x = evt.clientX - rect.left;
		y = evt.clientY - rect.top;
		return {x, y};
	}

	function getCanvasTileIndex(x, y){
		x = Math.round(x);
		y = Math.round(y);
		x = Math.floor(x / cnv.offsetHeight / (1 / colTileCount));
		y = Math.floor(y / cnv.offsetWidth / (1 / rowTileCount))
		return {x, y};
	}

	function getCanvasTileCoord(x, y){
		x = x * (cnv.offsetWidth / colTileCount);
		y = y * (cnv.offsetHeight / rowTileCount);
		return {x, y}
	}

	function drawBackground(){
	   	for(let r = 0; r < rowTileCount; r++){
	      	for (let c = 0; c < colTileCount; c++){
	         	let tile = mapdata.background[r][c];
	         	let tileRow = (tile / imageNumTiles) | 0;
	         	let tileCol = (tile % imageNumTiles) | 0;
	         	ctx.drawImage(tileset, (tileCol * tileSize), (tileRow * tileSize), tileSize - 0.01, tileSize - 0.01, (c * canvasTileWidth), (r * canvasTileHeight), canvasTileWidth, canvasTileHeight);
	          	// drawImage(img, sourceX, sourceY, sourceWidth, sourceHeight, destinationX, destinationY, destinationWidth, destinationHeight)
	      		// Eventuellement ajouter "- 0.1" au tileSize de sourceWidth et sourceHeight
	      	}
	   	}
	}

	function showAvailableElements(){
		container.innerHTML = "";
		for(elem of Object.keys(mapdata.tileProperties)){
			let tile  = new Tile(elem, imageNumTiles, tileSize);
		}
	}

	class Tile{

		constructor(index, imageNumTiles, tileSize){
			this.index = index;
			this.tileRowIndex = index % imageNumTiles;
			this.tileColIndex = Math.floor(index / imageNumTiles);
			this.resolution = tileSize;
			this.displayTile();
		}

		displayTile(){			
			let tile = document.createElement("label");
			tile.classList.add("tile");

			let tileCnv = document.createElement("canvas");
			tileCnv.classList.add("tileIcon");
			tileCnv.width = Math.min(container.offsetHeight / (Object.keys(mapdata.tileProperties).length * 1.1)), container.offsetWidth;
			tileCnv.height = Math.min(container.offsetHeight / (Object.keys(mapdata.tileProperties).length * 1.1)), container.offsetWidth;

			let tileSelector = document.createElement("input");
			tileSelector.type = "radio";
			tileSelector.name  = "tileSelector";
			tileSelector.value = [this.index, this.tileRowIndex, this.tileColIndex, this.resolution];
			tileSelector.id = "tileSelector";

			tile.appendChild(tileSelector);
			tile.appendChild(tileCnv);

			let tileContext = tileCnv.getContext("2d");
			tileContext.imageSmoothingEnabled = false;
			tileContext.drawImage(tileset, (this.tileRowIndex * this.resolution), (this.tileColIndex * this.resolution), this.resolution, this.resolution, 0, 0, tileCnv.width, tileCnv.height);

			container.appendChild(tile);
		}
	}

	function drawGrid(){
		ctx.fillStyle = "#000000";
      	for (let c = 0; c < colTileCount; c++){
      		ctx.beginPath();
      		ctx.moveTo(c * canvasTileWidth, 0);
      		ctx.lineTo(c * canvasTileWidth, cnv.height);
      		ctx.stroke();
      		ctx.closePath();
      	}
      	for (let r = 0; r < rowTileCount; r++){
      		ctx.beginPath();
      		ctx.moveTo(0, r * canvasTileHeight);
      		ctx.lineTo(cnv.width, r * canvasTileHeight);
      		ctx.stroke();
      		ctx.closePath();
      	}
	}

	function deleteMap(map){
		delete result[map];
		saveJSON(dbURL, result);
		if(mapSelector.value == null || mapSelector.value == "Select a map"){
			console.log("Impossible de supprimer la map");
			return;
		}
		else{
			main(mapSelector[mapSelector.selectedIndex].value);
			return;
		}
	}

	function createMapSelector(){
		let selectedMapIndex = mapSelector.selectedIndex;
		let selectedMap = null;
		if(selectedMapIndex != -1){
			selectedMap = mapSelector[selectedMapIndex].value;
		}
		
		mapSelector.innerHTML = "";

		let title = document.createElement("option");
		title.innerHTML = "Select a map";
		title.setAttribute("disabled", "");
		if(firstPageLoad){
			title.setAttribute("selected", "");
			firstPageLoad = false;
		}
		mapSelector.appendChild(title);

		let maps = Object.keys(result);
		for(map of maps){
			let elem = document.createElement("option");
			elem.value = map;
			elem.innerHTML = map.toString();
			mapSelector.appendChild(elem);
			if(map == selectedMap){
				elem.setAttribute("selected", "");
			}
		}
	}

	function drawTileOnClick(evt){
		let mousePos = getMousePos(cnv, evt);
		let selectedTile = document.querySelector('input[name="tileSelector"]:checked');

		console.log("cnvTileWidth", canvasTileWidth);
		console.log("cnvTileHeight", canvasTileHeight);

		if(selectedTile){
			let selectedTileData = selectedTile.value.split(","); // [0] : tileType | [1] : tilePosX | [2] : tilePosY | [3] : tileResolution

			let canvasTileIndex = getCanvasTileIndex(mousePos.x, mousePos.y);
			let canvasTilePos = getCanvasTileCoord(canvasTileIndex.x, canvasTileIndex.y);

			ctx.drawImage(tileset, (selectedTileData[1] * selectedTileData[3]), (selectedTileData[2] * selectedTileData[3]) - 0.01, selectedTileData[3], selectedTileData[3], canvasTilePos.x, canvasTilePos.y, canvasTileWidth, canvasTileHeight);
			mapdata.background[canvasTileIndex.y][canvasTileIndex.x] = selectedTileData[0];
			saveJSON(dbURL, result);
		}
	}

	async function createMap(url, filename){

		let mapName = document.getElementById("mapName");
		let mapWidth = document.getElementById("mapWidth");
		let mapHeight = document.getElementById("mapHeight");
		// let tilesPerLine = document.getElementById("tilesPerLine");
		// let mapTileset = document.getElementById("mapTileset");
		// let mapSprite = document.getElementById("mapSprite");

		let fields = [mapName, mapWidth, mapHeight]; //, tilesPerLine, mapTileset, mapSprite

		function onlyLetters(str){ // COPIEE D'ICI : https://bobbyhadz.com/blog/javascript-check-if-string-contains-only-letters
	  		return /^[a-zA-Z]+$/.test(str);
		}

		function isFilled(){
			for(let i = 0; i < fields.length; i++){
				if(fields[i].value == ""){
					return false;
				}
			}
			return onlyLetters(mapName.value);
		}

		function clearFields(){
			for(field of fields){
				field.value = "";
			}
		}

		if(isFilled()){
			let filename = mapName.value;
			let mapdata = {};

			let background = [];
			for(let i = 0; i < mapHeight.value; i++){
				let row = Array.apply(null, Array(parseInt(mapWidth.value, 10)).map(function f() {}));
				background.push(row);
			}

			mapdata["background"] = background;
			mapdata["sprite"] = {
				path: "img/sprite.png",
				resolution: 8,
				starting: [3, 3]
			};
			mapdata["tileset"] = {
				path: "img/tileset.png",
				tilePerLine: 2,
				tileResolution: 8
			};

			let tileset = new Image();
			tileset.src = mapdata.tileset.path;
			tileset.onload = function getDimension(){
				let tilesetWidth = this.width / mapdata.tileset.tileResolution;
				let tilesetHeight = this.height / mapdata.tileset.tileResolution;
				let tileProp = {
					consistency: "normal"
				};
				mapdata["tileProperties"] = {};
				for(let i = 0; i < tilesetWidth * tilesetHeight; i++){
					mapdata["tileProperties"][i.toString()] = tileProp;
				}
				result[filename] = mapdata;
				saveJSON(url, result);
			};
		}
		else{
			console.log("Impossible de créer la carte");
			return;
		}
	}
}

main("e");
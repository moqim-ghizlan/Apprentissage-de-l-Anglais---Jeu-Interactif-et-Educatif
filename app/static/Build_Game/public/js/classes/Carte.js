class Carte{
    //tileset, terrain, murs, portesF, portesO,
    constructor(nom) {
        const xhr = getXMLHttpRequest();
        xhr.open("GET", './maps/' + nom + '.json', false);
        xhr.send(null);
        if (xhr.readyState != 4 || (xhr.status != 200 && xhr.status != 0))
            throw new Error("Impossible de charger la carte nommée \"" + nom + "\" (code HTTP : " + xhr.status + ").");
        const mapJsonData = xhr.responseText;
        this.mapData = JSON.parse(mapJsonData);

        //const fs = require('fs');
        //const storeData = (data, path) => {
        //    try {
        //        fs.writeFileSync(path, JSON.stringify(data))
        //    } catch (err) {
        //        console.error(err)
        //    }
        //}

        //const loadData = (path) => {
        //    try {
        //        return fs.readFileSync(path, 'utf8')
        //    } catch (err) {
        //        console.error(err)
        //        return false
        //    }
        //}

        this.tileset = new Tileset(this.mapData.tileset);
        this.terrain = this.mapData.terrain;
        this.murs = this.mapData.murs;
        this.portesF = this.mapData.portesF;
        this.portesO = this.mapData.portesO;
        this.personnages = new Array();
    }


    ouvrirPorte(){
        // supprimer la premeiere porte de la liste this.portesF et le rajouter à this.portesO
        const porte = this.portesF.shift();
        this.portesO.unshift(porte);
    }
//
    //modifierMapData(nom){
    //    var jsondata;
    //    var flickr = {'action': 'Flickr', 'get':'getPublicPhotos'};
    //    var data = JSON.stringify(flickr);
//
    //    var xhr = new XMLHttpRequest();
//
//
    //    xhr.open("GET", './maps/' + nom + '.json', false);
    //    xhr.send(null);
    //    console.log(xhr.readyState, xhr.status);
    //    if (xhr.readyState != 4 || (xhr.status != 200 && xhr.status != 0))
    //        throw new Error("Impossible de charger la carte nommée \"" + nom + "\" (code HTTP : " + xhr.status + ").");
    //    const mapJsonData = xhr.responseText;
    //    let mapData = JSON.parse(mapJsonData);
    //    console.log(mapData);
    //    //on modifie les nos vlaeurs:
    //    mapData['portesO'] = [2,1, 3, 4, 5, 6];
    //    console.log(mapData);
    //    var data = JSON.stringify(mapData);
    //    console.log(data);
//
//
//
    //    xhr.open("PUST", './maps/' + nom + '.json', !0);
    //    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    //    xhr.send(data);
    //    xhr.onreadystatechange = function () {
    //        if (xhr.readyState === 4 && xhr.status === 200) {
    //            //in case we reply back from server
    //            jsondata = JSON.parse(xhr.responseText);
    //            console.log(jsondata);
    //        }
    //    }
    //}
//

    getNumeroTuile(x , y){
        return this.terrain[y][x];
    }

    getHauteur() {
        return this.terrain.length;
    }
    getLargeur() {
        return this.terrain[0].length;
    }
    dessinerMap(context) {
        for (let i = 0, l = this.terrain.length; i < l; i++) {
            let ligne = this.terrain[i];
            let y = i * 32;
            for (let j = 0, k = ligne.length; j < k; j++) {
                this.tileset.dessinerTile(ligne[j], context, j * 32, y);
            }
        }
        // Dessin des personnages
        for(var i = 0, l = this.personnages.length ; i < l ; i++) {
            this.personnages[i].dessinerPersonnage(context);
        }
    }

    // Pour ajouter un personnage
    addPersonnage(perso) {
        this.personnages.push(perso);
    }

    getPersonnage(){
        return this.personnages[0];
    }
}






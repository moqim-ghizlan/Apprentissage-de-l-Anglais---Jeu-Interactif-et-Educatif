


modifierMapData(nom){
    //modifier this.portesF et this.portesO dans this.mapData, et envoier this.mapData dans la fichier premiere.json
    // peut-être il faut supprimer la contenu de la fichier avant de la remplire 
    // faire un DELETE puis un PUT
    const xhr = getXMLHttpRequest();
    xhr.open("GET", './maps/' + nom + '.json', false);
    xhr.send(null);
    console.log(xhr.readyState, xhr.status);
    if (xhr.readyState != 4 || (xhr.status != 200 && xhr.status != 0))
        throw new Error("Impossible de charger la carte nommée \"" + nom + "\" (code HTTP : " + xhr.status + ").");
    const mapJsonData = xhr.responseText;
    let mapData = JSON.parse(mapJsonData);
    console.log(mapData);
    //on modifie les nos vlaeurs:
    mapData['portesO'] = [2,1, 3, 4, 5, 6];
    console.log(typeof(mapData));
    //on envoie avec un request le modification au serveur:
    xhr.open("PUT", './maps/' + nom + '.json', false);
    xhr.setRequestHeader("json", "application/json");
    //xhr.send("jsonTxt="+JSON.stringify(mapData));

}
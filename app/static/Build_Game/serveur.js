const express = require("express");
const app = express()
app.use(express.static('public'));


function connexionDB(name){
    const sqlite3 = require('sqlite3');
    const dbname = name
    // Ouverture de la base de données
    let db = new sqlite3.Database('./../../appdb.db', sqlite3.OPEN_READWRITE, err=> {
        if (err)
            throw err
        console.log('Database stated on ' + dbname)})
    return db
}


function getPlanCarte(){
    let db = connexionDB("appdb");
    let dataMap = db.get('SELECT * FROM Carte', (err, data) => {
        if (err)
            throw err
        console.log(data.getPlanCarte)
    })
}

//app.post('/data', async (request, responsse) => {
//    const data = await resquest.body;
//    const gotData = data.carteRecherche;
//    const nomCarte = gotData;
//    console.log(nomCarte);
//
//    let db = connexionDB();
//    let mapData = db.each('SELECT * FROM Carte', (err, data) => {
//        if (err)
//            throw err
//        console.log(data.planCarte)
//    })
//})


//const fs = require('fs');
//var data = fs.readFileSync('public/maps/premiere.json', 'utf8')
//console.log(data)
//let mapData = JSON.parse(data)
//console.log(mapData.tileset)



//app.get('/', function(req, res){
//    res.render('index',);
//})


app.listen(80, ()=> console.log("server listening on port 80"));




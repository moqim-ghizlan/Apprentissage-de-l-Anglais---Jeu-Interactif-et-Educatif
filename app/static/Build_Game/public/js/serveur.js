const express = require("express");
const app = express()

app.use(express.static('public'));

app.listen(80, ()=> console.log("server listening on port 80"));




//const http = require('http')
//const fs = require('fs')
//const port = 3000
//
//const server = http.createServer(function(req, res){
//    res.writeHead(200, {'Content-Type': 'text/html'})
//    fs.readFile('./../index.html', function(error, data){
//        if(error){
//            res.writeHead(404)
//            res.write('Error: File Not Found')
//        }else{
//            res.write(data)
//        }
//        res.end()   
//    })
//})
//
//
//server.listen(port, function(error){
//    if (error){
//        console.log('Something went worng', error)
//    } else {
//        console.log('Server is listening on port' + port)
//    }
//})//
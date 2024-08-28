const express = require('express');
const { Socket } = require('socket.io');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use(express.static('public '));

io.on('çonnection', (Socket) => { 
    console.log('um jogador entrou no jogo!');

    //logica de jogo aqui

}); 

http.listen(3000, () => {
    console.log('Servidor rodando em http://localhost:3000');
});



import React, { useState, useEffect } from 'react';
import { createDeck } from './cards';

const Game = () => {
    const [playerDeck, setPlayerDeck] = useState([]);
    const [opponentDeck, setOpponentDeck] = useState([]);
    const [currentPlayerCard, setCurrentPlayerCard] = useState(null);
    const [currentOpponentCard, setCurrentOpponentCard] = useState(null);

    useEffect(() => {
        const deck = createDeck();
        setPlayerDeck(deck.slice(0, 10));
        setOpponentDeck(deck.slice(10));
    }, []);

    const playTurn = () => {
        setCurrentPlayerCard(playerDeck[0]);
        setCurrentOpponentCard(opponentDeck[0]);

        // Implementar a lógica de batalha aqui
    };

    return (
        <div className="game-board">
            <div className="player-hand">
                {currentPlayerCard && (
                    <div className="card">
                        <p>Atk: {currentPlayerCard.atk}</p>
                        <p>Def: {currentPlayerCard.def}</p>
                        <p>Atks: {currentPlayerCard.atks}</p>
                        <p>Ex: {currentPlayerCard.ex}</p>
                    </div>
                )}
            </div>
            <button onClick={playTurn}>Jogar</button>
            <div className="opponent-hand">
                {currentOpponentCard && (
                    <div className="card">
                        <p>Atk: {currentOpponentCard.atk}</p>
                        <p>Def: {currentOpponentCard.def}</p>
                        <p>Atks: {currentOpponentCard.atks}</p>
                        <p>Ex: {currentOpponentCard.ex}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Game;

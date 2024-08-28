const generateRandomStat = () => Math.floor(Math.random() * 100) + 1;

const createCard = (id) => ({
    id,
    atk: generateRandomStat(),
    def: generateRandomStat(),
    atks: generateRandomStat(),
    ex: generateRandomStat()
});

export const createDeck = () => {
    const deck = [];
    for (let i = 1; i <= 20; i++) {
        deck.push(createCard(i));
    }
    return deck;
};

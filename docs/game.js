// Prosta gra Phaser.js
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

let player;

function preload() {
    this.load.image('player', 'player.png'); // Załaduj grafikę dla gracza
}

function create() {
    player = this.add.sprite(400, 300, 'player'); // Stwórz gracza na ekranie
}

function update() {
    // Prosta logika do poruszania graczem
    if (this.input.keyboard.isDown(Phaser.Input.Keyboard.KeyCodes.LEFT)) {
        player.x -= 5;
    }
    if (this.input.keyboard.isDown(Phaser.Input.Keyboard.KeyCodes.RIGHT)) {
        player.x += 5;
    }
}

const game = new Phaser.Game(config);

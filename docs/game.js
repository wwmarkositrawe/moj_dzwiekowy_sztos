let cursors;
let grafika;
let dzwiek1, dzwiek2;
let tekstStart;
let tekstRestart;
let konfetti = [];

const config = {
    type: Phaser.AUTO,
    width: 600,
    height: 400,
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    audio: {
        disableWebAudio: false
    }
};

const game = new Phaser.Game(config);

function preload() {
    this.load.image('grafika', 'grafika.jpg');
    this.load.audio('dzwiek1', 'nagranie1.mp3');
    this.load.audio('dzwiek2', 'nagranie2.mp3');
}

function create() {
    grafika = this.add.image(300, 200, 'grafika').setDisplaySize(600, 400);
    dzwiek1 = this.sound.add('dzwiek1');
    dzwiek2 = this.sound.add('dzwiek2');

    tekstStart = this.add.text(100, 180, "Kliknij, by zacząć", {
        fontSize: '32px',
        fill: '#000'
    });

    this.input.once('pointerdown', () => {
        tekstStart.setVisible(false);
        startGame.call(this);
    });
}

function startGame() {
    const powt = Phaser.Math.Between(1, 5);
    const odtworz = (n) => {
        if (n > 0) {
            dzwiek1.play();
            dzwiek1.once('complete', () => odtworz(n - 1));
        } else {
            dzwiek2.play();
            dzwiek2.once('complete', () => pokazKonfetti.call(this));
        }
    };
    odtworz(powt);
}

function pokazKonfetti() {
    for (let i = 0; i < 100; i++) {
        konfetti.push({
            x: Phaser.Math.Between(0, 600),
            y: Phaser.Math.Between(0, 400),
            r: Phaser.Math.Between(3, 7),
            kolor: Phaser.Display.Color.RandomRGB()
        });
    }
    tekstRestart = this.add.text(100, 180, "Kliknij, by zagrać jeszcze raz", {
        fontSize: '28px',
        fill: '#ff0000'
    });
    this.input.once('pointerdown', () => location.reload());
}

function update() {
    const g = game.scene.scenes[0];
    if (konfetti.length > 0) {
        konfetti.forEach(k => {
            const kolo = g.add.circle(k.x, k.y, k.r, k.kolor.color);
            setTimeout(() => kolo.destroy(), 1000);
        });
        konfetti = [];
    }
}

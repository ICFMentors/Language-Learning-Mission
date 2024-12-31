const config = {
    type: Phaser.AUTO, // Automatically chooses WebGL or Canvas
    width: window.innerWidth,
    height: window.innerHeight,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 }, // No gravity for a top-down game
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

function preload() {
    // Load assets here
    this.load.image('player', 'static/images/character3nobackground.png');
    this.load.image('map', 'static/images/gameScene1.webp');
}

function create() {
    // Add background map centered and with bezels
    const map = this.add.image(config.width / 2, config.height / 2, 'map');
    map.setOrigin(0.5, 0.5);

    // Calculate the scale to fit the height of the game while preserving aspect ratio
    const scale = Math.min(config.width / map.width, config.height / map.height);
    map.setScale(scale);

    // Define collision boundaries for shelves based on the image
    this.shelves = this.physics.add.staticGroup();

    // Example: Define white tile areas where the player can walk
    // Add precise collision zones for the colorful shelves
    // Define collision boundaries for shelves and walkable areas based on the image
    this.shelves = this.physics.add.staticGroup();

    // Define collision zones for the shelves (non-walkable areas)
    const shelfAreas = [
        { x: 150, y: 150, width: 300, height: 100 }, // Top-left shelf
        { x: 450, y: 150, width: 300, height: 100 }, // Top-center shelf
        { x: 750, y: 150, width: 300, height: 100 }, // Top-right shelf
        { x: 150, y: 400, width: 300, height: 200 }, // Left-side shelf
        { x: 750, y: 400, width: 300, height: 200 }, // Right-side shelf
        { x: 450, y: 650, width: 600, height: 100 }, // Bottom-center shelf
    ];

    for (const shelf of shelfAreas) {
        const collider = this.add.rectangle(shelf.x, shelf.y, shelf.width, shelf.height, 0x000000, 0);
        this.physics.add.existing(collider);
        collider.body.setImmovable(true);
        this.shelves.add(collider);
    }

    // Add player sprite
    this.player = this.physics.add.sprite(config.width / 2, config.height / 2, 'player');
    this.player.setScale(0.2);
    // Scale down the character to look proportional in the store
    this.player.setCollideWorldBounds(true);
    this.physics.add.collider(this.player, this.shelves);

    // Add keyboard controls
    this.cursors = this.input.keyboard.createCursorKeys();
}

function update() {
    // Player movement
    if (this.cursors.left.isDown) {
        this.player.setVelocityX(-200);
    } else if (this.cursors.right.isDown) {
        this.player.setVelocityX(200);
    } else {
        this.player.setVelocityX(0);
    }

    if (this.cursors.up.isDown) {
        this.player.setVelocityY(-200);
    } else if (this.cursors.down.isDown) {
        this.player.setVelocityY(200);
    } else {
        this.player.setVelocityY(0);
    }
}
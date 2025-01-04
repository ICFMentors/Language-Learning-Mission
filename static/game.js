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
    this.load.image('player', '../static/images/character3nobackground.png');
    this.load.image('npc', '../static/images/cashierNoBackground.png')
    this.load.image('map', '../static/images/gameScene1.webp');
}

function create() {
    // Add background map centered and with bezels
    const map = this.add.image(config.width / 2, config.height / 2, 'map');
    map.setOrigin(0.5, 0.5);

    // Calculate the scale to fit the height of the game while preserving aspect ratio
    const scale = Math.min(config.width / map.width, config.height / map.height);
    map.setScale(scale);

    // Add player sprite
    this.player = this.physics.add.sprite(config.width / 2, config.height / 2, 'player');

    // Scale down the character to look proportional in the store
    this.player.setScale(0.2);

    // Define collision boundaries for shelves based on the image
 
    // Define collision zones for the shelves (non-walkable areas)
    
    const boundaries = [
        { x: 0, y: (map.height/2), width: config.width, height: 1 },  // Top boundary
        { x: 0, y: -(map.height/2), width: config.width, height: 1 }, // Bottom boundary
        { x: -(config.width / 2), y: 0, width: 1, height: config.height },  // Left boundary
        { x: (config.width / 2), y: 0, width: 1, height: config.height}  // Right boundary
    ];
    

    this.boundaryGroup = this.physics.add.staticGroup();

    for (const boundary of boundaries) {
        const rect = this.add.rectangle(boundary.x, boundary.y, boundary.width, boundary.height, 0x000000, 0);
        this.physics.add.existing(rect);
        rect.body.setImmovable(true);
        this.boundaryGroup.add(rect);
    }

    // Add collision for the player against boundaries
    this.physics.add.collider(this.boundaryGroup, this.player);

    
    // cannot leave world
    this.player.setCollideWorldBounds(true);
    this.physics.add.collider(this.player, this.boundaryGroup);

    // Add keyboard controls
    this.cursors = this.input.keyboard.createCursorKeys();

    // Add cashier 
    this.cashier = this.physics.add.staticSprite(config.width / 2, config.height / 10, 'npc'); // Position for cashier table
    this.cashier.setScale(0.15);
    this.physics.add.existing(this.cashier);

    

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

    // Add spacebar input for interaction
    this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    this.canInteract = false;

    if (this.spaceKey.isDown) {
        getTranslation();
    }

    this.physics.add.overlap(this.player, this.cashier, () => {
        this.canInteract = true;
        const interactPrompt = document.getElementById('interact-prompt');
        interactPrompt.style.display = 'block';
        interactPrompt.style.left = `${this.cashier.x - 50}px`;
        interactPrompt.style.top = `${this.cashier.y - 80}px`;
    }, null, this);

    this.physics.add.overlap(this.player, this.cashier, () => {
        this.canInteract = true;
    }, null, this);

    this.physics.add.collider(this.player, this.cashier, () => {
        const interactPrompt = document.getElementById('interact-prompt');
        if (!this.canInteract) {
            interactPrompt.style.display = 'none';
        }
    });

    
}
function interactWithCashier() {
    // Placeholder for Python function integration
    fetch('/api/translate', {
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'interact_with_cashier' })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Cashier says: ${data.message}`); // Display JSON response as an alert
    })
    .catch(err => console.error('Error interacting with cashier:', err));
}

function getTranslation() {
    fetch('/api/translate?text=' + "hello" )
        //headers: {
        //    'Content-Type': 'application/json'
        //},
        //body: JSON.stringify({ action: 'interact_with_cashier' })
    
    .then(response => response.json())
    .then(data => {
        alert(`Cashier says: ${data.translated_text}`); // Display JSON response as an alert
    })
    .catch(err => console.error('Error interacting with cashier:', err));
}
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

const quadrantInputs = {
    1:"apple",
    2:"banana",
    3:"orange",
    4:"grapes",
    5:"mango",
    6:"kiwi",
    7:"strawberry",
    8:"pineapple",
    9:"watermelon"
}

const game = new Phaser.Game(config);

function preload() {
    // Load assets here
    this.load.image('playerIdle', '../static/images/playerIdle.png');
    this.load.spritesheet('playerMoving', '../static/images/ezgif.com-gif-to-sprite-converter.png', {
        frameWidth: 1024,
        frameHeight: 1024
    });
    this.load.spritesheet('playerMovingLeft', '../static/images/ezgif.com-reverse.png', {
        frameWidth: 1024,
        frameHeight: 1024
    });
    this.load.image('npc', '../static/images/cashierNoBackground.png');
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
    this.player = this.physics.add.sprite(config.width / 2, config.height / 2, 'playerIdle');

    // Scale down the character to look proportional in the store
    this.player.setScale(0.1);

    // Add animation for moving
    this.anims.create({
        key: 'move',
        frames: this.anims.generateFrameNumbers('playerMoving', { start: 0, end: 1 }),
        frameRate: 10,
        repeat: 1
    });
    this.anims.create({
        key: 'moveLeft',
        frames: this.anims.generateFrameNumbers('playerMovingLeft', { start: 3, end: 4 }),
        frameRate: 10,
        repeat: 1
    });
    
 
    // Define collision zones for the walls (non-walkable areas)
    
    //const boundaries = [
    //    { x:  config.width/2, y: 0, width: config.width, height: 10 },  // Top boundary
    //    { x: config.width/2 , y: (config.height), width: config.width, height: 10 }, // Bottom boundary
    //    { x: 0, y: 0, width: 1, height: config.height },  // Left boundary
    //    { x: config.width, y: 0, width: 1, height: config.height}  // Right boundary
    //];
    

    //this.boundaryGroup = this.physics.add.staticGroup();

    //for (const boundary of boundaries) {
    //    const rect = this.add.rectangle(boundary.x, boundary.y, boundary.width, boundary.height, 0x000000, 0);
    //    this.physics.add.existing(rect);
    //    rect.body.setImmovable(true);
    //    this.boundaryGroup.add(rect);
    //}

    // Add collision for the player against boundaries
    //this.physics.add.collider(this.boundaryGroup, this.player);

    
    // cannot leave world
    //this.player.setCollideWorldBounds(true);
    //this.physics.add.collider(this.player, this.boundaryGroup);

    // Add keyboard controls
    this.cursors = this.input.keyboard.createCursorKeys();

    // Add cashier 
    this.cashier = this.physics.add.staticSprite(config.width / 2, config.height / 10, 'npc'); // Position for cashier table
    this.cashier.setScale(0.15);
    this.physics.add.existing(this.cashier);

    

}


function update() {
    let isMoving = false;
    let isLeft = false;

    // Player movement
    this.player.setVelocity(0);

    if (this.cursors.left.isDown) {
        this.player.setVelocityX(-200);
        isMoving = true;
        isLeft = true;
    } else if (this.cursors.right.isDown) {
        this.player.setVelocityX(200);
        isMoving = true;
        isLeft = false;
    }

    if (this.cursors.up.isDown) {
        this.player.setVelocityY(-200);
        isMoving = true;
    } else if (this.cursors.down.isDown) {
        this.player.setVelocityY(200);
        isMoving = true;
    }

    // Change sprite based on movement
    if (isMoving) {
        if (!this.player.anims.isPlaying) {
            this.player.play('move');
            console.log("The player coods are: ", this.player.x, ", " , this.player.y);
            playerCoords = getPlayerCoords(this.player.x, this.player.y, config.height, config.width);
            console.log("The player is in zone: ", playerCoords);
            if (isLeft) {
                this.player.play('moveLeft');
            }
        }
    } else {
        if (this.player.anims.isPlaying) {
            this.player.stop();
            this.player.setTexture('playerIdle');
        }
    }

    // Add spacebar input for interaction
    this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    this.canInteract = false;

    if (this.spaceKey.isDown) {
        getTranslation(quadrantInputs[playerCoords]);
        this.spaceKey.isDown = false;
        
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
        return (`Cashier says: ${data.message}`); // Display JSON response as an alert
    })
    .catch(err => console.error('Error interacting with cashier:', err));
}

/*function getTranslation(text) {
    fetch('/api/translate?text=' + text )
        //headers: {
        //    'Content-Type': 'application/json'
        //},
        //body: JSON.stringify({ action: 'interact_with_cashier' })
    
    .then(response => response.json())
    .then(data => {
        document.getElementById('interact-prompt').innerText = (`Cashier says: ${data.translated_text}`); // Display JSON response as an alert
    })
    .catch(err => console.error('Error interacting with cashier:', err));
}*/

function getTranslation() {
    const userInput = document.getElementById('user-input').value;

    if (!userInput) {
        document.getElementById('interact-prompt').innerText = 'Please enter text to translate.';
        return;
    }

    fetch('/api/translate?text=' + encodeURIComponent(userInput))
        .then(response => response.json())
        .then(data => {
            document.getElementById('interact-prompt').innerText = `Cashier says: ${data.translated_text}`;
        })
        .catch(err => {
            console.error('Error interacting with cashier:', err);
            document.getElementById('interact-prompt').innerText = 'An error occurred. Please try again.';
        });

    document.getElementById('translate-box').style.display = 'none';
}



function getPlayerCoords(xpos, ypos, height, width) {
    
    
    if (xpos < (width/3)) {
        if (ypos < (height/3)) {
            return "1";
        } else if (ypos < (height*2/3) && ypos > (height/3)) {
            return "4";
        }else {
            return "7";
        }
    }else if (xpos > (width/3) && xpos < (width*2/3)) {
        if (ypos < (height/3)) {
            return "2";
        } else if (ypos < (height*2/3) && ypos > (height/3)) {
            return "5";
        }else {
            return "8";
        }
    }else {
        if (ypos < (height/3)) {
            return "3";
        } else if (ypos < (height*2/3) && ypos > (height/3)) {
            return "6";
        }else {
            return "9";
        }
    }
}
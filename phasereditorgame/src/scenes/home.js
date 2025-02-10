
// You can write more code here

/* START OF COMPILED CODE */

/* START-USER-IMPORTS */
/* END-USER-IMPORTS */

export default class home extends Phaser.Scene {

	constructor() {
		super("home");

		/* START-USER-CTR-CODE */
		// Write your code here.
		/* END-USER-CTR-CODE */
	}

	/** @returns {void} */
	editorCreate() {

		// upKey
		const upKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.UP);

		// downKey
		const downKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.DOWN);

		// leftKey
		const leftKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.LEFT);

		// rightKey
		const rightKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.RIGHT);

		// sceneKey
		const sceneKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.P);

		// crossroads
		const crossroads = this.add.image(0, 0, "Crossroads");
		crossroads.setOrigin(0, 0);

		// player
		const player = this.add.sprite(427, 503, "characterIdle");
		player.scaleX = 0.3978902019419553;
		player.scaleY = 0.3978902019419553;
		player.play("run");

		this.player = player;
		this.upKey = upKey;
		this.downKey = downKey;
		this.leftKey = leftKey;
		this.rightKey = rightKey;
		this.sceneKey = sceneKey;

		this.events.emit("scene-awake");
	}

	/** @type {Phaser.GameObjects.Sprite} */
	player;
	/** @type {Phaser.Input.Keyboard.Key} */
	upKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	downKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	leftKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	rightKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	sceneKey;

	/* START-USER-CODE */

	// Write your code here

	create() {

		this.editorCreate();




		// Add animation for moving
		// this.anims.create({
		// 	key: 'move',
		// 	frames: this.anims.generateFrameNumbers('player_moving', { start: 0, end: 1 }),
		// 	frameRate: 10,
		// 	repeat: 1
		// });
		// this.anims.create({
		// 	key: 'moveLeft',
		// 	frames: this.anims.generateFrameNumbers('player_moving_left', { start: 3, end: 4 }),
		// 	frameRate: 10,
		// 	repeat: 1
		// });




	}

	update() {
    let isMoving = false;
    let isLeft = false;

    // // Player movement


    if (this.leftKey.isDown) {
        this.player.x -= 2;  

        isMoving = true;
        isLeft = true;
    } else if (this.rightKey.isDown) {
        this.player.x += 2;
        isMoving = true;
        isLeft = false;
    } 

    if (this.upKey.isDown) {
        this.player.y -= 2;
        isMoving = true;
    } else if (this.downKey.isDown) {
        this.player.y += 2;
        isMoving = true;
    } 

	if ((this.player.x > 230 && this.player.x < 350) && this.player.y > 550) {
		this.scene.start('house');
	}

    // // Change sprite based on movement
    if (isMoving) {

		this.player.play('move');
		// console.log("The player coods are: ", this.player.x, ", " , this.player.y);
		// playerCoords = getPlayerCoords(this.player.x, this.player.y, config.height, config.width);
		// console.log("The player is in zone: ", playerCoords);
		if (isLeft) {

			this.player.flipX;
			this.player.play('move');
		}

    } else {

        this.player.stop();
        this.player.setTexture('characterIdle');
    }

    // // Add spacebar input for interaction
    // this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    // this.canInteract = false;

    // if (this.spaceKey.isDown) {
    //     getTranslation(quadrantInputs[playerCoords]);
    //     this.spaceKey.isDown = false;

    // }
	/* END-USER-CODE */
}

/* END OF COMPILED CODE */

// You can write more code here
}
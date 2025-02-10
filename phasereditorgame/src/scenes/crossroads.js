
// You can write more code here

/* START OF COMPILED CODE */

import PlayerPrefab from "./PlayerPrefab.js";
/* START-USER-IMPORTS */
/* END-USER-IMPORTS */

export default class crossroads extends Phaser.Scene {

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

		// crossroads
		const crossroads = this.add.image(0, 0, "Crossroads");
		crossroads.setOrigin(0, 0);

		// player
		const player = new PlayerPrefab(this, 287, 503);
		this.add.existing(player);

		this.player = player;
		this.upKey = upKey;
		this.downKey = downKey;
		this.leftKey = leftKey;
		this.rightKey = rightKey;

		this.events.emit("scene-awake");
	}

	/** @type {PlayerPrefab} */
	player;
	/** @type {Phaser.Input.Keyboard.Key} */
	upKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	downKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	leftKey;
	/** @type {Phaser.Input.Keyboard.Key} */
	rightKey;

	/* START-USER-CODE */

	// Write your code here

	create() {

		this.editorCreate();
	}

	/* END-USER-CODE */
}

/* END OF COMPILED CODE */

// You can write more code here


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

	editorCreate(): void {

		// crossroads
		const crossroads = this.add.image(646, 360, "Crossroads");
		crossroads.scaleX = 1.179349039894206;
		crossroads.scaleY = 1.179349039894206;

		this.events.emit("scene-awake");
	}

	/* START-USER-CODE */

	// Write your code here

	create() {

		this.editorCreate();

	}

	/* END-USER-CODE */
}

/* END OF COMPILED CODE */

// You can write more code here

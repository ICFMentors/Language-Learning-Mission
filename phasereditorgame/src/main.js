import Level from "./scenes/Level.js";
import home from "./scenes/home.js";

window.addEventListener('load', function () {

	var game = new Phaser.Game({
		width: 572,
		height: 574,
		type: Phaser.AUTO,
        backgroundColor: "#242424",
		scale: {
			mode: Phaser.Scale.FIT,
			autoCenter: Phaser.Scale.CENTER_BOTH
		}
	});

	game.scene.add("home", home);
	game.scene.add("Level", Level);
	game.scene.add("Boot", Boot, true);
});

class Boot extends Phaser.Scene {

	preload() {
		
		this.load.pack("pack", "assets/asset-pack.json");
		// this.load.spritesheet('player_moving', 'playerMovingLeft', {
        // 	frameWidth: 1024,
        // 	frameHeight: 1024
    	// });
    	// this.load.spritesheet('player_moving_left', 'playerMovingLeft', {
        // 	frameWidth: 1024,
        // 	frameHeight: 1024
    	// });
	}

	create() {

		this.scene.start("home");

		
		

		
	}


	

}


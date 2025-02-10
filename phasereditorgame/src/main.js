import Level from "./scenes/Level.js";
import crossroads from "./scenes/crossroads.js";
import house from "./scenes/house.js";

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

	game.scene.add("house", house);
	game.scene.add("crossroads", crossroads);
	game.scene.add("Level", Level);
	game.scene.add("Boot", Boot, true);
});

class Boot extends Phaser.Scene {

	preload() {
		
		//this.load.pack("pack", '/assets/asset-pack.json');
		if (window.assetPack) {
			this.load.json("pack", window.assetPack);
			console.log(assetPack);
			this.load.once('complete', () => {
				let data = this.cache.json.get('pack'); // Get the loaded JSON
			
				if (data && Array.isArray(data.section1.files)) {
					// Loop through each object and modify the "url" property
					for (let i = 0; i < data.section1.files.length; i++) {
						
						let url = data.section1.files[i].url;
						url = "phasereditorgame/" + (url);
						data.section1.files[i].url = url;
						if (data.section1.files[i].type == "image")
							this.load.image(data.section1.files[i].key, url);
						else if (data.section1.files[i].type == "json")
							this.load.json(data.section1.files[i].key, url);
						else if (data.section1.files[i].type == "animation")
							this.load.animation(data.section1.files[i].key, url);
					};
						
			
					// Update the JSON cache with the modified data
					this.cache.json.add('pack', data);
			
					console.log('Modified asset pack:', data);
					//this.load.image('Crossroads', "phasereditorgame/assets/Crossroads.webp");
					this.load.pack('pack', data);
				} else {
					console.error('Failed to load asset pack or invalid structure:', data);
				}
			
				this.load.start();
			});
		} else 
		{
			this.load.pack("pack", 'assets/asset-pack.json');
		}
		
		this.load.start();
		
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

		this.scene.start("crossroads");
		//this.scene.start('crossroads');
		
		
		

		
	}

	update() {

	}

	

}


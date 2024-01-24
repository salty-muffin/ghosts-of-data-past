<script lang="ts">
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import type { PageData } from './$types';

	export let data: PageData;

	import { onMount } from 'svelte';
	import Sketch from './scene';
	import { timestamp } from '$lib/stores/timestamp';

	const MAXRECORDING = 60;

	let container: HTMLDivElement;
	let canvas: HTMLCanvasElement;

	let show = false;
	let download = false;
	let url = '';

	let sketch: Sketch;

	let relaxation: number;
	let radius: number;
	let strength: number;

	$: if (sketch) sketch.setParameters(relaxation / 10000 + 0.99, radius / 100, strength / 100);

	$: onMount(() => {
		// load image
		const image = new Image();
		image.src = data.qr;

		// draw text & qr code on canvas
		const ctx = canvas.getContext('2d', { alpha: false });
		if (ctx) {
			const draw = () => {
				// get current height
				canvas.width = container.offsetWidth;
				canvas.height = container.offsetHeight;

				// draw image
				const imageSize = container.offsetHeight * 0.5;

				ctx.drawImage(
					image,
					(container.offsetWidth - imageSize) / 2,
					(container.offsetHeight - imageSize) / 2,
					imageSize,
					imageSize
				);

				// draw text
				ctx.font = '1px "ABC Favorit Lining", sans-serif';
				const textSize =
					(container.offsetWidth /
						ctx.measureText(
							`${data.domain.replace('http://', '').replace('https://', '')}${
								data.gate ? `/?gate=${data.gate}` : ''
							}`
						).width) *
					0.5;
				ctx.font = `${textSize}px "ABC Favorit Lining", sans-serif`;
				ctx.textAlign = 'center';
				ctx.textBaseline = 'top';
				ctx.fillStyle = 'rgb(255 255 255 / 100%)';
				ctx.fillText(
					`${data.domain.replace('http://', '').replace('https://', '')}${
						data.gate ? `/?gate=${data.gate}` : ''
					}`,
					container.offsetWidth / 2,
					container.offsetHeight * 0.8
				);
			};

			const init = () => {
				draw();
				window.addEventListener('resize', draw);

				sketch = new Sketch(container, canvas, MAXRECORDING);
				sketch.animate();

				relaxation = (sketch.relaxation - 0.99) * 10000;
				radius = sketch.radius * 100;
				strength = sketch.strength * 100;

				window.addEventListener('keydown', (e) => {
					if (e.key == ' ') {
						if (!$timestamp.recording) {
							sketch.startRecording();
						} else {
							sketch.stopRecording();
						}
					}
					if (e.key == 'p') {
						if (!sketch.playing) {
							sketch.play();
						} else {
							sketch.stop();
						}
					}
					if (e.key == 's') {
						show = !show;
					}
					if (e.key == 'r') {
						sketch.resetRecording();
						download = false;
					}
				});
			};
			if (image.complete) {
				init();
			} else {
				image.addEventListener('load', init);
			}
		}
	});

	const saveData = () => {
		if (sketch) {
			const blob = new Blob([sketch.getDisplacementBuffer()]);

			url = window.URL.createObjectURL(blob);

			download = true;
		}
	};

	const downloadData = () => {
		const a = document.createElement('a');
		a.href = url;
		a.download = 'distortion_data.dat';
		a.target = '_blank';
		a.style.display = 'none';
		document.body.appendChild(a);
		a.click();
		a.remove();

		setTimeout(() => window.URL.revokeObjectURL(url), 20000);
	};
</script>

<div class="link" bind:this={container}>
	<canvas id="canvas" bind:this={canvas} />
	<span id="timestamp" class="ui" class:recording={$timestamp.recording}>{$timestamp.time}</span>
	<span id="info" class="ui">
		press SPACE for recording, P for playback, S to display extras & R to reset recording
	</span>
	<div class="ui" id="save" class:show>
		<button on:click={saveData}>save recording</button>
		{#if download}
			<button id="download" on:click={downloadData}>download recording</button>
		{/if}
	</div>
	<div id="settings" class="ui" class:show>
		<input
			type="range"
			id="relaxation"
			name="relaxation"
			min="0"
			max="100"
			step="5"
			bind:value={relaxation}
		/>
		<label for="relaxation">relaxation</label>
		<input type="range" id="radius" name="radius" min="0" max="100" step="5" bind:value={radius} />
		<label for="radius">radius</label>
		<input
			type="range"
			id="strength"
			name="strength"
			min="0"
			max="100"
			step="5"
			bind:value={strength}
		/>
		<label for="strength">strength</label>
	</div>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.link {
		width: 100vw;
		height: 100vh;
	}

	#canvas {
		display: none;
		pointer-events: none;
		position: absolute;
	}

	.ui {
		position: absolute;

		color: white;
	}

	#timestamp {
		left: 1em;
		top: 1em;

		&.recording {
			color: red;
		}
	}

	#save {
		position: absolute;
		left: 1em;
		bottom: 1em;

		color: black;

		display: none;
		&.show {
			display: block;
		}
	}

	#settings {
		right: 1em;
		bottom: 1em;

		flex-direction: column;

		display: none;
		&.show {
			display: flex;
		}
	}

	#info {
		position: absolute;
		right: 1em;
		top: 1em;

		color: white;
	}

	.qr {
		max-width: 70vh;
		height: auto;
	}
</style>

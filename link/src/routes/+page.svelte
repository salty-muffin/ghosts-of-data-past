<script lang="ts">
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import type { PageData } from './$types';

	export let data: PageData;

	import { onMount } from 'svelte';
	import Sketch from './scene';

	let container: HTMLDivElement;
	let canvas: HTMLCanvasElement;

	onMount(() => {
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

			draw();
			window.addEventListener('resize', draw);

			const initSketch = () => {
				const sketch = new Sketch(container, canvas);
				sketch.animate();
			};
			if (image.complete) {
				initSketch();
			} else {
				image.addEventListener('load', initSketch);
			}
		}
	});
</script>

<div class="link" bind:this={container}>
	<canvas id="canvas" bind:this={canvas} />
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.link {
		width: 100vw;
		height: 100vh;

		img,
		canvas {
			display: none;
			pointer-events: none;
			position: absolute;
		}
	}

	.qr {
		max-width: 70vh;
		height: auto;
	}

	// .text {
	// 	font-size: 2.5em;
	// 	line-height: 1.6;
	// 	font-family: $font-family-text;
	// 	font-feature-settings: 'calt' 1, 'liga' 1, 'rlig' 1, 'rvrn' 1, 'kern' 1, 'rclt' 1, 'ss04' 1,
	// 		'ss05' 1;
	// 	color: map-get($colors, 'foreground');

	// 	font-weight: 200;

	// 	p {
	// 		margin: 0;
	// 	}

	// 	a {
	// 		color: map-get($colors, 'foreground');
	// 		font-family: $font-family-underline;
	// 		font-feature-settings: 'calt' 1, 'liga' 1, 'rlig' 1, 'rvrn' 1, 'kern' 1, 'rclt' 1, 'ss04' 1,
	// 			'ss05' 1, 'ss09' 1;
	// 		text-decoration: none;
	// 	}
	// }
</style>

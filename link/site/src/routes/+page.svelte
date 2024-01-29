<script lang="ts">
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import type { PageData } from './$types';

	export let data: PageData;

	import { onMount } from 'svelte';
	import Sketch from './scene';

	let container: HTMLDivElement;
	let canvas: HTMLCanvasElement;

	let sketch: Sketch;

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
				// ctx.font = '1px "ABC Favorit Lining", sans-serif';
				// const textSize =
				// 	(container.offsetWidth /
				// 		ctx.measureText(
				// 			`${data.domain.replace('http://', '').replace('https://', '')}${
				// 				data.gate ? `/?gate=${data.gate}` : ''
				// 			}`
				// 		).width) *
				// 	0.5;
				// ctx.font = `${textSize}px "ABC Favorit Lining", sans-serif`;
				ctx.font = '35.3px "ABC Favorit Lining", sans-serif';
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

				sketch = new Sketch(container, canvas, 'data/sequence_drip_slow.dat', 30);
				sketch.updateCanvas();
				sketch.animate();
			};
			if (image.complete) {
				init();
			} else {
				image.addEventListener('load', init);
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
		overflow: hidden;
	}

	#canvas {
		display: none;
		pointer-events: none;
		position: absolute;
	}

	@keyframes qrMove {
		from {
			transform: translateX(-10px);
		}

		to {
			transform: translateX(10px);
		}
	}

	canvas {
		animation: 30s infinite alternate linear qrMove;
	}
</style>

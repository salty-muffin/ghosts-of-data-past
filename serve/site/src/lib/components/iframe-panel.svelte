<script lang="ts">
	import { onMount } from 'svelte';

	import Player from '@vimeo/player';

	let className = '';
	export { className as class };
	export let url: string;
	export let player: Player;

	let iframe: HTMLIFrameElement;
	let wrapper: HTMLElement;

	let aspectRatio: number;
	let playing = false;
	let targetWidth = 0;
	let targetHeight = 0;

	const calculateDimensions = () => {
		if (aspectRatio !== 0) {
			const width = wrapper.offsetWidth;
			const height = wrapper.offsetHeight;
			if (width / aspectRatio >= height) {
				targetWidth = width;
				targetHeight = width / aspectRatio;
			} else {
				targetHeight = height;
				targetWidth = height * aspectRatio;
			}
		}
	};
	onMount(() => {
		iframe.src = `${url}?background=1&dnt=1`;

		player = new Player(iframe);

		// get aspect ration
		player.on('loaded', async () => {
			const width = await player.getVideoWidth();
			const height = await player.getVideoHeight();
			aspectRatio = width / height;

			// execute on first load
			calculateDimensions();

			// set resize listener so that it rerenders on every resize
			window.addEventListener('resize', calculateDimensions);

			// remove this function
			player.off('loaded');
		});

		// set up fade in of video at the right time
		player.on('playing', () => {
			playing = true;

			// remove this function
			player.off('playing');
		});

		// clean up function
		return () => {
			// remove resize listener
			window.removeEventListener('resize', calculateDimensions);
		};
	});
</script>

<div class="iframe-panel__wrapper {className}" bind:this={wrapper}>
	<div class="iframe-panel__animation-wrapper" style="opacity: {playing ? '0' : '1'}">
		<div class="iframe-panel__animation">
			<div />
			<span>x</span>
			<div />
			<span>x</span>
			<div />
		</div>
	</div>
	<iframe
		class="iframe-panel__iframe"
		style="width: {targetWidth}px; height: {targetHeight}px; opacity: {playing ? '1' : '0'}"
		title="vimeo-player"
		src="about:blank"
		bind:this={iframe}
		frameborder="0"
		allow="autoplay"
	/>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.iframe-panel__wrapper {
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.iframe-panel__iframe {
		border: none;
		pointer-events: none;
		flex-shrink: 0;
		transition: opacity 2s ease-in-out;
	}

	@keyframes fadeInOut {
		0% {
			opacity: 0;
		}
		30% {
			opacity: 0;
			transform: translateY(80%);
		}
		100% {
			opacity: 1;
			transform: translateY(-20%);
		}
	}

	.iframe-panel__animation-wrapper {
		display: inline-block;
		position: absolute;
		left: 50%;
		right: 50%;
		transform: translate(-50%, -50%);
		width: 80px;
		height: 80px;

		z-index: -1;

		transition: opacity 0.5s ease-in-out;
	}

	.iframe-panel__animation {
		display: flex;
		align-items: center;

		div {
			width: 1em;
			height: 1em;

			background-color: map-get($colors, 'foreground');
			border-radius: 100%;

			animation-name: fadeInOut;
			animation-duration: 1.6s;
			animation-timing-function: ease;
			animation-iteration-count: infinite;
			animation-direction: alternate;
			animation-fill-mode: both;
		}
		div:nth-of-type(1) {
			animation-delay: 0s;
		}
		div:nth-of-type(2) {
			animation-delay: 0.2s;
		}
		div:nth-of-type(3) {
			animation-delay: 0.4s;
		}

		span {
			visibility: hidden;
			width: map-get($margin-secondary, 'sm');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.iframe-panel__animation {
			div {
				width: 1.1em;
				height: 1.1em;
			}

			span {
				width: map-get($margin-secondary, 'md');
			}
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.iframe-panel__animation {
			div {
				width: 1.3;
				height: 1.3;
			}

			span {
				width: map-get($margin-secondary, 'lg');
			}
		}
	}
</style>

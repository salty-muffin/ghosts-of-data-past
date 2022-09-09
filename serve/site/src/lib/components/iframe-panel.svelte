<script lang="ts">
	import { onMount } from 'svelte';

	import Player from '@vimeo/player';

	let className = '';
	export { className as class };
	export let url: string;

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

		const player = new Player(iframe);

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
	<iframe
		class="iframe-panel__iframe"
		style="width: {targetWidth}px; height: {targetHeight}px; opacity: {playing ? '1' : '0'}"
		title="vimeo-player"
		src="about:blank"
		bind:this={iframe}
		frameborder="0"
	/>
</div>

<style global lang="scss">
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
</style>

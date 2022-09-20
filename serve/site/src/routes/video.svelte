<script lang="ts">
	import IframePanel from '$lib/components/iframe-panel.svelte';
	import Nav from '$lib/components/nav.svelte';

	import type Player from '@vimeo/player';

	let player: Player;
</script>

<div class="video">
	<IframePanel bind:player class="video__panel" url="https://player.vimeo.com/video/636103889" />
	<Nav class="video__nav" links={[{ href: '/background', text: 'background' }]} />
</div>
<a href="#text">
	<div class="video__arrow">
		<svg width="30" height="37" viewBox="0 0 30 37" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M15 2V34M15 34L27 22.0784M15 34L3 22.0784"
				stroke-width="3"
				stroke-linecap="square"
			/>
		</svg>
	</div>
</a>
<div class="video__text" id="text">
	<p>
		This is a video documentation of <em>ghosts of data past</em>.
	</p>
	<p>
		The background texts and all other pages are visible exactly like this in the artwork. Only this
		page would usually hold the live generated chat of which a short excerpt is here documented.
	</p>
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.video {
		position: relative;
		width: 100vw;
		height: 100vh;
		max-height: -webkit-fill-available;
	}

	.video__arrow {
		position: absolute;
		bottom: map-get($nav-size, 'sm');
		left: 0;

		padding: 0.5em 0.5em 0.2em;
		margin: 1em;

		background-color: map-get($colors, 'background');

		svg {
			path {
				stroke: map-get($colors, 'foreground');
			}
		}
	}

	.video__panel {
		width: 100%;
		height: 100%;

		z-index: -1;
	}

	.video__nav {
		position: absolute;
		left: 0;
		bottom: 0;
		right: 0;
	}

	.video__text {
		padding: map-get($margin-primary, 'sm');
		border-top: map-get($border-width, 'sm') solid map-get($colors, 'foreground');

		& > *:first-of-type {
			margin-top: 0;
		}
		& > *:last-of-type {
			margin-bottom: 0;
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.video__arrow {
			bottom: map-get($nav-size, 'lg');

			svg {
				width: 3em;
				height: auto;
			}

			padding: 0.7em 0.7em 0.3em;
			margin: 1.5em;
		}

		.video__text {
			padding: map-get($margin-primary, 'md');
			border-top: map-get($border-width, 'md') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-width: 80em) {
		.video__arrow {
			display: none;
		}

		.video__elements {
			position: absolute;
			bottom: 0;
			left: 0;
			right: 0;
		}

		.video__text {
			position: absolute;
			bottom: map-get($nav-size, 'md');
			left: 0;

			margin: 2em;
			padding: 2em;

			width: 19em;

			border-top: none;

			background-color: map-get($colors, 'background');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.video__text {
			bottom: map-get($nav-size, 'lg');

			width: 22em;
		}
	}
</style>
